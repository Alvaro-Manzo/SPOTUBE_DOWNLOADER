.PHONY: help install test lint format docker-build docker-up docker-down clean run-api run-web run-gui

help: ## Mostrar esta ayuda
	@echo "🎵 Spotify Downloader PRO - Comandos disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependencias
	@echo "📦 Instalando dependencias..."
	pip install -r requirements.txt
	pip install pytest pytest-cov flake8 black

test: ## Ejecutar tests
	@echo "🧪 Ejecutando tests..."
	pytest tests/ -v --cov=. --cov-report=html

test-watch: ## Ejecutar tests en modo watch
	@echo "👀 Ejecutando tests en modo watch..."
	pytest-watch tests/ -v

lint: ## Verificar código con flake8
	@echo "🔍 Verificando código..."
	flake8 . --count --statistics

format: ## Formatear código con black
	@echo "🎨 Formateando código..."
	black .

docker-build: ## Construir imagen Docker
	@echo "🐳 Construyendo imagen Docker..."
	docker-compose build

docker-up: ## Iniciar contenedores
	@echo "🚀 Iniciando contenedores..."
	docker-compose up -d
	@echo "✅ Servicios iniciados:"
	@echo "   - API: http://localhost:5001"
	@echo "   - Web: http://localhost:8000"

docker-down: ## Detener contenedores
	@echo "🛑 Deteniendo contenedores..."
	docker-compose down

docker-logs: ## Ver logs de Docker
	docker-compose logs -f

clean: ## Limpiar archivos temporales
	@echo "🧹 Limpiando archivos temporales..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	rm -rf TEMPORAL/
	@echo "✅ Limpieza completada"

run-api: ## Ejecutar API backend
	@echo "🚀 Iniciando API en http://localhost:5001..."
	python api.py

run-web: ## Ejecutar servidor web
	@echo "🌐 Iniciando servidor web en http://localhost:8000..."
	cd web && python -m http.server 8000

run-gui: ## Ejecutar interfaz gráfica
	@echo "🖥️  Iniciando GUI..."
	python gui.py

run-cli: ## Ejecutar CLI básico
	@echo "⌨️  Iniciando CLI..."
	python main.py

run-cli-pro: ## Ejecutar CLI PRO
	@echo "⌨️  Iniciando CLI PRO..."
	python main_pro.py

dev: ## Entorno de desarrollo completo
	@echo "🔧 Iniciando entorno de desarrollo..."
	@make docker-up
	@echo ""
	@echo "✅ Entorno listo:"
	@echo "   - API: http://localhost:5001"
	@echo "   - Web: http://localhost:8000"
	@echo "   - Redis: localhost:6379"

check: ## Verificar todo (lint + test)
	@make lint
	@make test

all: clean install check ## Instalar, limpiar y verificar todo

info: ## Mostrar información del proyecto
	@echo "🎵 Spotify Downloader PRO"
	@echo "=========================="
	@echo "Python version: $$(python --version)"
	@echo "Pip version: $$(pip --version)"
	@echo "Docker version: $$(docker --version 2>/dev/null || echo 'No instalado')"
	@echo "=========================="
