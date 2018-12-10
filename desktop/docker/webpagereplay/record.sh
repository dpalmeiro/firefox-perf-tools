#!/bin/bash
set -x

sudo ./wpr record --http_port 80 --https_port 443 --https_cert_file wpr_cert.pem --https_key_file wpr_key.pem --inject_scripts deterministic.js /tmp/archive.wprgo
