{ buildPythonApplication
, gobject-introspection, wrapGAppsHook, gtk3, ibus
, lm_sensors
, pygobject3, xlib, appdirs, psutil
, simplei3, simplealsa
}:

buildPythonApplication rec {
  name = "icebar";
  version = "1.0";
  src = ./.;
  doCheck = false;

  buildInputs = [
    gobject-introspection
    wrapGAppsHook
    gtk3
    ibus
  ];

  propagatedBuildInputs = [
    pygobject3
    xlib
    appdirs
    psutil

    simplei3
    simplealsa
  ];

  postPatch = ''
    substituteInPlace icebar/widgets/temperature.py \
      --replace '"sensors"' '"${lm_sensors}/bin/sensors"'
  '';
}
