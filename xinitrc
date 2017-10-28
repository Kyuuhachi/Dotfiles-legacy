#!/bin/sh
export PATH="$HOME/dot/scripts:$HOME/.local/bin:$PATH"
export LANG="en_US.UTF-8"
export LC_TIME="C"
export LC_NUMERIC="C"

export GTK_IM_MODULE=ibus
export QT_IM_MODULE=ibus
export XMODIFIERS=@im=ibus

export MOZ_USE_XINPUT2=1
export MPD_HOST=~/.mpd/socket

export QT_QPA_PLATFORMTHEME=gtk2
export GTK_CSD=0
export LD_PRELOAD=/usr/lib/libgtk3-nocsd.so.0
export GTK_OVERLAY_SCROLLING=0

xkbcomp ~/dot/c98.xkb $DISPLAY
xset -dpms s off
xrdb -load .Xresources
compton --config ~/dot/compton.conf &
pgrep mpd &>/dev/null || mpd --no-daemon &
while /usr/local/libexec/mate-notification-daemon; do true; done &
ibus-daemon &
exec ${1:-i3}
