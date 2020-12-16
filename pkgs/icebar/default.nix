{ buildPythonApplication, mkPatch
, gobject-introspection, wrapGAppsHook, gtk3, ibus
, alsaLib, lm_sensors, i3
, pygobject3, xlib, appdirs, psutil
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
	];

	patches = [
		(mkPatch "icebar/simplealsa.py" 17
			''	asound = c.CDLL("«»")''
			"libasound.so" "${alsaLib}/lib/libasound.so")
		(mkPatch "icebar/widgets/temperature.py" 11
			''	out = subprocess.check_output(["«»", "-u"]).decode()''
			"sensors" "${lm_sensors}/bin/sensors")
		(mkPatch "icebar/simplei3.py" 21
			''		proc = await asyncio.create_subprocess_exec("«»", "--get-socketpath", stdout=asyncio.subprocess.PIPE)''
			"i3" "${i3}/bin/i3")
	];
}
