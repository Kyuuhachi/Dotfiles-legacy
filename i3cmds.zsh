#!/usr/bin/env zsh
trap 'trap - TERM; kill -- -$$' INT TERM EXIT
{
	{
		~/dot/i3bg.py &
		~/dot/i3kb.py &
		~/dot/i3bar.py &
		wait
	} 3>&2 2>&1 1>&3 # Swap stdout and stderr
} 2> ~/i3-out #And then send stderr to a log
