{ config, pkgs, ...}:
{ config = {
  home.packages = [ pkgs.zsh ];
  home.file.".zshrc".text = ''
    source ${./prompt.zsh}
    source ${./inp.zsh}
    source ${pkgs.zsh-fast-syntax-highlighting}/share/zsh/site-functions/fast-syntax-highlighting.plugin.zsh
    source ${pkgs.zsh-history-search-multi-word}/history-search-multi-word.plugin.zsh
    source ${./zshrc}
  '';
}; }
