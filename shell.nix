{ python-version ? "36" }:
with builtins;
let
  pkgs = import <nixpkgs> {};
  from = where: what: getAttr what where;

  v = python-version;
  py = from pkgs "python${v}";
  pyp = from pkgs "python${v}Packages";

  extra = with pyp; [
    ipython
    numpy
    scipy
    pandas
    sympy
    notebook
    matplotlib
    seaborn
  ];

in pyp.buildPythonPackage rec {

  name = "bayex";
  src = ./.;
  propagatedBuildInputs = with pyp; [ networkx pytest ] ++ extra;
  doCheck = false;

}
