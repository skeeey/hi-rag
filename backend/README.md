# Backend

https://github.com/ollama/ollama

## Dev

1. Open the Command Palette, start typing the `Python: Create Environment`, then select `Venv`
2. Open the Command Palette, start typing the `Terminal: Create New Terminal`, then run the `python -m pip install <package-name>` to install dependent packages

```sh
python3 -m venv /path/to/new/virtual/environment
source bin/activate
pip install -r requirements.txt
```

## Run a chat bot locally


## Run a chat server

```sh
curl -v -X POST \
  -H "Accept: application/json" -H "Accept: application/json" \
  --json '{"id":"1","content":"My managed cluster status is offline in the ACM hub, how can I fix it?"}' \
  http://127.0.0.1:8000/chat
```

### TODO
- Support stream response
    https://sysid.github.io/server-sent-events/


## Test Questions

- My managed cluster status is offline in the Red Hat Advanced Cluster Management hub, how can I fix it?

- There is an error 'Secret in version "v1" cannot be ...' when I importing a cluster to the Red Hat Advanced Cluster Management hub, how can I fix it?
