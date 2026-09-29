#!/bin/sh
# Read-only pull of YouTube Studio analytics through agent-browser, using a logged-in Chrome profile.
# Never click, edit or save anything in Studio: this only opens report URLs and reads the table.
#
# Usage:
#   scripts/studio_pull.sh login                    open a visible window to sign in once
#   scripts/studio_pull.sh videos [channel_id]      lifetime per-video table: views, impressions, CTR, retention, subs
#   scripts/studio_pull.sh traffic <video_id>...    traffic-source split per video (browse, search, suggested, external)
#
# Env: STUDIO_PROFILE (default ~/.agent-browser-profiles/youtube-studio), STUDIO_SESSION (default yt-studio)
set -e
profile=${STUDIO_PROFILE:-$HOME/.agent-browser-profiles/youtube-studio}
session=${STUDIO_SESSION:-yt-studio}
ab() { agent-browser --session "$session" --profile "$profile" "$@" </dev/null; }
rows() { ab eval "Array.from(document.querySelectorAll('yta-explore-table-row')).map(r=>r.innerText.replace(/\s*\n\s*/g,' | ')).join('\n')" | sed 's/^"//; s/"$//; s/\\n/\n/g'; }

cmd=${1:-videos}; shift || true
case $cmd in
  login)
    ab --headed open "https://studio.youtube.com" >/dev/null
    echo "Sign in in the browser window, then rerun with 'videos'."
    ;;
  videos)
    c=${1:-UCO60vEm-6WAAtGckVqCi6Vg}
    ab open "https://studio.youtube.com/channel/$c/analytics/tab-overview/period-default/explore?entity_type=CHANNEL&entity_id=$c&time_period=lifetime&explore_type=TABLE_AND_CHART&metric=VIEWS&granularity=DAY&t_metrics=VIEWS&t_metrics=VIDEO_THUMBNAIL_IMPRESSIONS&t_metrics=VIDEO_THUMBNAIL_IMPRESSIONS_VTR&t_metrics=AVERAGE_WATCH_TIME&t_metrics=AVERAGE_WATCH_PERCENTAGE&t_metrics=SUBSCRIBERS_NET_CHANGE&t_metrics=WATCH_TIME&dimension=VIDEO&o_column=VIEWS&o_direction=ANALYTICS_ORDER_DIRECTION_DESC" >/dev/null
    sleep 8
    case $(ab get url) in *accounts.google.com*) echo "Not signed in: run '$0 login' first." >&2; exit 1;; esac
    echo "duration | title | views | views% | impressions | ctr | avg_view_duration | avg_pct_viewed | subs | subs% | watch_hours | watch%"
    rows
    ;;
  traffic)
    for v in "$@"; do
      ab open "https://studio.youtube.com/video/$v/analytics/tab-overview/period-default/explore?entity_type=VIDEO&entity_id=$v&time_period=lifetime&explore_type=TABLE_AND_CHART&metric=VIEWS&granularity=DAY&t_metrics=VIEWS&t_metrics=VIDEO_THUMBNAIL_IMPRESSIONS&t_metrics=VIDEO_THUMBNAIL_IMPRESSIONS_VTR&t_metrics=AVERAGE_WATCH_TIME&dimension=TRAFFIC_SOURCE_TYPE&o_column=VIEWS&o_direction=ANALYTICS_ORDER_DIRECTION_DESC" >/dev/null
      sleep 6
      echo "== $v (source | views | share | impressions | ctr | avg_view_duration)"
      rows
    done
    ;;
  *) echo "unknown command: $cmd" >&2; exit 2 ;;
esac
