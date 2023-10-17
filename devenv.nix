{ pkgs, ... }:

{
  packages = [
    pkgs.nodePackages.pyright
  ];

  languages.python = {
    enable = true;
    version = "3.12";

    venv.enable = true;
    venv.requirements = ./requirements.txt;
  };
}
