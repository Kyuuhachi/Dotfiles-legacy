#!/usr/bin/zsh
cd $(dirname $0)

case $1 in #$1: real location, $2: ~/dot/ location
	link) #Creates a link
		func() {
			rm $1
			ln -s $2 $1
		} ;;
	remove) #Removes the real one (not sure why you'd do that)
		func() {
			rm $1
		} ;;
	create) #Moves the real config to ~/dot/
		func() {
			if [[ ! -e $2 ]]; then
				mv $1 $2
				ln -s $2 $1
			fi
		} ;;
	*)
		echo "Invalid command. Only link|remove|create are supported."
		exit 1
		;;
esac

abspath() {
	local ans=$(cd $(dirname $1) && pwd)/$(basename $1)
	echo ${ans%/}
}

apply() {
	echo $1
	func $(abspath $1) $(abspath $2)
}

apply ~/.zshrc zsh/zshrc
apply ~/.i3blocks.conf i3blocks.conf
apply ~/.i3/config i3config.conf
apply ~/.config/nvim nvim
apply ~/scripts scripts
