{
  lib,
  stdenvNoCC,
  makeWrapper,
  dunst,
  libcanberra-gtk3,
}:

stdenvNoCC.mkDerivation {
  pname = "my-notification";
  version = "0.2.0";
  src = lib.fileset.toSource {
    root = ../.;
    fileset = lib.fileset.unions [
      ../audio
      ../design
      ../tools/play.sh
    ];
  };

  nativeBuildInputs = [ makeWrapper ];
  dontBuild = true;

  installPhase = ''
    runHook preInstall
    install -Dm755 tools/play.sh "$out/libexec/my-notification"
    install -Dm644 -t "$out/share/my-notification/audio" audio/*.wav audio/CREDITS.md
    install -Dm644 -t "$out/share/my-notification/audio/source" audio/source/*
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
      --set MY_NOTIFICATION_AUDIO_DIR "$out/share/my-notification/audio"
    runHook postInstall
  '';

  meta = {
    description = "Notification sounds and Material You preview";
    mainProgram = "my-notification";
    platforms = lib.platforms.linux;
  };
}
