{ pkgs, config, lib, ... }:
{
  home.packages = [
    (pkgs.runCommand "x-terminal-emulator" {} ''
      mkdir -p $out/bin
      ln -s ${pkgs.mate.mate-terminal}/bin/mate-terminal $out/bin/x-terminal-emulator
    '')
  ];

  dconf.settings = {
    "org/mate/terminal/global" = {
      use-mnemonics = false;
      use-menu-acceleratiors = false;
      confirm-window-close = true;
    };

    "org/mate/terminal/profiles/default" = {
      background-color = "#002B36";
      foreground-color = "#839496";
      palette = "#2E3436:#DD2222:#4E9A06:#C4A000:#3068B0:#826387:#06989A:#D3D7CF:"
              + "#555555:#EF2929:#8AE234:#FCE94F:#729FCF:#AD7FA8:#34E2E2:#EEEEEC";
      background-darkness = 0.89;
      background-type = "transparent";
      use-theme-colors = false;

      default-show-menubar = false;
      scrollback-unlimited = true;
      title-mode = "ignore";
      word-chars = "-A-Za-z0-9,./?%&#_ = +@~";
    };
  };
}
