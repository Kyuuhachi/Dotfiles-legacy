{ buildPythonApplication, mkPatch
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

	patches = [
		(mkPatch "icebar/widgets/temperature.py" 11
			''	out = subprocess.check_output(["«»", "-u"]).decode()''
			"sensors" "${lm_sensors}/bin/sensors")
	];
}
