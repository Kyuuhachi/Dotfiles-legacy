#!/bin/sh

source ~/.profile

export GTK_IM_MODULE=ibus
export QT_IM_MODULE=ibus
export XMODIFIERS=@im=ibus

export MOZ_USE_XINPUT2=1

export QT_QPA_PLATFORMTHEME=gtk2

systemctl --user import-environment DISPLAY XAUTHORITY
dbus-update-activation-environment DISPLAY XAUTHORITY

xkbcomp ~/dot/c98.xkb $DISPLAY
xset -dpms s off
xrdb -load .Xresources

ibus-daemon &
compton --config ~/dot/compton.conf &
unclutter --timeout 2.5 &

firefox &
discord &
python dot/oshirase/oshirase.py &

exec ${1:-i3}
