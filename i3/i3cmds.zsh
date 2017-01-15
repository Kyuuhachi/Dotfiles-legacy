#!/usr/bin/env zsh
trap 'trap - TERM; kill -- -$$' INT TERM EXIT
pwd=${0:a:h}
source $pwd/../venv/bin/activate
truncate -s 0 ~/i3-log
truncate -s 0 ~/i3-out
$pwd/i3bg.py &>> ~/i3-log &
$pwd/i3kb.py &>> ~/i3-log &
$pwd/i3bar.py 2>> ~/i3-log | tee ~/i3-out &
wait
