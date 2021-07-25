export PATH="$HOME/dot/scripts:$HOME/.local/bin:${PATH+:}$PATH"
export PYTHONPATH="$HOME/dot/pylib${PYTHONPATH+:}$PYTHONPATH"
export PYTHONSTARTUP="$HOME/dot/__init__.py"
export PYTHONPYCACHEPREFIX=/tmp/__pycache__
export LANG="en_US.UTF-8"
export LC_TIME="C"
export LC_NUMERIC="C"
export EDITOR=nvim VISUAL=nvim PAGER=semete
export RIPGREP_CONFIG_PATH=$HOME/.ripgreprc

if [ -e /home/yuki/.nix-profile/etc/profile.d/nix.sh ]; then . /home/yuki/.nix-profile/etc/profile.d/nix.sh; fi # added by Nix installer
