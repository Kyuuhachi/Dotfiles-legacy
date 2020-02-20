#!/bin/zsh
CURRENT_BG="default"
prompt_segment() { # bg color, fg color
	local bg=$1 fg=$2
	if [[ $RIGHT != 1 ]]; then
		if [[ $CURRENT_BG == $bg ]]; then
			echo -n "%{%F{$fg}%}"
		elif [[ $CURRENT_BG == "default" ]]; then
			echo -n "%{%K{$bg}%F{$fg}%}"
		else
			echo -n "%{%K{$bg}%F{$CURRENT_BG}%}%{%F{$fg}%}"
		fi
	else
		if [[ $CURRENT_BG == $bg ]]; then
			echo -n "%{%F{$fg}%}"
		elif [[ $CURRENT_BG == "default" ]]; then
			echo -n "%{%F{$bg}%}%{%K{$bg}%F{$fg}%}"
		else
			echo -n "%{%F{$bg}%K{$CURRENT_BG}%}%{%K{$bg}%F{$fg}%}"
		fi
	fi
	CURRENT_BG=$1
}

prompt_status() {
	prompt_segment black default
	icons=()
	if   [[ $RETVAL == 130 || $RETVAL == 131 ]]; then icons=($icons "%{%F{yellow}%}") # SIGINT and SIGQUIT
	elif [[ $RETVAL == 148                   ]]; then icons=($icons "%{%F{blue}%}") # SIGTSTOP
	elif [[ $RETVAL != 0                     ]]; then icons=($icons "%{%F{red}%}")
	fi
	[[ $(jobs -s | wc -l) -gt 0 ]] && icons=($icons "%{%F{cyan}%}") # Suspended jobs
	[[ $(jobs -r | wc -l) -gt 0 ]] && icons=($icons "%{%F{green}%}") # Running jobs
	[[ $#icons -gt 0 ]] && echo -n " ${(j. .)icons}"
	echo -n " "
}

prompt_context() {
	prompt_segment $(print -P "%(!.yellow.green)") black
	echo -n " %n "
}

prompt_dir() {
	prompt_segment blue black
	echo -n " %~ "
}

prompt_git() {
	{
		if git rev-parse --is-inside-work-tree >/dev/null; then
			git status --ignore-submodules=dirty -z | grep -zq '^.\S'; local HAS_UNSTAGED=$?
			git status --ignore-submodules=dirty -z --untracked-files=no | grep -zq '^\S.'; local HAS_STAGED=$?
			prompt_segment $([[ $HAS_UNSTAGED == 0 || $HAS_STAGED == 0 ]] && echo yellow || echo green) black
			echo -n " "

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
			echo -n " "
			[[ $HAS_STAGED == 0 ]] && prompt_segment $([[ $HAS_UNSTAGED != 1 ]] && echo yellow || echo green) black
		fi
	} 2> /dev/null
}

prompt_time() {
	prompt_segment blue black
	if [[ $_SENDING == 1 ]]; then
		echo -n " %D{%H:%M:%S} "
	else
		echo -n " --:--:-- "
	fi
}

VIRTUAL_ENV_DISABLE_PROMPT=1
prompt_venv() {
	if (( ${+VIRTUAL_ENV} )); then
		prompt_segment 24 yellow
		echo -n "  $(realpath --relative-base=. $VIRTUAL_ENV) "
	fi
}

build_prompt() {
	RETVAL=$?
	RIGHT=0
	prompt_status
	prompt_venv
	prompt_context
	prompt_dir
	prompt_git
	prompt_segment default default
	echo -n " "
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
