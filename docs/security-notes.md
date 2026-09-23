# Security Notes

Safe interview claim:

> I separated demo-safe behavior from production-sensitive behavior by using mock AI by default, environment variables for provider keys, input validation with Pydantic, and scoped file upload handling.

## Current proof

- `AI_PROVIDER=mock` lets demos run without exposing a paid API key.
- OpenAI usage is behind a service abstraction and environment variable.
- Pydantic schemas validate case creation, status updates, deadlines, and structured analysis output.
- Uploaded files are handled through FastAPI `UploadFile` and saved with `Path(...).name` to avoid trusting a full client-provided path.
- CORS origins are configured through settings instead of being hard-coded as wildcard production access.

## What not to claim yet

- Do not claim authentication or authorization is complete.
- Do not claim tenant isolation.
- Do not claim production document security.

## Simple next upgrade

Add login, user-owned cases, file size limits, file type checks, and tests that verify one user cannot access another user's cases.
