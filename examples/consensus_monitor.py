"""
Consensus Monitor Agent
Watches for significant consensus movement above a configurable threshold.
Logs alerts when markets shift direction meaningfully.

For informational purposes only. Not investment advice.
"""
import time
import json
from datetime import datetime
from meridianedge import MeridianEdge

POLL_INTERVAL_SECONDS = 60
MOVEMENT_ALERT_SPORTS = ["nba", "nhl", "nfl"]


def check_movements(me, prior_state):
    """Fetch current consensus, compare to prior state, return alerts."""
    events = me.consensus()
    alerts = []
    new_state = {}

    for e in events:
        key = e.get("event_key", "")
        consensus = e.get("consensus", 0.5)
        movement = e.get("movement", "stable")
        new_state[key] = consensus

        if key in prior_state:
            delta = consensus - prior_state[key]
            if abs(delta) >= 0.05:  # 5% move since last poll
                alerts.append({
                    "event_key": key,
                    "event_name": e.get("event_name", key),
                    "sport": e.get("sport", ""),
                    "prior": prior_state[key],
                    "current": consensus,
                    "delta": delta,
                    "movement": movement,
                    "narrative": e.get("narrative", ""),
                })

    return new_state, alerts


def main():
    me = MeridianEdge()
    print(f"Consensus Monitor started — {datetime.now():%Y-%m-%d %H:%M:%S}")
    print(f"Polling every {POLL_INTERVAL_SECONDS}s. Ctrl+C to stop.\n")

    # Seed initial state
    events = me.consensus()
    state = {e.get("event_key", ""): e.get("consensus", 0.5) for e in events}
    print(f"Seeded {len(state)} events. Watching for movement...\n")

    try:
        while True:
            time.sleep(POLL_INTERVAL_SECONDS)
            state, alerts = check_movements(me, state)

            if alerts:
                ts = datetime.now().strftime("%H:%M:%S")
                for a in alerts:
                    direction = "UP" if a["delta"] > 0 else "DOWN"
                    print(f"[{ts}] MOVEMENT {direction} | {a['event_name']}")
                    print(f"          {a['prior']*100:.1f}% → {a['current']*100:.1f}%  (Δ{a['delta']*100:+.1f}%)")
                    if a.get("narrative"):
                        print(f"          {a['narrative']}")
                    print()
            else:
                print(f"[{datetime.now():%H:%M:%S}] No significant movement. {len(state)} events tracked.")

    except KeyboardInterrupt:
        print("\nMonitor stopped.")

    print("\nFor informational purposes only. Not investment advice.")

if __name__ == "__main__":
    main()
