sudo docker run --cap-add=NET_ADMIN --shm-size=1g --rm -v "$(pwd)":/browsertime \
  -e REPLAY=true                                                                \
  -e LATENCY=100                                                                \
  -e JSGC_DISABLE_POISONING=1                                                   \
  -e BASEOPTS="--firefox.nightly --firefox.binaryPath /shape.base/firefox"      \
  -e  REFOPTS="--firefox.nightly --firefox.binaryPath /shape.base/firefox --firefox.preference javascript.options.ion:false"       \
  custom/browsertime:latest --skipHar -b firefox -n 3 "$@"
