# Backend

https://github.com/ollama/ollama

## Dev

1. Open the Command Palette, start typing the `Python: Create Environment`, then select `Venv`
2. Open the Command Palette, start typing the `Terminal: Create New Terminal`, then run the `python -m pip install <package-name>` to install dependent packages

```sh
python -m venv $HOME/.hi-rag
source $HOME/.hi-rag/bin/activate
cd hi-rag/backend
make build-deps
```

```
INDEX_DIR=/home/cloud-user/rag-index/huggingface LOCAL_DATA_DIR=/home/cloud-user/hi-rag/backend/example/data/doc  make build-index
```

## Run a chat bot locally

time used 1390.281s
time used 4.898s

## Run a chat server

```sh
curl -v -X POST \
  -H "Accept: application/json" -H "Accept: application/json" \
  --json '{"id":"1","content":"My managed cluster status is offline in the ACM hub, how can I fix it?"}' \
  http://127.0.0.1:8000/chat
```

## Test Questions

- My managed cluster status is offline in the Red Hat Advanced Cluster Management hub, how can I fix it?

- There is an error 'Secret in version "v1" cannot be ...' when I importing a cluster to the Red Hat Advanced Cluster Management hub, how can I fix it?

### TODO
- Support stream response
    https://sysid.github.io/server-sent-events/