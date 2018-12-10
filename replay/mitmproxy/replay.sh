#!/bin/bash
set -x
mitmdump --server-replay /tmp/test.mp --set http2_priority=true --set server_replay_refresh=false --set server_replay_nopop=true --server-replay-kill-extra "$@"
