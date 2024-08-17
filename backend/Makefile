SHELL:=/bin/bash

# Container tool
CONTAINER_TOOL?=podman

# Database connection details
DB_NAME:=hirag
DB_PORT=5432
DB_USER:=hirag
DB_IMAGE?=docker.io/pgvector/pgvector:pg16

.PHONY: db-setup
db-setup:
	$(CONTAINER_TOOL) run --name psql-hi-rag \
		-e POSTGRES_DB=$(DB_NAME) -e POSTGRES_USER=$(DB_USER) -e POSTGRES_PASSWORD=$(DB_PASSWORD) \
		-p $(DB_PORT):5432 -d $(DB_IMAGE)

.PHONY: db-login
db-login:
	$(CONTAINER_TOOL) exec -it psql-hi-rag bash -c "psql -h localhost -U $(DB_USER) $(DB_NAME)"

.PHONY: deps
deps:
	pip install -r requirements.txt

.PHONY: lint
lint: deps
	pylint **/*.py

.PHONY: build-index
build-index:
	python -m scripts.build_index

.PHONY: build-index-with-db
build-index-with-db:
	python -m scripts.build_index_with_db

.PHONY: chat
chat:
	TOKENIZERS_PARALLELISM=false python -m app.llm_chat
