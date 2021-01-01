{ addSetupPy, buildPythonPackage, i3 }:
buildPythonPackage (addSetupPy {
  src = ./simplei3.py;
  postPatch = ''
    substituteInPlace simplei3.py \
      --replace '"i3"' '"${i3}/bin/i3"'
  '';
})
