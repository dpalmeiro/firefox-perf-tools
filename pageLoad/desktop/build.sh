#!/bin/bash
set -x

if [ $1  == "--refresh" ]; then
  rm -rf browsertime
fi

if [ ! -d directory ]; then
  cp -R ../../external/browsertime .
  cp docker/scripts/start.sh browsertime/docker/scripts/start.sh
  cp Dockerfile browsertime/docker/Dockerfile
fi

cd browsertime

docker system prune -a
sudo docker build -t custom/browsertime .
