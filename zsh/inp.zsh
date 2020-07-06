function ctrl-z() {
	[[ $(jobs | wc -l) > 0 ]] && {
		zle zle-line-finish
		zle -I
		fg
		zle zle-line-init
	}
}
zle -N ctrl-z

function expand-with-dots() {
	print -Pn "%{%F{red}...%f%}" | nowrap
	zle expand-word
	zle redisplay
}
zle -N expand-with-dots

function complete-with-dots() {
	print -Pn "%{%F{red}...%f%}" | nowrap
	zle complete-word
	zle redisplay
}
zle -N complete-with-dots

function nop() {}
zle -N nop

function addsub {
	local start=$((CURSOR+1))
	until [[ $BUFFER[$start] == [0-9] ]]; do
		((start++))
		[[ $BUFFER[$start] ]] || return
	done
	while [[ $BUFFER[$start] = [0-9] ]]; do
		((start--))
	done
	local len=1
	while [[ $BUFFER[$start+$len+1] = [0-9] ]]; do
		((len++))
	done
	local firstDigit=$BUFFER[$start+1]
	if [[ $BUFFER[$start] = '-' ]]; then
		((start--))
		((len++))
	fi

	local pre=${BUFFER:0:$start}
	local num=${BUFFER:$start:$len}
	local suf=${BUFFER:$start+$len}
	if [[ $WIDGET = "incarg" ]]; then
		local num2=$((num+${NUMERIC:-1}))
	else
		local num2=$((num-${NUMERIC:-1}))
	fi
	[[ $firstDigit = 0 ]] && num2=$(printf "%0${#num}d" $num2)
	BUFFER="$pre$num2$suf"
	CURSOR=$((start+len-1))
	zle redisplay
}
zle -N incarg addsub
zle -N decarg addsub

export KEYTIMEOUT=1

bindkey -e
bindkey "^[[2~"   overwrite-mode       # Insert
bindkey "^?"      backward-delete-char # Backspace
bindkey "^[^?"    backward-delete-word # A-Backspace
bindkey "^[[3~"   delete-char          # Delete
bindkey "^[[3;3~" delete-word          # A-Delete
bindkey "^[[A"    up-line-or-history   # Up
bindkey "^[[B"    down-line-or-history # Down
bindkey "^[[C"    forward-char         # Right
bindkey "^[[D"    backward-char        # Left
bindkey "^[[F"    end-of-line          # End
bindkey "^[[H"    beginning-of-line    # Home
bindkey "^[[5~"   nop                  # PgUp
bindkey "^[[6~"   nop                  # PgDn

bindkey "^[" vi-cmd-mode
bindkey "^Z" ctrl-z
bindkey "^@" expand-with-dots
bindkey "^I" complete-with-dots

bindkey -a "^[" vi-insert
bindkey -a "H"  vi-beginning-of-line
bindkey -a "L"  vi-end-of-line
bindkey -a "^A" incarg
bindkey -a "^X" decarg
bindkey -a "^Q" push-line
bindkey -a "^Z" ctrl-z

# autoload -Uz add-zle-hook-widget
# function set-cursor {
# 	if [[ $KEYMAP == main ]]; then
# 		echo -n $'\e[5 q'
# 	else
# 		echo -n $'\e[ q'
# 	fi
# }
# function reset-cursor {
# 	echo -n $'\e[ q'
# }
# add-zle-hook-widget line-init set-cursor
# add-zle-hook-widget keymap-select set-cursor
# add-zle-hook-widget line-finish reset-cursor

function zle-line-init {
	if [[ $KEYMAP == main ]]; then
		echo -n $'\e[5 q'
	else
		echo -n $'\e[ q'
	fi
}
function zle-line-finish {
	echo -n $'\e[ q'
}
zle -N zle-line-init
zle -N zle-keymap-select zle-line-init
zle -N zle-line-finish

__fsel() {
	unset REPORTTIME
	setopt localoptions pipefail no_aliases 2> /dev/null
	find * -type f,l | cf | \
		fzf --no-mouse --ansi --multi --height=$((LINES-1)) --preview='view {}' | \
		while read f; do printf "%q " $f; done
}

fzf-file-widget() {
	LBUFFER="${LBUFFER}$(__fsel)"
	local ret=$?
	zle reset-prompt
	return $ret
}
zle -N fzf-file-widget
bindkey '^F' fzf-file-widget
