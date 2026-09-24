# Student Feedback App (Flask + Docker + GitHub Actions)

## Run locally
    pip install -r requirements.txt
    python app.py            # http://localhost:5000
    pytest                   # run tests

## Run with Docker
    docker build -t student-feedback .
    docker run -p 5000:5000 -v feedback-data:/data student-feedback

## CI/CD (.github/workflows/ci-cd.yml)
1. **On every push / PR to `main`:** install deps, lint (flake8), run pytest.
2. **On push to `main` only:** build Docker image, smoke-test `/health`,
   push to GitHub Container Registry (`ghcr.io/<user>/<repo>:latest` and `:<sha>`).

## Deploy the published image
    docker run -d -p 80:5000 -v feedback-data:/data ghcr.io/<user>/<repo>:latest
