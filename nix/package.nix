{
  lib,
  stdenvNoCC,
  makeWrapper,
  dunst,
  libcanberra-gtk3,
  sound-theme-freedesktop,
}:

let
  events = {
    message-new-instant = "lullaby";
    message-new-email = "lullaby";
    audio-volume-change = "volume";
    device-added = "connect";
    device-removed = "disconnect";
    dialog-information = "connect";
    dialog-question = "attention";
    dialog-warning = "attention";
    dialog-error = "error";
    window-attention = "attention";
  };
in
stdenvNoCC.mkDerivation {
  pname = "my-notification";
  version = "0.4.1";
  src = lib.fileset.toSource {
    root = ../.;
    fileset = lib.fileset.unions [
      ../audio
      ../design
      ../tools/play.sh
      ./sound-theme.index
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
    theme="$out/share/sounds/my-notification"
    install -Dm644 nix/sound-theme.index "$theme/index.theme"
    mkdir -p "$theme/stereo"
    ${lib.concatLines (
      lib.mapAttrsToList (
        event: cue: ''ln -s "../../../my-notification/audio/${cue}.wav" "$theme/stereo/${event}.wav"''
      ) events
    )}
    patchShebangs "$out/libexec/my-notification"
    makeWrapper "$out/libexec/my-notification" "$out/bin/my-notification" \
      --prefix PATH : ${
        lib.makeBinPath [
          dunst
          libcanberra-gtk3
        ]
      } \
      --prefix XDG_DATA_DIRS : "$out/share:${sound-theme-freedesktop}/share" \
      --set MY_NOTIFICATION_AUDIO_DIR "$out/share/my-notification/audio"
    for theme in my-notification freedesktop; do
      makeWrapper "$out/bin/my-notification" "$out/libexec/dunst/$theme" \
        --add-flags "--dunst $theme system"
    done
    for cue in lullaby kalimba piano nylon glass; do
      makeWrapper "$out/bin/my-notification" "$out/libexec/dunst/$cue" \
        --add-flags "--dunst my-notification $cue"
    done
    runHook postInstall
  '';

  meta = {
    description = "Notification sounds and Material You preview";
    mainProgram = "my-notification";
    platforms = lib.platforms.linux;
  };
}
