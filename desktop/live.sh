#!/bin/bash
set -x

sudo docker run --shm-size=1g --rm -v "$(pwd)":/browsertime sitespeedio/browsertime:latest "$@"
