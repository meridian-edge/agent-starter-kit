"""
Slack Alerter Agent
Posts consensus movement alerts to a Slack channel via webhook.
Designed to run on a schedule (e.g., every 5 minutes via cron).

For informational purposes only. Not investment advice.
"""
import os
import json
import time
import urllib.request
from datetime import datetime
from meridianedge import MeridianEdge

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")
MOVEMENT_THRESHOLD = 0.06  # Alert on 6%+ consensus moves
CHECK_SPORTS = ["nba", "nhl"]

STATE_FILE = "/tmp/meridian_slack_state.json"


def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def post_to_slack(message):
    if not SLACK_WEBHOOK_URL:
        print(f"[SLACK] {message}")
        return
    payload = json.dumps({"text": message}).encode()
    req = urllib.request.Request(
        SLACK_WEBHOOK_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"Slack post failed: {e}")


def main():
    me = MeridianEdge()
    prior = load_state()

    events = me.consensus()
    current = {}
    alerts = []

    for e in events:
        key = e.get("event_key", "")
        sport = e.get("sport", "").lower()
        if sport not in CHECK_SPORTS:
            continue
        consensus = e.get("consensus", 0.5)
        current[key] = consensus

        if key in prior:
            delta = consensus - prior[key]
            if abs(delta) >= MOVEMENT_THRESHOLD:
                direction = "📈" if delta > 0 else "📉"
                name = e.get("event_name", key)
                narrative = e.get("narrative", "")
                msg = (
                    f"{direction} *Consensus Alert* — {name}\n"
                    f">{prior[key]*100:.1f}% → {consensus*100:.1f}% (Δ{delta*100:+.1f}%)\n"
                    f">{narrative}\n"
                    f">_For informational purposes only. Not investment advice._"
                )
                alerts.append(msg)

    if alerts:
        for msg in alerts:
            post_to_slack(msg)
        print(f"Sent {len(alerts)} alert(s) to Slack.")
    else:
        print(f"No significant movements detected ({len(current)} events checked).")

    # Merge current into prior (only update keys we just fetched)
    prior.update(current)
    save_state(prior)

    print("For informational purposes only. Not investment advice.")

if __name__ == "__main__":
    main()
