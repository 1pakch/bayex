{ python-version ? "36" }:
with builtins;
let
  pkgs = import <nixpkgs> {};
  from = where: what: getAttr what where;

  v = python-version;
  python = from pkgs "python${v}";
  pythonPackages = from pkgs "python${v}Packages";
  
  package-names = [
    "ipython"
    #"tkinter" # support %paste in ipython
    "numpy"
    "scipy"
    "pandas"
    "sympy"
    "networkx"
    #"matplotlib"
    #"seaborn" # for pymc plots primarily
    #"imageio"
    #"ipykernel"
    #"ipywidgets"
    "notebook"
    #"pymc3"
    #"scikitlearn"
  ];

  bayex = pythonPackages.buildPythonPackage rec {
    name = "bayex";
    src = ./.;
    propagatedBuildInputs = with pythonPackages; [ networkx pytest ];
  };

  packages = map (from pythonPackages) package-names ++ [bayex];

in pkgs.stdenv.mkDerivation {

  name = "py${v}env";
  buildInputs = [python] ++ packages;

}
