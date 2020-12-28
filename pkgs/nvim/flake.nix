{
	description = "Neovim with my config and custom plugins";

	inputs = {
		"PotatoesMaster/i3-vim-syntax"  = { url = "github:PotatoesMaster/i3-vim-syntax"; flake = false; };
		"neovimhaskell/haskell-vim"     = { url = "github:neovimhaskell/haskell-vim"; flake = false; };
		"tpope/vim-abolish"             = { url = "github:tpope/vim-abolish"; flake = false; };
		"tpope/vim-characterize"        = { url = "github:tpope/vim-characterize"; flake = false; };
		"vim-scripts/JavaScript-Indent" = { url = "github:vim-scripts/JavaScript-Indent"; flake = false; };
	};

	outputs = inputs@{ self, nixpkgs, ... }: let
		sys = "x86_64-linux";
		pkgs = import nixpkgs {
			system = sys;
			config.allowUnfreePredicate = pkg: builtins.elem (pkgs.lib.getName pkg) [ "tabnine" ];
		};
		mkNvim = pkgs.callPackage ./lib.nix {};

		plugins = with pkgs.vimPlugins; [
			# General
			vim-textobj-user
			inputs."tpope/vim-abolish".outPath
			inputs."tpope/vim-characterize".outPath
			commentary
			repeat
			surround
			targets-vim
			airline
			easy-align
			undotree
			fzf-vim

			# Multiple languages
			ale
			deoplete-nvim
			neco-syntax
			polyglot
			(deoplete-tabnine.overrideAttrs (old: {
				patches = [(pkgs.writeText "tabnine.patch" ''
--- a/rplugin/python3/deoplete/sources/tabnine.py
+++ b/rplugin/python3/deoplete/sources/tabnine.py
@@ -178,2 +178,1 @@
-        binary_dir = os.path.join(self._install_dir, 'binaries')
-        path = get_tabnine_path(binary_dir)
+        path = '${pkgs.tabnine}/bin/TabNine'
@@ -187,1 +186,1 @@
-                '--log-file-path', os.path.join(self._install_dir, 'tabnine.log'),
+                '--log-file-path', '/tmp/tabnine.log',
				'')];
			}))

			# Specific languages
			[vimtex {for = ["tex" "sty"];}]
			inputs."PotatoesMaster/i3-vim-syntax".outPath
			[inputs."neovimhaskell/haskell-vim".outPath {for = "haskell";}]
			[inputs."vim-scripts/JavaScript-Indent".outPath {for = ["javascript" "jsx"];}]
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
	in {
		packages.${sys}.nvim = mkNvim pkgs.neovim-unwrapped {
			inherit plugins;
			extraPython3Packages = ps: [ps.jedi ps.python-ly];
			rc = "source ${./init.vim}";
		};
		defaultPackage.${sys} = self.packages.${sys}.nvim;
	};
}
