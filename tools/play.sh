#!/usr/bin/env bash
set -euo pipefail

play_event() {
  local theme=$1 event=$2
  case "$theme" in
    my-notification|freedesktop) ;;
    *) return 2 ;;
  esac

  exec canberra-gtk-play --id="$event" --description="MY Notification" \
    --property="canberra.xdg-theme.name=$theme" --property=canberra.enable=1
}

play_cue() {
  case "$1" in
    lullaby|kalimba|piano|nylon|glass|wood|paper|drop) ;;
    *) return 2 ;;
  esac

  exec canberra-gtk-play --file="${MY_NOTIFICATION_AUDIO_DIR:?}/$1.wav" \
    --description="MY Notification" --property=canberra.enable=1
}

case "${1:-lullaby}" in
  --dunst)
    case "${DUNST_URGENCY:-NORMAL}" in NORMAL) ;; *) exit 0 ;; esac
    case "${DUNST_STACK_TAG:-}" in m3-osd|m3-theme|m3-mode|m3) exit 0 ;; esac
    case "${DUNST_APP_NAME:-}" in OSD|"Material You"|"Центр управления") exit 0 ;; esac
    if [[ "$(dunstctl is-paused 2>/dev/null)" == true ]]; then
      exit 0
    fi
    if [[ "${3:-system}" == "system" ]]; then
      play_event "${2:-my-notification}" message-new-instant
    else
      play_cue "$3"
    fi
    ;;
  --preview-notification)
    if [[ "$3" == "system" ]]; then
      play_event "$2" message-new-instant
    else
      play_cue "$3"
    fi
    ;;
  --event)
    play_event "$2" "$3"
    ;;
  *)
    if ! play_cue "${1:-lullaby}"; then
      printf 'Usage: my-notification [lullaby|kalimba|piano|nylon|glass|wood|paper|drop]\n' >&2
      exit 2
    fi
    ;;
esac
