{
  inputs = {
    # Vim
    "PotatoesMaster/i3-vim-syntax"  = { url = "github:PotatoesMaster/i3-vim-syntax"; flake = false; };
    "neovimhaskell/haskell-vim"     = { url = "github:neovimhaskell/haskell-vim"; flake = false; };
    "tpope/vim-abolish"             = { url = "github:tpope/vim-abolish"; flake = false; };
    "tpope/vim-characterize"        = { url = "github:tpope/vim-characterize"; flake = false; };
    "vim-scripts/JavaScript-Indent" = { url = "github:vim-scripts/JavaScript-Indent"; flake = false; };

    # Zsh
    "zdharma/history-search-multi-word" = { url = "github:zdharma/history-search-multi-word"; flake = false; };
  };

  outputs = inputs@{ self, nixpkgs, ... }: let
    sys = "x86_64-linux";
    pkgs = import nixpkgs {
      system = sys;
      config.allowUnfreePredicate = pkg: builtins.elem (pkgs.lib.getName pkg) [ "tabnine" ];

      overlays = [myOverlay];
    };
    call = pkgs.lib.callPackageWith;
    callWithPy = call (pkgs // pkgs.python3Packages // myPkgs // myPkgs.python3Packages);

    myOverlay = final: prev: {
      dmenu = prev.dmenu.override {
        patches = [(pkgs.writeText "flush.patch" ''
          --- a/dmenu.c
          +++ b/dmenu.c
          @@ -467,2 +467,3 @@ insert:
           		puts((sel && !(ev->state & ShiftMask)) ? sel->text : text);
          +		fflush(stdout);
           		if (!(ev->state & ControlMask)) {
        '')];
      };
    };

    myPkgs = {
      vimPlugins = let
        plug = name: pkgs.vimUtils.buildVimPlugin { name = baseNameOf name; src = inputs.${name}.outPath; };
      in {
        i3-vim-syntax = plug "PotatoesMaster/i3-vim-syntax";
        haskell-vim = plug "neovimhaskell/haskell-vim";
        vim-abolish = plug "tpope/vim-abolish";
        vim-characterize = plug "tpope/vim-characterize";
        JavaScript-Indent = plug "vim-scripts/JavaScript-Indent";
      };

      nvim- = call pkgs ./nvim {
        vimPlugins = pkgs.vimPlugins // myPkgs.vimPlugins;
      };

      zsh- = call pkgs ./zsh {
        zsh-history-search-multi-word = inputs."zdharma/history-search-multi-word".outPath;
      };

      python3Packages = {
        addSetupPy =
          { src
          , _basename ? pkgs.lib.removeSuffix ".py" (baseNameOf src)
          , name ? _basename
          , version ? "0.0"
          , preConfigure ? ""
          , ...}@attrs: attrs // {
            inherit name version src;
            doCheck = false;
            unpackPhase = "cp ${src} $(stripHash ${src})";
            preConfigure = preConfigure + ''
              echo >setup.py '
              import setuptools
              setuptools.setup(name="${name}", version="${version}", py_modules=["${_basename}"])
              '
            '';
          };

        simplei3 = callWithPy ./simplei3.nix {};
        simplealsa = callWithPy ./simplealsa.nix {};
        icebar = callWithPy ./icebar {};
      };

      i3- = callWithPy ./i3 {};
    };
  in {
    packages.${sys} = myPkgs;
    overlay = myOverlay;
  };
}
