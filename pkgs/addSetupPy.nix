{ lib }:

{
  src,
  _basename ? lib.removeSuffix ".py" (baseNameOf src),
  name ? _basename,
  version ? "0.0",
  preConfigure ? "",
  ...
}@attrs:
attrs // {
  inherit name version src;
  doCheck = false;
  unpackPhase = "cp ${src} $(stripHash ${src})";
  preConfigure = preConfigure + ''
    echo >setup.py '
    import setuptools
    setuptools.setup(name="${name}", version="${version}", py_modules=["${_basename}"])
    '
  '';
}
