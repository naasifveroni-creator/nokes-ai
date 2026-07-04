.PHONY: help install dev test lint format run docker-build docker-run clean

help:
	@echo "Nokes AI - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install dependencies"
	@echo "  make dev              Install dev dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make run              Run the server"
	@echo "  make cli              Run interactive CLI"
	@echo "  make test             Run tests"
	@echo "  make lint             Run linters"
	@echo "  make format           Format code"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build     Build Docker image"
	@echo "  make docker-run       Run in Docker"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Remove cache and temp files"

install:
	pip install -r requirements.txt

dev: install
	pip install -r requirements-dev.txt

run:
	python -m nokes.api.server

cli:
	python -m nokes.cli.main chat

test:
	pytest -v --cov=nokes --cov-report=html

lint:
	flake8 nokes/ --max-line-length=100
	mypy nokes/ --ignore-missing-imports

format:
	isort nokes/ tests/
	black nokes/ tests/

docker-build:
	docker build -f docker/Dockerfile -t nokes:latest .

docker-run:
	docker run -e OPENAI_API_KEY=${OPENAI_API_KEY} -p 8000:8000 nokes:latest

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type d -name '.pytest_cache' -exec rm -rf {} +
	find . -type d -name '.mypy_cache' -exec rm -rf {} +
	find . -type d -name 'htmlcov' -exec rm -rf {} +
	rm -rf .coverage
