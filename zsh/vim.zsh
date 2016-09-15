bindkey -d
bindkey -A viins main
KEYTIMEOUT=1

zle-line-init() {
	zle -K vicmd
}
zle -N zle-line-init

zle-keymap-select() {
	CURRENT_KEYMAP=$1
	zle reset-prompt
}
zle -N zle-keymap-select

ctrl-z() {
	[[ $(jobs | wc -l) > 0 ]] && {
		zle push-line
		BUFFER="fg"
		zle accept-line
	}
}
zle -N ctrl-z
bindkey -M vicmd "^Z" ctrl-z

expand-or-complete-with-dots() {
	print -Pn "%{%F{red}...%f%}" | nowrap
	zle expand-or-complete
	zle redisplay
}
zle -N expand-or-complete-with-dots
bindkey "^I" expand-or-complete-with-dots

nop() {}
zle -N nop
bindkey -M vicmd '\e' nop
bindkey -M vicmd ':' nop

bindkey -M vicmd -s "s" "xi"

bindkey -M vicmd "^[OA" up-line
bindkey -M vicmd "^[[A" up-line
bindkey -M vicmd "k" up-line
bindkey -M vicmd "^[OB" down-line
bindkey -M vicmd "^[[B" down-line
bindkey -M vicmd "j" down-line
bindkey -M vicmd "+" history-beginning-search-forward
bindkey -M vicmd "J" history-beginning-search-forward
bindkey -M vicmd "^[[6~" history-beginning-search-forward
bindkey -M vicmd -- "-" history-beginning-search-backward
bindkey -M vicmd "K" history-beginning-search-backward
bindkey -M vicmd "^[[5~" history-beginning-search-backward

bindkey -M viins '^J' vi-open-line-above
bindkey -M viins '^M' vi-open-line-below
bindkey -M viins "^[OA" up-line
bindkey -M viins "^[[A" up-line
bindkey -M viins "^[OB" down-line
bindkey -M viins "^[[B" down-line
bindkey -M viins "^H" backward-delete-char
bindkey -M viins "^?" backward-delete-char
bindkey -M viins "^[[3~" vi-delete-char
bindkey -M viins "^[[3~" vi-delete-char
