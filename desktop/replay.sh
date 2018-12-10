#!/bin/bash
set -x
sudo docker run --cap-add=NET_ADMIN --shm-size=1g --rm -v "$(pwd)":/browsertime \
  -e REPLAY=true -e LATENCY=100 -e JSGC_DISABLE_POISONING=1 \
  shapesearch/browsertime:latest --skipHar -b firefox --firefox.nightly --firefox.binaryPath /shape.opt/firefox -n 3 "$@"
