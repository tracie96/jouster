.PHONY: help install run test clean docker-build docker-run

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

run: ## Run the application
	python main.py

test: ## Run API tests
	python test_api.py

test-unit: ## Run unit tests
	python test_unit.py

test-all: ## Run all tests
	python test_unit.py
	python test_api.py

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -f jouster.db

docker-build: ## Build Docker image
	docker build -t jouster-api .

docker-run: ## Run with Docker Compose
	docker-compose up --build

setup: ## Initial setup
	python3 -m venv venv
	@echo "Activate virtual environment with: source venv/bin/activate"
	@echo "Then run: make install"
