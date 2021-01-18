{ neovim-unwrapped
, tabnine
, writeText
, vimPlugins
, pkgs}:

let
  mkNvim = pkgs.callPackage ./lib.nix {};

  plugins = with vimPlugins; [
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
    (deoplete-tabnine.overrideAttrs (old: {
      patches = [(writeText "tabnine.patch" ''
        --- a/rplugin/python3/deoplete/sources/tabnine.py
        +++ b/rplugin/python3/deoplete/sources/tabnine.py
        @@ -178,2 +178,1 @@
        -        binary_dir = os.path.join(self._install_dir, 'binaries')
        -        path = get_tabnine_path(binary_dir)
        +        path = '${tabnine}/bin/TabNine'
        @@ -187,1 +186,1 @@
        -                '--log-file-path', os.path.join(self._install_dir, 'tabnine.log'),
        +                '--log-file-path', '/tmp/tabnine.log',
      '')];
    }))

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
in
  mkNvim neovim-unwrapped {
    inherit plugins;
    extraPython3Packages = ps: [ps.jedi ps.python-ly];
    rc = "source ${./init.vim}";
  }
