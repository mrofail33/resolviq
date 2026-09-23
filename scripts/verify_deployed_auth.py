from __future__ import annotations

import argparse
import json
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def request_json(url: str, *, method: str = "GET", api_key: str | None = None, body: dict | None = None):
    headers = {"X-Demo-User": "demo@resolviq.local"}
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if api_key:
        headers["X-API-Key"] = api_key

    request = Request(url, data=data, headers=headers, method=method)
    with urlopen(request, timeout=20) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def request_text(url: str) -> tuple[int, str]:
    request = Request(url, method="GET")
    with urlopen(request, timeout=20) as response:
        return response.status, response.read().decode("utf-8", errors="replace")


def expect_http_error(url: str, expected_status: int) -> None:
    try:
        request_json(url)
    except HTTPError as exc:
        if exc.code == expected_status:
            return
        raise AssertionError(f"Expected {expected_status} from {url}, got {exc.code}") from exc
    raise AssertionError(f"Expected {expected_status} from {url}, but request succeeded")


def retry(label: str, action, attempts: int = 6, delay_seconds: int = 10):
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return action()
        except (AssertionError, HTTPError, URLError, TimeoutError) as exc:
            last_error = exc
            print(f"{label} attempt {attempt}/{attempts} failed: {exc}")
            if attempt < attempts:
                time.sleep(delay_seconds)
    raise AssertionError(f"{label} failed after {attempts} attempts") from last_error


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-url", required=True)
    parser.add_argument("--frontend-url", required=True)
    parser.add_argument("--api-key", required=True)
    args = parser.parse_args()

    api_url = args.api_url.rstrip("/")
    frontend_url = args.frontend_url.rstrip("/")

    status, health = retry("health check", lambda: request_json(f"{api_url}/health"))
    assert status == 200 and health["status"] == "ok"
    print("Backend health check passed.")

    retry("auth rejection check", lambda: expect_http_error(f"{api_url}/cases", 401))
    print("Unauthenticated /cases request was rejected.")

    title = f"Deployed auth verification {int(time.time())}"
    status, created = retry(
        "authorized case creation",
        lambda: request_json(
            f"{api_url}/cases",
            method="POST",
            api_key=args.api_key,
            body={"title": title, "category": "refund"},
        ),
    )
    assert status == 201 and created["title"] == title
    print(f"Authorized case creation passed with case id {created['id']}.")

    status, cases = retry("authorized case listing", lambda: request_json(f"{api_url}/cases", api_key=args.api_key))
    assert status == 200 and any(item["id"] == created["id"] for item in cases)
    print("Authorized case listing passed.")

    status, html = retry("frontend load", lambda: request_text(frontend_url))
    assert status == 200 and "Resolviq" in html
    print("Frontend loaded successfully.")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
