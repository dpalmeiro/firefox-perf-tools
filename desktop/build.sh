#!/bin/bash
set -x

#rm -rf docker/obj-base
#cp -R /home/denis/bugs/shape/mozilla-central/obj-base/dist/firefox docker/obj-base
#rm -rf docker/obj-opt
#cp -R /home/denis/bugs/shape/mozilla-central/obj-opt/dist/firefox docker/obj-opt

sudo docker system prune -a
sudo docker build -t shapesearch/browsertime .
