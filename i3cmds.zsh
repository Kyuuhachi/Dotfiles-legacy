#!/usr/bin/env zsh
trap 'trap - TERM; kill -- -$$' INT TERM EXIT
truncate -s 0 ~/i3-log
truncate -s 0 ~/i3-out
~/dot/i3bg.py &>> ~/i3-log &
~/dot/i3kb.py &>> ~/i3-log &
~/dot/i3bar.py 2>> ~/i3-log | tee ~/i3-out &
wait
