{ pkgs, config, lib, ... }:
{
  imports = [
    ./i3
    ./zsh
    ./nvim
  ];

  home.packages = [
    pkgs.tree
    pkgs.ripgrep
    pkgs.file
    pkgs.htop

    (pkgs.python3.withPackages (p: [p.numpy]))

    (pkgs.runCommand "aliases" {} ''
      mkdir -p $out/bin
      ln -s ${pkgs.mate.mate-terminal}/bin/mate-terminal $out/bin/x-terminal-emulator
      ln -s ${pkgs.zsh}/bin/zsh $out/bin/.shell
      '')
  ];

  home.sessionVariables.PYTHONPYCACHEPREFIX = "/tmp/__pycache__";

  home.stateVersion = "21.03";
}
