#!/bin/bash
set -x
rm -f /tmp/test.mp
rm -f content/*
mitmdump -w /tmp/test.mp -s scripts/inject.py --set http2_priority=true "$@"
