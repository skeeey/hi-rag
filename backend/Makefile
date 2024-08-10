SHELL :=/bin/bash

all:
	 @echo $(CURDIR)

.PHONY: build-deps
build-deps:
	pip install -r requirements.txt

.PHONY: build-index
build-index:
	python -m scripts.build_index

.PHONY: chat-example
chat-example:
	mkdir -p $(CURDIR)/_output/index
	tar -xf $(CURDIR)/example/data/index/index.tar.gz -C $(CURDIR)/_output/index
	INDEX_DIR=$(CURDIR)/_output/index TOKENIZERS_PARALLELISM=false python -m app.llm_chat

.PHONY: run-server
run-server:
	mkdir -p $(CURDIR)/_output/index
	tar -xf $(CURDIR)/example/data/index/index.tar.gz -C $(CURDIR)/_output/index
	INDEX_DIR=$(CURDIR)/_output/index hack/run_server.sh
