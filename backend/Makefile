SHELL :=/bin/bash

all:
	 @echo $(CURDIR)

.PHONY: build-deps
build-deps:
	pip install -r requirements.txt

.PHONY: build-index
build-index:
	python -m scripts.build_index

.PHONY: chat
chat:
	TOKENIZERS_PARALLELISM=false python -m app.llm_chat
