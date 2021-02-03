{ config, pkgs, ...}:
let
  mkNvim = pkgs.callPackage ./lib.nix {};

  plugins = with pkgs.vimPlugins; [
    # General
    vim-textobj-user
    vim-abolish
    vim-characterize
    vim-commentary
    vim-repeat
    vim-surround
    targets-vim
    vim-airline
    vim-easy-align
    undotree
    fzf-vim

    # Multiple languages
    ale
    deoplete-nvim
    neco-syntax
    vim-polyglot

    # Specific languages
    [vimtex {for = ["tex" "sty"];}]
    i3-vim-syntax
    [haskell-vim {for = "haskell";}]
    [JavaScript-Indent {for = ["javascript" "jsx"];}]
    [deoplete-zsh {for = "zsh";}]
    [neco-vim {for = "vim";}]
    [deoplete-jedi {for = "python";}]
    semshi

    # Custom
    ./98color
    ./98fuzz
    [./98lilypond {for = "lilypond";}] # TODO these two have custom build scripts
    [./98lua {for = "lua";}]
    ./98motion
    [./98python {for = "python";}]
    ./98tabbar
  ];

  nvim = mkNvim pkgs.neovim-unwrapped {
    inherit plugins;
    extraPython3Packages = ps: [ps.jedi ps.python-ly];
    rc = "source ${./init.vim}";
  };

in { config = {
  home.packages = [ nvim pkgs.fzf ]; # XXX remove fzf as soon as I figure out how
  home.sessionVariables.EDITOR = "nvim"; # Can't give an absolute path or I'll have to relog to have the config update
}; }
