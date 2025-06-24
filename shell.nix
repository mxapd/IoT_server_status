{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.mpremote
  ];

  shellHook = ''
    echo "MicroPython dev environment ready."
  '';
}
