#!/usr/bin/env bash

REPO_DIR="$(cd "$(dirname ${BASH_SOURCE[0]})/../.." ; pwd -P)"

backend_dir=${REPO_DIR}/backend
work_dir=${backend_dir}/_output
index_dir=${work_dir}/index

mkdir -p ${index_dir}

tar -xf ${backend_dir}/example/data/index/index.tar.gz -C ${index_dir}

pushd ${backend_dir}
INDEX_DIR=${index_dir} make chat
popd
