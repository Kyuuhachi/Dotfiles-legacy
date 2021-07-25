{ pkgs, config, lib, ... }:
{
  imports = [
    ./i3
    ./zsh
    ./nvim
    ./dircolors
    ./mate-terminal.nix
    ./picom.nix
  ];

  home.packages = [
    pkgs.tree
    pkgs.ripgrep
    pkgs.file
    pkgs.htop

    (pkgs.python3.withPackages (p: [p.numpy]))

    (pkgs.runCommand "aliases" {} ''mkdir -p $out/bin; ln -s ${pkgs.zsh}/bin/zsh $out/bin/.shell'')
  ];

  dconf.enable = true;
  dconf.settings = {
    "org/gtk/settings/debug" = {
      enable-inspector-keybinding = true;
      inspector-warning = false;
    };

    "org/gnome/evince/default" = {
      continuous = true;
      zoom = 1;
      sidebar-page = "outline";
    };
  };

  home.sessionVariables.PYTHONPYCACHEPREFIX = "/tmp/__pycache__";

  home.stateVersion = "21.03";
}
