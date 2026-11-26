{
  description = "Material You notifications for m3 on i3";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { nixpkgs, ... }:
    let
      forLinux = nixpkgs.lib.genAttrs [
        "x86_64-linux"
        "aarch64-linux"
      ];
    in
    {
      packages = forLinux (system: {
        default = nixpkgs.legacyPackages.${system}.callPackage ./nix/package.nix { };
      });

      devShells = forLinux (system: {
        default = nixpkgs.legacyPackages.${system}.mkShell {
          packages = with nixpkgs.legacyPackages.${system}; [
            ffmpeg
            python3
          ];
        };
      });

      lib.withM3 =
        pkgs: m3:
        let
          notification = pkgs.callPackage ./nix/package.nix { };
        in
        m3.overrideAttrs (old: {
          patches = (old.patches or [ ]) ++ [ ./nix/m3-templates.patch ];
          postPatch = (old.postPatch or "") + ''
            substituteInPlace templates/dunstrc.j2 \
              --replace-fail '@my_notification@' '${notification}/bin/my-notification'
          '';
        });
    };
}
