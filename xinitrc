#!/bin/sh
export PATH="$HOME/dot/scripts:$HOME/bin:$HOME/.gem/ruby/2.4.0/bin:$PATH"
export LC_ALL="en_US.UTF-8"
export LC_TIME="C.UTF-8"
export LC_NUMERIC="C.UTF-8"

export GTK_IM_MODULE=ibus
export QT_IM_MODULE=ibus
export XMODIFIERS=@im=ibus

export MOZ_USE_XINPUT2=1
export MPD_HOST=~/.mpd/socket

export BROWSER=firefox
export EDITOR=nvim
export SHELL=zsh
export TERMINAL=x-terminal-emulator

export XDG_DESKTOP_DIR="$HOME"
export QT_QPA_PLATFORMTHEME=gtk2

xkbcomp ~/dot/c98.xkb $DISPLAY
xset -dpms s off
xrdb -load .Xresources
exec i3
