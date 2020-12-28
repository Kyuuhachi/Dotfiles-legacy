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
			config.allowUnfreePredicate = pkg: builtins.elem (pkgs.lib.getName pkg) [
				"tabnine"
			];
		};
		vimlib = import ./lib.nix {inherit pkgs inputs;};

		plugins = with pkgs.vimPlugins; [
			# General
			vim-textobj-user
			"tpope/vim-abolish"
			"tpope/vim-characterize"
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
				patches = [(pkgs.writeTextFile {
					name = "tabnine.patch";
					text = ''
--- a/rplugin/python3/deoplete/sources/tabnine.py
+++ b/rplugin/python3/deoplete/sources/tabnine.py
@@ -178,2 +178,1 @@
-        binary_dir = os.path.join(self._install_dir, 'binaries')
-        path = get_tabnine_path(binary_dir)
+        path = '${pkgs.tabnine}/bin/TabNine'
@@ -187,1 +186,1 @@
-                '--log-file-path', os.path.join(self._install_dir, 'tabnine.log'),
+                '--log-file-path', '/tmp/tabnine.log',
					'';
				})];
			}))

			# Specific languages
			[vimtex {for = ["tex" "sty"];}]
			"PotatoesMaster/i3-vim-syntax"
			["neovimhaskell/haskell-vim" {for = "haskell";}]
			["vim-scripts/JavaScript-Indent" {for = ["javascript" "jsx"];}]
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
		packages.${sys}.nvim = vimlib.mkNvim pkgs.neovim-unwrapped {
			inherit plugins;
			extraPython3Packages = ps: [ps.jedi];
			# configure.plug.plugins = with pkgs.vimPlugins; [ deoplete-nvim ];
			rc = "source ${./init.vim}";
			withRuby = false;
		};
		defaultPackage.${sys} = self.packages.${sys}.nvim;
	};
}
