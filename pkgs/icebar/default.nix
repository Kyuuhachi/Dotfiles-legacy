{ buildPythonApplication, mkPatch
, gobject-introspection, wrapGAppsHook, gtk3, ibus
, alsaLib, lm_sensors
, pygobject3, xlib, appdirs, psutil
, simplei3
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
	];

	patches = [
		(mkPatch "icebar/simplealsa.py" 17
			''	asound = c.CDLL("«»")''
			"libasound.so" "${alsaLib}/lib/libasound.so")
		(mkPatch "icebar/widgets/temperature.py" 11
			''	out = subprocess.check_output(["«»", "-u"]).decode()''
			"sensors" "${lm_sensors}/bin/sensors")
	];
}
