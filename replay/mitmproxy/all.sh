#!/bin/bash
set -x

RECORDINGS=$(for i in `pwd`/../../recordings/mitmproxy/* ; do echo -n "--server-replay $i "; done)
mitmdump $RECORDINGS --set http2_priority=true --set server_replay_refresh=false --set server_replay_nopop=true --server-replay-kill-extra "$@"
