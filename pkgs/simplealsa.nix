{ addSetupPy, buildPythonPackage, mkPatch, alsaLib }:
buildPythonPackage (addSetupPy {
	src = ./simplealsa.py;
	patches = [
		(mkPatch "simplealsa.py" 17
			''	asound = c.CDLL("«»")''
			"libasound.so" "${alsaLib}/lib/libasound.so")
	];
})

