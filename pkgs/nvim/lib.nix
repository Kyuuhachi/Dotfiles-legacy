{ pkgs, inputs ? {} }:
let lib = pkgs.stdenv.lib; in
rec {
	toVimL = x:
		     if builtins.isString x then "'${lib.replaceStrings [ "\n" "'" ] [ "\n\\ " "''" ] x}'"
		else if builtins.isAttrs x && x ? out then toVimL x.out # a derivation
		else if builtins.isAttrs x then "{${lib.concatStringsSep ", " (lib.mapAttrsToList (n: v: "${toVimL n}: ${toVimL v}") x)}}"
		else if builtins.isList x then "[${lib.concatMapStringsSep ", " toVimL x}]"
		else if builtins.isInt x || builtins.isFloat x then builtins.toString x
		else if builtins.isBool x then (if x then "v:true" else "v:false")
		else throw "turning ${lib.generators.toPretty {} x} into a VimL thing not implemented yet";

	transitiveClosure = plugin:
		[ plugin ] ++ (
			lib.unique (builtins.concatLists (map transitiveClosure plugin.dependencies or []))
		);

	findDependenciesRecursively = plugins: lib.concatMap transitiveClosure plugins;

	makeNeovimConfig = args@{
		withPython2 ? false, extraPython2Packages ? (_: []),
		withPython3 ? true, extraPython3Packages ? (_: []),
		withNodeJs ? false, withRuby ? true,
		plugins ? [],
		...
	}: let
		getDeps = attrname: map (plugin: plugin.${attrname} or (_: []));

		python2Env = pkgs.pythonPackages.python.withPackages (ps:
			[ ps.pynvim ]
			++ extraPython2Packages ps
			++ lib.concatMap (f: f ps) (getDeps "pythonDependencies" plugins));

		python3Env = pkgs.python3Packages.python.withPackages (ps:
			[ ps.pynvim ]
			++ extraPython3Packages ps
			++ lib.concatMap (f: f ps) (getDeps "python3Dependencies" plugins));

		rubyEnv = pkgs.bundlerEnv {
			name = "neovim-ruby-env";
			gemdir = "${inputs.nixpkgs.outPath}/pkgs/applications/editors/neovim/ruby_provider";
			postBuild = ''
				ln -sf ${pkgs.ruby}/bin/* $out/bin
			'';
		};

		hostprog_check_table = {
			python = withPython2;
			python3 = withPython3;
			ruby = withRuby;
			node = withNodeJs;
		};

		binPath = lib.makeBinPath (
			lib.optionals withRuby [ rubyEnv ]
			++ lib.optionals withNodeJs [ pkgs.nodejs ]
		);

		flags = lib.concatLists (lib.mapAttrsToList (
			prog: withProg:
				if withProg then
					["--cmd" "let g:${prog}_host_prog='${placeholder "out"}/bin/nvim-${prog}'"]
				else
					["--cmd" "let g:loaded_${prog}_provider=1"]
		) hostprog_check_table);

		wrapperArgs =
			[ "--argv0" "$0" "--add-flags" (lib.escapeShellArgs flags) ]
			++ lib.optionals withRuby [ "--set" "GEM_HOME" "${rubyEnv}/${rubyEnv.ruby.gemPath}" ]
			++ lib.optionals (binPath != "") [ "--suffix" "PATH" ":" binPath ];
	in
		args // {
			inherit wrapperArgs;
			inherit python2Env;
			inherit python3Env;
			inherit rubyEnv;
			inherit withNodeJs;
		};

	Plug = x: let
		rtpOf = x: if x ? rtp then x.rtp else
			(pkgs.vimUtils.buildVimPlugin {
				name = baseNameOf x;
				src = if builtins.isString x then inputs.${x} else x;
			}).rtp;
		dat = (if builtins.isList x
			then { rtp = lib.elemAt x 0; conf = lib.elemAt x 1; }
			else { rtp = x; conf = {}; }
		);
	in
		"Plug ${toVimL (rtpOf dat.rtp)}, ${toVimL (dat.conf // {frozen = true;})}";

	PlugAll = plugins: ''
		source ${pkgs.vimPlugins.vim-plug.rtp}/plug.vim
		call plug#begin('/dev/null')
		${lib.concatMapStrings (p: "${Plug p}\n") (findDependenciesRecursively plugins)}
		call plug#end()
	'';

	# The builtin wrapNeovim doesn't understand my custom plugin manager
	mkNvim = unwrapped: args@{
		# A list, where each item is either a list of a plugin and a config, or
		# just a plugin, in which case the config is set to {}.
		# The plugins can be:
		# • a derivation
		# • a string, which is then looked up in `inputs`
		# • a path
		plugins ? [],
		# A string that is inserted into the init.vim. It should call the
		# `DoPlug()` function.
		rc ? "",
		extraMakeWrapperArgs ? "",
		...
	}: let
		res = makeNeovimConfig (builtins.removeAttrs args ["rc"]);
		allPlugins = PlugAll plugins;
		init-vim = ''
			function DoPlug()
				${allPlugins}
			endfunction
			echo 'asdf'
			${rc}
			delf DoPlug
		'';
	in
		pkgs.wrapNeovimUnstable unwrapped (res // {
			wrapperArgs = lib.escapeShellArgs (
				res.wrapperArgs ++ [
					"--add-flags" "-u ${pkgs.writeText "init.vim" init-vim}"
					# "--set" "NVIM_RPLUGIN_MANIFEST" "/dev/null"
				]
			) + " ${extraMakeWrapperArgs}";
			manifestRc = allPlugins;
		});
}
