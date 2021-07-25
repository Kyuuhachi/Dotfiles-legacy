{ config, pkgs, ...}:
{ config.programs.zsh = {
  enable = true;
  initExtra = ''
    unset __HM_SESS_VARS_SOURCED # Why does this exist in the first place?

    source ${./prompt.zsh}
    source ${./inp.zsh}
    source ${pkgs.zsh-fast-syntax-highlighting}/share/zsh/site-functions/fast-syntax-highlighting.plugin.zsh
    source ${pkgs.zsh-history-search-multi-word}/history-search-multi-word.plugin.zsh
    source ${./zshrc}
  '';
}; }
