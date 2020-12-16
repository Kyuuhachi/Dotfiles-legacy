{ pkgs ? import <nixpkgs> {}
, pythonPackages ? pkgs.python3Packages
}:
with pkgs;
let ps = pythonPackages; in

let mkPatch = file: lineno: text: from: to: writeTextFile {
	name = "${file}.patch";
	text = let
		linestr = toString lineno;
		line1 = builtins.replaceStrings ["«»"] [from] text;
		line2 = builtins.replaceStrings ["«»"] [to] text;
	in "--- a/${file}\n+++ b/${file}\n@@ -${linestr},1 +${linestr},1 @@\n-${line1}\n+${line2}\n";
}; in

ps.buildPythonApplication rec {
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
		ps.pygobject3
		ps.xlib
		ps.appdirs
		ps.psutil
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
