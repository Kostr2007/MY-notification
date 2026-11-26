#!/usr/bin/env bash
set -euo pipefail

case "${1:-}" in
  --dunst)
    case "${DUNST_URGENCY:-NORMAL}" in NORMAL) ;; *) exit 0 ;; esac
    case "${DUNST_STACK_TAG:-}" in m3-osd|m3-theme|m3-mode|m3) exit 0 ;; esac
    case "${DUNST_APP_NAME:-}" in OSD|"Material You"|"Центр управления") exit 0 ;; esac
    if [[ "$(dunstctl is-paused 2>/dev/null)" == true ]]; then
      exit 0
    fi
    ;;
  "") ;;
  *)
    printf 'Usage: my-notification [--dunst]\n' >&2
    exit 2
    ;;
esac

exec canberra-gtk-play --file="${MY_NOTIFICATION_WAV:?}" --description="MY Notification"
