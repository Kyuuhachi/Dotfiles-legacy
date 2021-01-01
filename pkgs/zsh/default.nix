{ writeText, makeWrapper, symlinkJoin
, zsh-fast-syntax-highlighting
, zsh-history-search-multi-word
, zsh,
}: let
  zshrc = writeText "zshrc" ''
    source ${./prompt.zsh}
    source ${./inp.zsh}
    source ${zsh-fast-syntax-highlighting}/share/zsh/site-functions/fast-syntax-highlighting.plugin.zsh
    source ${zsh-history-search-multi-word}/history-search-multi-word.plugin.zsh
    source ${./zshrc}
  '';
in
  symlinkJoin {
    name = "zsh";
    paths = [];
    buildInputs = [ zsh makeWrapper ];
    postBuild = ''
      mkdir $out/bin
      makeWrapper ${zsh}/bin/zsh $out/bin/zsh --set ZDOTDIR $out
      cp ${zshrc} $out/.zshrc
    '';
  }
