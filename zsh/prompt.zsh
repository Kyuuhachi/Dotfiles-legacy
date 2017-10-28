#!/bin/zsh
CURRENT_BG="default"
prompt_segment() {
	if [[ $RIGHT != 1 ]]; then
		if [[ $CURRENT_BG == "default" ]]; then
			echo -n "%{%K{$1}%F{$2}%} "
		else
			echo -n " %{%K{$1}%F{$CURRENT_BG}%}%{%F{$2}%} "
		fi
	else
		if [[ $CURRENT_BG == "default" ]]; then
			echo -n "%{%F{$1}%}%{%K{$1}%F{$2}%} "
		else
			echo -n " %{%F{$1}%K{$CURRENT_BG}%}%{%K{$1}%F{$2}%} "
		fi
	fi
	CURRENT_BG=$1
}

prompt_status() {
	prompt_segment black default
	pid=$$
	n=0
	while [[ ! -z $pid && $pid != 1 ]]; do
		[[ $(readlink /proc/$pid/exe) == $(realpath =$SHELL) ]] && (( n++ ))
		pid=$(echo -n $(ps -o ppid= -p $pid))
	done
	printf "%$((n-1))s" ""

	icons=()
	if [[ $RETVAL == 130 || $RETVAL == 131 ]]; then
		icons=($icons "%{%F{yellow}%}") # SIGINT and SIGQUIt
	elif [[ $RETVAL == 148 ]]; then
		icons=($icons "%{%F{blue}%}") # SIGTSTOP
	elif [[ $RETVAL != 0 ]]; then
		icons=($icons "%{%F{red}%}")
	fi
	[[ $(jobs -s | wc -l) -gt 0 ]] && icons=($icons "%{%F{cyan}%}") # Suspended jobs
	[[ $(jobs -r | wc -l) -gt 0 ]] && icons=($icons "%{%F{green}%}") # Running jobs
	# Possibly %{%F{yellow}%} for root
	echo -n ${(j. .)icons}
}

prompt_context() {
	prompt_segment $(print -P "%(!.yellow.green)") black
	echo -n "%n"
}

prompt_dir() {
	prompt_segment blue black
	echo -n '%~'
}

prompt_git() {
	{
		if git rev-parse --is-inside-work-tree >/dev/null; then
			prompt_segment $([[ -n $(git status --porcelain) ]] && echo -n yellow || echo green) black

			if git symbolic-ref HEAD >/dev/null; then
				echo -n " $(git symbolic-ref HEAD | sed s:refs/heads/::)"
			else
				echo -n "➦ $(git rev-parse --short HEAD)"
			fi

			local AHEAD=$(git log --oneline @{u}.. | wc -l)
			local BEHIND=$(git log --oneline ..@{u} | wc -l)
			if [[ $AHEAD -gt 0 || $BEHIND -gt 0 ]]; then
				echo -n " "
				[[ $AHEAD -gt 0 ]] && echo -n "↑$AHEAD"
				[[ $BEHIND -gt 0 ]] && echo -n "↓$BEHIND"
			fi
		fi
	} 2> /dev/null
}

prompt_time() {
	prompt_segment blue black
	if [[ $_SENDING == 1 ]]; then
		echo -n "%D{%H:%M:%S}"
	else
		echo -n "--:--:--"
	fi
}

build_prompt() {
	RETVAL=$?
	RIGHT=0
	prompt_status
	prompt_context
	prompt_dir
	prompt_git
	prompt_segment default default
}

build_rprompt() {
	RIGHT=1
	prompt_time
	echo -n "%{ %}"
}

setopt promptsubst
_PROMPT_RESET=$'%{\e[0m%}'
PROMPT=$_PROMPT_RESET'$(build_prompt)'
RPROMPT=$_PROMPT_RESET'$(build_rprompt)'

function _reset-prompt-and-accept-line {
	_SENDING=1
	zle reset-prompt
	_SENDING=0
	zle .accept-line
}
zle -N accept-line _reset-prompt-and-accept-line
