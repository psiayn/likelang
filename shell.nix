with import <nixpkgs> {};
let
  pythonEnv = python38.withPackages (ps: [
    ps.lark-parser
  ]);
in mkShell {
  packages = [
    pythonEnv
    black
  ];
}
