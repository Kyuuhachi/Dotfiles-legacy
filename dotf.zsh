#!/usr/bin/zsh
cd $(dirname $0)

case $1 in 
	link)
		apply() {
			ln -s $2 $1
		} ;;
	remove)
		apply() {
			rm -r $1
		} ;;
	create)
		apply() {
			mv $1 $2
			ln -s $2 $1
		} ;;
	*)
		echo "Invalid command. Only link|remove|create are supported."
		exit 1
		;;
esac

apply ~/.zshrc zshrc
apply ~/.i3blocks.conf i3blocks.conf
apply ~/.i3/config i3config.conf
