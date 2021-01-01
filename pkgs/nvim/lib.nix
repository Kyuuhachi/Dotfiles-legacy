{ lib, writeText, symlinkJoin, makeWrapper
, python3, vimUtils, vimPlugins
}: let
  toVimL = x:
         if builtins.isString x then "'${lib.replaceStrings [ "\n" "'" ] [ "\n\\ " "''" ] x}'"
    else if builtins.isAttrs x && x ? out then toVimL x.out # a derivation
    else if builtins.isAttrs x then "{${lib.concatStringsSep ", " (lib.mapAttrsToList (n: v: "${toVimL n}: ${toVimL v}") x)}}"
    else if builtins.isList x then "[${lib.concatMapStringsSep ", " toVimL x}]"
    else if builtins.isInt x || builtins.isFloat x then builtins.toString x
    else if builtins.isBool x then (if x then "v:true" else "v:false")
    else throw "turning ${lib.generators.toPretty {} x} into a VimL thing not implemented yet";

  transitiveClosure = plugin: [ plugin ]
    ++ (lib.concatMap transitiveClosure plugin.dependencies or []);

  findDependenciesRecursively = plugins: lib.unique (lib.concatMap transitiveClosure plugins);

  getDeps = attrname: map (plugin: plugin.${attrname} or (_: []));

  Plug = x: let
    rtpOf = x: if x ? rtp then x.rtp else
      (vimUtils.buildVimPlugin rec {
        name = if lib.isStorePath x then "source" else baseNameOf x;
        src = x;
      }).rtp;
    dat = (if builtins.isList x
      then { rtp = lib.elemAt x 0; conf = lib.elemAt x 1; }
      else { rtp = x; conf = {}; }
    );
  in
    "  Plug ${toVimL (rtpOf dat.rtp)}, ${toVimL (dat.conf // {frozen = true;})}";

  PlugAll = plugins: ''
    source ${vimPlugins.vim-plug.rtp}/plug.vim
    call plug#begin('/dev/null')
    ${lib.concatMapStringsSep "\n" (p: "${Plug p}") plugins}
    call plug#end()'';

in unwrapped: {
  # A list, where each item is either a list of a plugin and a config, or
  # just a plugin, in which case the config is set to {}. The plugins can
  # be either derivations or paths.
  plugins ? [],
  # A string that is inserted into the init.vim. It should call the
  # `DoPlug()` function.
  rc ? "",

  extraPython3Packages ? (_: []),
}: let
  recplugins = findDependenciesRecursively plugins;

  init-vim = ''
    function DoPlug()
    ${PlugAll recplugins}
    endfunction
    ${rc}
    delf DoPlug
  '';

  python3Env = python3.withPackages (ps:
    [ ps.pynvim ]
    ++ extraPython3Packages ps
    ++ lib.concatMap (f: f ps) (getDeps "python3Dependencies" recplugins));

  wrapperArgs = lib.escapeShellArgs [
    "--argv0" "$0"
    "--add-flags"
    (lib.escapeShellArgs [
      "-u" (writeText "init.vim" init-vim)
      "--cmd" "let g:python3_host_prog='${python3Env}/bin/python3'"
      "--cmd" "let g:loaded_python_provider=1"
      "--cmd" "let g:loaded_node_provider=1"
      "--cmd" "let g:loaded_ruby_provider=1"
    ])
  ];
in
  symlinkJoin {
    name = "nvim-${lib.getVersion unwrapped}";
    paths = [];
    postBuild = ''
      makeWrapper ${unwrapped}/bin/nvim ./nvim-wrapper \
        --set NVIM_SYSTEM_RPLUGIN_MANIFEST /dev/null \
        --set NVIM_RPLUGIN_MANIFEST $out/rplugin.vim \
        --set HOME $PWD \
        ${wrapperArgs}

      if ! ./nvim-wrapper -i NONE -n -E -V1rplugins.log -s \
          +UpdateRemotePlugins +quit! > outfile 2>&1
      then
        cat outfile
        echo -e "\nGenerating rplugin.vim failed!"
        exit 1
      fi
      rm ./nvim-wrapper

      mkdir $out/bin
      makeWrapper ${unwrapped}/bin/nvim $out/bin/nvim \
        --set NVIM_SYSTEM_RPLUGIN_MANIFEST $out/rplugin.vim \
        --set NVIM_RPLUGIN_MANIFEST /dev/null \
        ${wrapperArgs}
    '';

    buildInputs = [ makeWrapper ];
    passthru = { inherit unwrapped; };

    preferLocalBuild = true;
    meta = unwrapped.meta // {
      hydraPlatforms = [];
      priority = (unwrapped.meta.priority or 0) - 1;
    };
  }
