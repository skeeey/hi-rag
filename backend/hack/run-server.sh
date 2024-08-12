#!/usr/bin/env bash

REPO_DIR="$(cd "$(dirname ${BASH_SOURCE[0]})/../.." ; pwd -P)"

backend_dir=${REPO_DIR}/backend
work_dir=${backend_dir}/_output
log_dir=${work_dir}/logs

mkdir -p ${log_dir}

(exec uvicorn app.llm_chat_server:app --host 0.0.0.0) &> ${log_dir}/server.log &
SERVER_PID=$!
touch ${work_dir}/$SERVER_PID
echo "server ($SERVER_PID) is running ..."
echo "log is located at ${log_dir}/server.log"
