# PowerShell task runner for AI Engineering Roadmap
# Usage examples (run from repo root in PowerShell):
#   ./tasks.ps1 setup
#   ./tasks.ps1 lint
#   ./tasks.ps1 run:pipeline
#   ./tasks.ps1 run:api
#   ./tasks.ps1 docker:build
#   ./tasks.ps1 docker:run
#   ./tasks.ps1 rag:ingest
#   ./tasks.ps1 rag:app
#   ./tasks.ps1 mlflow:ui
param(
  [Parameter(Position=0)]
  [string]$Task = "help"
)

$ErrorActionPreference = "Stop"

function Ensure-Venv {
  if (-not (Test-Path ".venv")) {
    Write-Host "Creating venv .venv ..."
    python -m venv .venv
  }
}

function Py {
  # Use venv python if exists, else system python
  if (Test-Path ".venv\Scripts\python.exe") { return ".venv\Scripts\python.exe" }
  return "python"
}

function Pip {
  if (Test-Path ".venv\Scripts\pip.exe") { return ".venv\Scripts\pip.exe" }
  return "pip"
}

switch ($Task) {
  "help" {
    Write-Host "Available tasks:"
    Write-Host "  setup            - Create venv, install requirements, register Jupyter kernel"
    Write-Host "  lint             - Run ruff, black --check, isort --check-only"
    Write-Host "  run:pipeline     - Train tabular pipeline and save model.joblib"
    Write-Host "  run:api          - Start FastAPI service (model must exist)"
    Write-Host "  rag:ingest       - Build FAISS index from docs/*.md"
    Write-Host "  rag:app          - Run RAG CLI app"
    Write-Host "  docker:build     - Build Docker image fastapi-ml"
    Write-Host "  docker:run       - Run Docker container on port 8000"
    Write-Host "  mlflow:ui        - Start MLflow UI at http://127.0.0.1:5000"
    break
  }

  "setup" {
    Ensure-Venv
    & (Pip) install --upgrade pip setuptools wheel
    & (Pip) install -r "ai-engineering-roadmap/requirements.txt"
    & (Py) -m ipykernel install --user --name ai-roadmap --display-name "Python (ai-roadmap)"
    Write-Host "Setup complete."
    break
  }

  "lint" {
    & (Pip) install ruff black isort
    ruff check ai-engineering-roadmap
    black --check ai-engineering-roadmap
    isort --check-only ai-engineering-roadmap
    break
  }

  "run:pipeline" {
    Ensure-Venv
    & (Py) "ai-engineering-roadmap/labs/03-ml-pipeline.py" --n-samples 1500 --random-state 42
    break
  }

  "run:api" {
    Ensure-Venv
    $modelPath = "ai-engineering-roadmap/labs/07-fastapi-ml/model.joblib"
    if (-not (Test-Path $modelPath)) {
      Write-Warning "Model not found at $modelPath. Run './tasks.ps1 run:pipeline' first."
    }
    & (Py) "ai-engineering-roadmap/labs/07-fastapi-ml/main.py"
    break
  }

  "docker:build" {
    docker build -f "ai-engineering-roadmap/labs/07-fastapi-ml/Dockerfile" -t fastapi-ml .
    break
  }

  "docker:run" {
    if (-not (Test-Path "ai-engineering-roadmap/.env")) {
      Write-Warning "ai-engineering-roadmap/.env not found. Copy from .env.example if needed."
    }
    docker run --rm -p 8000:8000 --env-file "ai-engineering-roadmap/.env" fastapi-ml
    break
  }

  "rag:ingest" {
    Ensure-Venv
    & (Py) "ai-engineering-roadmap/labs/06-rag-chatbot/ingest.py" --glob "ai-engineering-roadmap/docs/*.md"
    break
  }

  "rag:app" {
    Ensure-Venv
    & (Py) "ai-engineering-roadmap/labs/06-rag-chatbot/app.py"
    break
  }

  "mlflow:ui" {
    mlflow ui --port 5000
    break
  }

  default {
    Write-Error "Unknown task '$Task'. Run './tasks.ps1 help' to see available tasks."
  }
}
