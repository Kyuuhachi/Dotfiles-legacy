# History
setopt histignorealldups sharehistory
HISTSIZE=1000
SAVEHIST=1000
HISTFILE=~/.zsh_history

#Utils
autoload -Uz compinit && compinit
autoload -Uz colors && colors
autoload -U zmv

#Variables
win=/media/caagr98/OSDisk/Users/admusr
: ~win
s=car0b1nius@muncher.se
alias su="sudo $SHELL"

path=(~/bin $path)

#Sub-rcs
for f in ~/.zsh/*.zsh; do
	source $f
done
