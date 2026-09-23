# Deployment and Operations Proof

Safe interview claim:

> I packaged the backend and database for local deployment, added CI checks, and verified the frontend can produce a production build.

## Current proof

- `docker-compose.yml` starts PostgreSQL for local development.
- `backend/Dockerfile` packages the FastAPI backend.
- `.github/workflows/ci.yml` runs backend tests and frontend build checks.
- `frontend/package.json` includes a production build script.
- The demo screenshot in `docs/screenshots/resolviq-dashboard.png` was captured from the local app running against a real backend demo database in mock AI mode.
- `DEMO_API_KEY` can enable a lightweight deployed-demo auth boundary between React and FastAPI.

## Local verification commands

```bash
cd backend
pytest
```

```bash
cd frontend
npm run build
```

## What not to claim yet

- Do not claim it is deployed to a public cloud.
- Do not claim production monitoring or autoscaling.
- Do not claim multi-user production security.

## Simple next upgrade

Deploy the frontend to a static host and the backend to a small container service, then add the public URLs and health-check output here.
