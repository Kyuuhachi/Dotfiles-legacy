{ pkgs ? import <nixpkgs> {}
, pythonPackages ? pkgs.python3Packages
}:
with pkgs;
let ps = pythonPackages; in

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

	patches = [ (writeTextFile {
		name = "icebar.patch";
		text = ''
		--- a/icebar/simplealsa.py
		+++ b/icebar/simplealsa.py
		@@ -17,1 +17,1 @@
		-	asound = c.CDLL("libasound.so")
		+	asound = c.CDLL("${alsaLib.out}/lib/libasound.so")

		--- a/icebar/widgets/temperature.py
		+++ b/icebar/widgets/temperature.py
		@@ -11,1 +11,1 @@
		-	out = subprocess.check_output(["sensors", "-u"]).decode()
		+	out = subprocess.check_output(["${lm_sensors.out}/bin/sensors", "-u"]).decode()

		--- a/icebar/simplei3.py
		+++ b/icebar/simplei3.py
		@@ -11,1 +11,1 @@
		-		proc = await asyncio.create_subprocess_exec("i3", "--get-socketpath", stdout=asyncio.subprocess.PIPE)
		+		proc = await asyncio.create_subprocess_exec("${i3.out}/bin/i3", "--get-socketpath", stdout=asyncio.subprocess.PIPE)
		'';
	}) ];
}
