# Deployment and Operations Proof

Safe interview claim before a public deployment is connected:

> I packaged the backend and database for local deployment, added CI checks, and verified the frontend can produce a production build.

Safe interview claim after the deployed verification workflow passes:

> I deployed the React and FastAPI app with PostgreSQL and verified the auth-protected case flow from GitHub Actions.

## Current proof

- `docker-compose.yml` starts PostgreSQL for local development.
- `backend/Dockerfile` packages the FastAPI backend.
- `.github/workflows/ci.yml` runs backend tests and frontend build checks.
- `frontend/package.json` includes a production build script.
- The demo screenshot in `docs/screenshots/resolviq-dashboard.png` was captured from the local app running against a real backend demo database in mock AI mode.
- `DEMO_API_KEY` can enable a lightweight deployed-demo auth boundary between React and FastAPI.
- `render.yaml` defines a simple full-stack deployment with PostgreSQL, FastAPI, and React.
- `.github/workflows/deploy-verification.yml` verifies the deployed auth-protected flow after URLs and secrets are connected.

## Deployment verification

The deployed flow is intentionally small and easy to explain:

```text
User -> React -> demo authentication -> FastAPI -> PostgreSQL -> LLM/mock LLM
```

After deployment, set these GitHub Actions secrets:

```text
RESOLVIQ_API_URL
RESOLVIQ_FRONTEND_URL
RESOLVIQ_DEMO_API_KEY
```

Then set this GitHub repository variable:

```text
ENABLE_DEPLOY_VERIFY=true
```

The `Verify Deployed App` workflow checks:

- backend `/health`
- unauthenticated `/cases` returns `401`
- authenticated case creation succeeds
- authenticated case listing succeeds
- frontend page loads

## Local verification commands

```bash
cd backend
pytest
```

```bash
cd frontend
npm run build
```

## What not to claim yet unless the deployed verification workflow is green

- Do not claim it is deployed to a public cloud.
- Do not claim production monitoring or autoscaling.
- Do not claim multi-user production security.

## Simple next upgrade

Connect the deployment provider to GitHub, add the same demo key to backend and frontend environment variables, then turn on `ENABLE_DEPLOY_VERIFY`.
