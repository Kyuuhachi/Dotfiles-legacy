#!/bin/zsh
CURRENT_BG=''
prompt_segment() {
	local bg fg
	[[ -n $1 ]] && bg="%K{$1}" || bg="%k"
	[[ -n $2 ]] && fg="%F{$2}" || fg="%f"
	if [[ -z $CURRENT_BG ]]; then
		echo -n "%{$bg$fg%} "
	else
		echo -n " %{$bg%F{$CURRENT_BG}%}%{$fg%} "
	fi
	CURRENT_BG=$1
	[[ -n $3 ]] && echo -n $3
}

prompt_status() {
	prompt_segment black default

	#Zsh nesting depth
	local d=0
	local pid=$PPID
	local exe=$(readlink -f $SHELL)
	local cmd
	while true; do
		cmd=$(readlink -f /proc/$pid/exe)
		[[ "$cmd" == "$exe" ]] || break
		((d++))
		pid=$(ps -o ppid h $pid | sed -r "s/^\s+//;s/\s+$//")
	done
	printf %${d}s ""

	#Various status symbols
	local symbols
	symbols=()
	[[ $RETVAL -ne 0 ]] && symbols+="%{%F{red}%}✘"
	[[ $UID -eq 0 ]] && symbols+="%{%F{yellow}%}⚡"
	[[ $(jobs -l | wc -l) -gt 0 ]] && symbols+="%{%F{cyan}%}⚙"
	echo -n "$symbols"
}

prompt_context() {
	prompt_segment $([[ $UID == 0 ]] && echo yellow || echo green) black "$USER"
}

prompt_dir() {
	prompt_segment blue black '%~'
}

prompt_git() {
	{
		if git rev-parse --is-inside-work-tree >/dev/null; then
			prompt_segment $([[ -n $(git status --porcelain) ]] && echo yellow || echo green) black

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

build_prompt() {
	RETVAL=$?
	prompt_status
	prompt_context
	prompt_dir
	prompt_git
	prompt_segment
}

setopt promptsubst
PROMPT='%{%f%b%k%}$(build_prompt)'
