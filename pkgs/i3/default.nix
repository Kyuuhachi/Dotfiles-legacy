{pkgs, ...}:
let
  inherit (pkgs) lib;

  parseKey = lib.replaceStrings ["c-" "s-" "w-" "a-"] ["Ctrl+" "Shift+" "Mod4+" "Mod1+"];
  keybindings = binds:
    lib.concatStringsSep "\n"
      (lib.mapAttrsToList (k: v: "bindsym ${parseKey k} \"${v}\"") binds);

  compose-py = pkgs.runCommand "compose.py" {} ''
    substitute ${./compose.py} $out \
      --replace '"dmenu"' '"${pkgs.dmenu}/bin/dmenu"' \
      --replace '"notify-send"' '"${pkgs.libnotify}/bin/notify-send"' \
  '';

  binds = {
    c-a-Backspace = "exit";
    w-z = "restart";
    w-x = "kill";

    w-f = "fullscreen"; w-s-f = "border toggle";
    w-a = "focus parent"; w-s-a = "focus child";
    w-space = "focus mode_toggle"; w-s-space = "floating toggle";
    w-c-space = "floating enable; resize set 1500 600; move position center";

    w-1 = "workspace 1";  w-s-1 = "move container to workspace 1; workspace 1";
    w-2 = "workspace 2";  w-s-2 = "move container to workspace 2; workspace 2";
    w-3 = "workspace 3";  w-s-3 = "move container to workspace 3; workspace 3";
    w-4 = "workspace 4";  w-s-4 = "move container to workspace 4; workspace 4";
    w-5 = "workspace 5";  w-s-5 = "move container to workspace 5; workspace 5";
    w-6 = "workspace 6";  w-s-6 = "move container to workspace 6; workspace 6";
    w-7 = "workspace 7";  w-s-7 = "move container to workspace 7; workspace 7";
    w-8 = "workspace 8";  w-s-8 = "move container to workspace 8; workspace 8";
    w-9 = "workspace 9";  w-s-9 = "move container to workspace 9; workspace 9";
    w-0 = "workspace 10"; w-s-0 = "move container to workspace 10; workspace 10";

    w-minus = "exec ${pkgs.python3.withPackages(p:[p.anyio p.simplei3])} ${./from_scratch.py}";
    w-s-minus = "move scratchpad";

    w-h = "focus left";  w-s-h = "move left";
    w-j = "focus down";  w-s-j = "move down";
    w-k = "focus up";    w-s-k = "move up";
    w-l = "focus right"; w-s-l = "move right";

    w-c-h = "resize shrink width  10 px"; w-c-s-h = "resize shrink width  1 px";
    w-c-j = "resize grow   height 10 px"; w-c-s-j = "resize grow   height 1 px";
    w-c-k = "resize shrink height 10 px"; w-c-s-k = "resize shrink height 1 px";
    w-c-l = "resize grow   width  10 px"; w-c-s-l = "resize grow   width  1 px";

    w-Return = "exec ${pkgs.i3}/bin/i3-sensible-terminal";
    w-d = "exec ${pkgs.dmenu}/bin/dmenu_run";
    Caps_Lock = "exec ${pkgs.python3.withPackages(p:[p.xlib])}/bin/python ${compose-py} ${../../compose.txt}";
  } // (let Maim = flags: "exec ${pkgs.maim}/bin/main ${flags} | ${pkgs.xclip}/bin/xclip -selection clipboard -t image/png"; in {
    Print   = Maim "--nokeyboard --nodecorations --select --hidecursor";
    s-Print = Maim "--nokeyboard";
    a-Print = Maim "--nokeyboard --nodecorations --window=$(${pkgs.xdotool}/bin/xdotool getactivewindow)";
  }) // {
    XF86_MonBrightnessUp = "${pkgs.brightnessctl}/bin/brightnessctl -e s 10%+";
    XF86_MonBrightnessDown = "${pkgs.brightnessctl}/bin/brightnessctl -e s 10%-";
  }; # volume

  i3-config = ''
    font pango:monospace 9.5

    floating_modifier Mod4
    floating_minimum_size 1 x 1
    floating_maximum_size -1 x -1
    focus_follows_mouse no
    workspace_auto_back_and_forth yes
    hide_edge_borders both
    workspace_layout tabbed
    focus_on_window_activation urgent

    for_window [class=".*"] title_format %title <span size="x-small" style="italic" weight="heavy">%class | %instance</span>

    set_from_resource $f1 i3.focused.bdr   #4c7899
    set_from_resource $f2 i3.focused.bg    #285577
    set_from_resource $f3 i3.focused.ind   #2e9ef4
    set_from_resource $i1 i3.ifocused.bdr  #333333
    set_from_resource $i2 i3.ifocused.bg   #5f676a
    set_from_resource $i3 i3.ifocused.ind  #484e50
    set_from_resource $u1 i3.unfocused.bdr #333333
    set_from_resource $u2 i3.unfocused.bg  #222222
    set_from_resource $u3 i3.unfocused.ind #292d2e
    set_from_resource $b1 i3.bar.bg        #232323
    set_from_resource $b2 i3.bar.text      #DCDCDC
    set_from_resource $b3 i3.bar.sep       #666666

    client.focused          $f1 $f2 #ffffff $f3 $f2
    client.focused_inactive $i1 $i2 #ffffff $i3 $i2
    client.unfocused        $u1 $u2 #888888 $u3 $u2

    bar {
      i3bar_command ${pkgs.icebar}/bin/icebar
      id icebar
      colors {
        background $b1
        statusline $b2
        separator  $b3
        focused_workspace  $f1 $f2 #ffffff
        active_workspace   $i1 $i2 #ffffff
        inactive_workspace $u1 $u2 #888888
      }
    }

    ${keybindings binds}
  '';

in { config = {
  home.packages = [
    pkgs.i3
    pkgs.icebar
  ];
  xsession.enable = true;
  xsession.windowManager.command = "${pkgs.i3}/bin/i3";
  xdg.configFile."i3/config".text = i3-config;

  xdg.configFile."icebar.py".source = ../icebar/config.py;
}; }
