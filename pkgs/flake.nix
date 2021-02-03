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

    home-manager = {
      url = "github:nix-community/home-manager";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = inputs@{ self, nixpkgs, home-manager, ... }: let
    sys = "x86_64-linux";
    pkgs = import nixpkgs {
      system = sys;
      config.allowUnfreePredicate = pkg: builtins.elem (pkgs.lib.getName pkg) [ "tabnine" ];
      config.allowAliases = false;

      overlays = [self.overlay];
    };

    myPkgs = {
      nvim- = pkgs.callPackage ./nvim {};

      zsh- = pkgs.callPackage ./zsh {
        zsh-history-search-multi-word = inputs."zdharma/history-search-multi-word".outPath;
      };

      inherit (pkgs) icebar;

      home-Sapphirl = (home-manager.lib.homeManagerConfiguration {
        username = "98";
        homeDirectory = "/home";
        system = sys;

        configuration = {
          nixpkgs.overlays = [self.overlay];

          imports = [
            ./i3
          ];

          home.packages = [
            myPkgs.nvim-
            myPkgs.zsh-
            pkgs.tree
            pkgs.ripgrep

            (pkgs.runCommand "x-terminal-emulator" {} ''mkdir -p $out/bin; ln -s ${pkgs.mate.mate-terminal}/bin/mate-terminal $out/bin/x-terminal-emulator'')
          ];

          sessionVariables.EDITOR = "${myPkgs.nvim-}/bin/nvim";

          home.stateVersion = "21.03";
        };
      }).activationPackage;
    };

  in {
    packages.${sys} = myPkgs;
    overlay = final: prev: {

      # Make dmenu flush properly
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

      python3 = prev.python3.override {
        packageOverrides = pfinal: pprev: {
          addSetupPy = final.callPackage ./addSetupPy.nix {};
          simplei3 = pfinal.callPackage ./simplei3.nix {};
          simplealsa = pfinal.callPackage ./simplealsa.nix {};
          icebar = pfinal.callPackage ./icebar {};
        };
      };

      vimPlugins = let
        plug = name: pkgs.vimUtils.buildVimPlugin { name = baseNameOf name; src = inputs.${name}.outPath; };
      in prev.vimPlugins // {
        i3-vim-syntax = plug "PotatoesMaster/i3-vim-syntax";
        haskell-vim = plug "neovimhaskell/haskell-vim";
        vim-abolish = plug "tpope/vim-abolish";
        vim-characterize = plug "tpope/vim-characterize";
        JavaScript-Indent = plug "vim-scripts/JavaScript-Indent";
      };

      inherit (final.python3.pkgs) icebar;

    };
  };
}
