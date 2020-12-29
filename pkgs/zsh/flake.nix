{
  description = "Zsh with my config and custom plugins";

  inputs = {
    "zdharma/history-search-multi-word"  = { url = "github:zdharma/history-search-multi-word"; flake = false; };
  };

  outputs = inputs@{ self, nixpkgs, ... }: let
    sys = "x86_64-linux";
    pkgs = import nixpkgs { system = sys; };
    zshrc = pkgs.writeText "zshrc" ''
      source ${./prompt.zsh}
      source ${./inp.zsh}
      source ${pkgs.zsh-fast-syntax-highlighting}/share/zsh/site-functions/fast-syntax-highlighting.plugin.zsh
      source ${inputs."zdharma/history-search-multi-word".outPath}/history-search-multi-word.plugin.zsh
      source ${./zshrc}
    '';
  in {
    packages.${sys}.zsh = pkgs.symlinkJoin {
      name = "zsh";
      paths = [];
      buildInputs = [ pkgs.zsh pkgs.makeWrapper ];
      postBuild = ''
        mkdir $out/bin
        makeWrapper ${pkgs.zsh}/bin/zsh $out/bin/zsh --set ZDOTDIR $out
        cp ${zshrc} $out/.zshrc
      '';
    };
    defaultPackage.${sys} = self.packages.${sys}.zsh;
  };
}
