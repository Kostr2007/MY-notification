{
  lib,
  stdenvNoCC,
  makeWrapper,
  dunst,
  libcanberra-gtk3,
}:

stdenvNoCC.mkDerivation {
  pname = "my-notification";
  version = "0.1.0";
  src = lib.fileset.toSource {
    root = ../.;
    fileset = lib.fileset.unions [
      ../audio/glass.wav
      ../audio/CREDITS.md
      ../design
      ../tools/play.sh
    ];
  };

  nativeBuildInputs = [ makeWrapper ];
  dontBuild = true;

  installPhase = ''
    runHook preInstall
    install -Dm755 tools/play.sh "$out/libexec/my-notification"
    install -Dm644 audio/glass.wav "$out/share/my-notification/audio/glass.wav"
    install -Dm644 audio/CREDITS.md "$out/share/my-notification/audio/CREDITS.md"
    install -Dm644 design/notification.svg "$out/share/my-notification/design/notification.svg"
    install -Dm644 design/preview.html "$out/share/my-notification/design/preview.html"
    patchShebangs "$out/libexec/my-notification"
    makeWrapper "$out/libexec/my-notification" "$out/bin/my-notification" \
      --prefix PATH : ${
        lib.makeBinPath [
          dunst
          libcanberra-gtk3
        ]
      } \
      --set MY_NOTIFICATION_WAV "$out/share/my-notification/audio/glass.wav"
    runHook postInstall
  '';

  meta = {
    description = "Glass notification sound and Material You preview";
    mainProgram = "my-notification";
    platforms = lib.platforms.linux;
  };
}
