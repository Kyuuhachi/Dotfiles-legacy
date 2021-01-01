{ addSetupPy, buildPythonPackage, alsaLib }:
buildPythonPackage (addSetupPy {
  src = ./simplealsa.py;
  postPatch = ''
    substituteInPlace simplealsa.py \
      --replace '"libasound.so"' '"${alsaLib}/lib/libasound.so"'
  '';
})

