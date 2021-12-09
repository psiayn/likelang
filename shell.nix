with import <nixpkgs> {};
let
  pythonEnv = python39.withPackages (ps: [
    ps.lark-parser
  ]);
in mkShell {
  packages = [
    pythonEnv
    python39
    black
    nodejs
  ];
}
