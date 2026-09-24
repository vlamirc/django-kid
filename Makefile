# Atalhos do dia a dia. Rode "make" para ver a lista.
.DEFAULT_GOAL := help
RUN = docker compose run --rm web

help: ## Mostra esta ajuda
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

.env:
	cp .env.example .env

setup: .env ## Primeira vez: cria o .env, monta as imagens e o banco com dados de exemplo
	docker compose build
	$(RUN) python manage.py migrate
	$(RUN) python manage.py seed_demo

up: .env ## Sobe o sistema em http://localhost:8000
	docker compose up

down: ## Para os containers
	docker compose down

test: ## Roda os testes com cobertura
	$(RUN) pytest --cov

lint: ## Verifica estilo e erros comuns (ruff)
	$(RUN) ruff check .
	$(RUN) ruff format --check .

format: ## Formata o código e corrige o que der automaticamente
	$(RUN) ruff check --fix .
	$(RUN) ruff format .

migrations: ## Cria migrações a partir dos modelos
	$(RUN) python manage.py makemigrations

migrate: ## Aplica as migrações
	$(RUN) python manage.py migrate

superuser: ## Cria um administrador
	$(RUN) python manage.py createsuperuser

shell: ## Abre o shell do Django
	$(RUN) python manage.py shell

check: lint test ## Tudo que o CI verifica
	$(RUN) python manage.py makemigrations --check --dry-run

.PHONY: help setup up down test lint format migrations migrate superuser shell check
