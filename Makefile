# Variables
PYTHON := .venv/bin/python
PIP := .venv/bin/pip
PYTEST := .venv/bin/pytest
FLAKE8 := .venv/bin/flake8
BLACK := .venv/bin/black

.PHONY: help install test lint format docker-build docker-up docker-down clean run-api run-web run-gui run-cli

help: ## Mostrar ayuda
@echo "🎵 Spotify Downloader PRO"
@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependencias
@echo "📦 Instalando..."
$(PIP) install -r requirements.txt
$(PIP) install pytest pytest-cov flake8 black

test: ## Ejecutar tests
@echo "🧪 Tests..."
$(PYTEST) tests/ -v

lint: ## Verificar código
@echo "🔍 Lint..."
$(FLAKE8) . --count --statistics

format: ## Formatear código
@echo "✨ Format..."
$(BLACK) .

run-api: ## Ejecutar API
@echo "🚀 API..."
$(PYTHON) api.py

run-web: ## Ejecutar web
@echo "🌐 Web..."
cd web && $(PYTHON) -m http.server 8000

run-gui: ## Ejecutar GUI
@echo "🎨 GUI..."
$(PYTHON) gui.py

run-cli: ## Ejecutar CLI
@echo "💻 CLI..."
$(PYTHON) main.py

docker-build: ## Build Docker
docker-compose build

docker-up: ## Start containers
docker-compose up -d

docker-down: ## Stop containers
docker-compose down

clean: ## Limpiar
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete
