{ addSetupPy, buildPythonPackage, mkPatch, i3 }:
buildPythonPackage (addSetupPy {
	src = ./simplei3.py;
	patches = [
		(mkPatch "simplei3.py" 21
			''		proc = await asyncio.create_subprocess_exec("«»", "--get-socketpath", stdout=asyncio.subprocess.PIPE)''
			"i3" "${i3}/bin/i3")
	];
})
