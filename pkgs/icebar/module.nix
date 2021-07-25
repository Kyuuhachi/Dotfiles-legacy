{ pkgs, lib, config, ...}:

{
  options.programs.icebar = {
    enable = lib.mkEnableOption "Icebar";

    height = lib.mkOption {
      default = 21;
      type = lib.types.int;
    };

    css = lib.mkOption {
      default = ''
        #fg { font-family: monospace; }
      '';
      type = lib.types.str;
    };

    widgets.left = lib.mkOption {
      default = [
        "Clock()"
        "Battery('/sys/class/power_supply/BAT0', verbose=2)"
        "Wifi()"
        "Disk('/')"
        "RAM()"
        "CPUGraph()"
      ];
    };

    widgets.right = lib.mkOption {
      default = [
        "Workspaces(i3())"
        "Battery('/sys/class/power_supply/BAT0', verbose=2)"
        "Wifi()"
        "Disk('/')"
        "RAM()"
        "CPUGraph()"
      ];
    };

  };
}
