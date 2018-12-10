sudo docker run --cap-add=NET_ADMIN --shm-size=1g --rm -v "$(pwd)":/browsertime \
  -e REPLAY=true                                                                \
  -e LATENCY=100                                                                \
  -e JSGC_DISABLE_POISONING=1                                                   \
  -e BASEOPTS="-b firefox"      \
  -e  REFOPTS="-b firefox --firefox.preference javascript.options.baselinejit:false"       \
  shapesearch/browsertime:latest --skipHar -b firefox -n 10 "$@"
