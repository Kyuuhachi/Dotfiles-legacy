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

	#Zsh nesting depth
	local pid=$PPID
	local exe=$(readlink -f $SHELL)
	while [[ $pid != 0 ]]; do
		[[ "$(readlink -f /proc/$pid/exe)" == "$exe" ]] && echo -n " "
		pid=$(ps -o ppid h $pid | sed -r "s/^\s+//;s/\s+$//")
	done

	#Various status symbols
	local symbols
	symbols=()
	[[ $RETVAL -ne 0 ]] && symbols+="%{%F{red}%}✘"
	[[ $UID -eq 0 ]] && symbols+="%{%F{yellow}%}⚡"
	[[ $(jobs -l | wc -l) -gt 0 ]] && symbols+="%{%F{cyan}%}⚙"
	echo -n "$symbols"
}

prompt_context() {
	prompt_segment $([[ $UID == 0 ]] && echo yellow || echo green) black
	echo -n "$USER"
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
PROMPT='%{%f%b%k%}$(build_prompt)'
RPROMPT='%{%f%b%k%}$(build_rprompt)'

function _reset-prompt-and-accept-line {
	_SENDING=1
	zle reset-prompt
	_SENDING=0
	zle .accept-line
}
zle -N accept-line _reset-prompt-and-accept-line
