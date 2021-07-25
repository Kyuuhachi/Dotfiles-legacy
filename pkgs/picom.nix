{ pkgs, config, lib, ...}:

let
  configFile = pkgs.writeText "picom.conf" ''
    backend = "glx"
    vsync = true

    glx-copy-from-front = false
    glx-no-rebind-pixmap = true
    use-damage = true

    refresh-rate = 0
    unredir-if-possible = true

    mark-wmwin-focused = true
    mark-ovredir-focused = true
    use-ewmh-active-win = true
    detect-transient = true
    # detect-client-leader = true

    opacity-rule = [
      "0:_NET_WM_STATE@:32a *= '_NET_WM_STATE_HIDDEN'"
      # "99.99:_NET_WM_STATE@:32a *= '_NET_WM_STATE_FULLSCREEN'",
      # "99.99:"
    ];

    inactive-dim = 0.4
    inactive-dim-fixed = true
  '';

in {
  systemd.user.services.picom = {
    Unit = {
      Description = "Picom X11 compositor";
      After = ["graphical-session-pre.target"];
      PartOf = ["graphical-session.target"];
    };

    Install = {
      WantedBy = ["graphical-session.target"];
    };

    Service = {
      ExecStart = "${pkgs.picom}/bin/picom --config ${configFile}";
      Restart = "always";
      RestartSec = 3;
    };
  };
}
