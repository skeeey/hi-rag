# Backend

Using [LLamaIndex](https://docs.llamaindex.ai/en/stable/) framework

## Prepare

1. (Optional but recommended) Create a virtual environment

```sh
VENV=<your python virtual environment dir>

# test with python >= 3.9.19
python -m venv $VENV
source $VENV/bin/activate
```

2. Install dependents

```sh
make build-deps
```

## Build Index

Currently, the pdf and markdown is supported

```sh
INDEX_DIR=<your-index-out-dir> LOCAL_DATA_DIR=<your-local-data-dir>  make build-index
```

## Run a chat bot

```sh
# using Groq
INDEX_DIR=<your-index-dir> LLM_MODEL=<llm-model-name> GROQ_TOKEN=<your-groq-token> make chat


# using Ollama
INDEX_DIR=<your-index-dir> LLM_MODEL=<llm-model-name> make chat
```

## Test Questions

- My Red Hat Advanced Cluster Management managed cluster status is offline in the Red Hat Advanced Cluster Management hub, how can I fix this?
- My cluster status is offline in the ACM hub, how can I fix it?
- There is an error 'Secret in version "v1" cannot be ...' when I importing a cluster into the ACM hub, how can I fix it?
- Will the CVE-2024-24786 have an impact on ACM?
- My ACM managed clusters created cannot reconnect to an AODP, how can I fix it?

## Build Development Environment

Refer to [Getting Started with Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial) to import the code in the VS Code

### TODO
- Support deploying with Containers
- Support [SSE](https://sysid.github.io/server-sent-events/)
