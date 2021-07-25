{ config, pkgs, lib, ...}:

let
  ls_colors = pkgs.runCommand "ls_colors" {} "${pkgs.python3}/bin/python ${./dircolors.py} < ${../../ls_colors} > $out";
  ls_colors_sh = lib.readFile (pkgs.runCommand "dircolors" {} "${pkgs.coreutils}/bin/dircolors -b ${ls_colors} > $out");

in {
  config.programs.bash.initExtra = ls_colors_sh;
  config.programs.zsh.initExtraBeforeCompInit = ls_colors_sh;
}
