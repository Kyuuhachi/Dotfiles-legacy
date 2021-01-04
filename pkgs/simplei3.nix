{ addSetupPy, buildPythonPackage, i3, anyio }:
buildPythonPackage (addSetupPy {
  src = ./simplei3.py;
  propagatedBuildInputs = [ anyio ];
  postPatch = ''
    substituteInPlace simplei3.py \
      --replace '"i3"' '"${i3}/bin/i3"'
  '';
})
