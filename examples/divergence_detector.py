"""
Divergence Detector Agent
Identifies events where regulated prediction markets show unusual disagreement.
High spread = markets are divided. Surfaces these for human review or downstream analysis.

For informational purposes only. Not investment advice.
"""
import json
from datetime import datetime
from meridianedge import MeridianEdge

DIVERGENCE_THRESHOLD = 0.08  # 8% spread = high divergence

def main():
    me = MeridianEdge()

    print(f"Divergence Detector — {datetime.now():%Y-%m-%d %H:%M:%S}")
    print(f"Threshold: {DIVERGENCE_THRESHOLD*100:.0f}% spread\n")

    events = me.consensus()
    divergent = [e for e in events if abs(e.get("spread", 0)) >= DIVERGENCE_THRESHOLD]

    if not divergent:
        print("No high-divergence events detected.")
    else:
        print(f"Found {len(divergent)} high-divergence event(s):\n")
        for e in sorted(divergent, key=lambda x: abs(x.get("spread", 0)), reverse=True):
            spread_pct = abs(e.get("spread", 0)) * 100
            consensus_pct = e.get("consensus", 0.5) * 100
            print(f"  [{e.get('sport','').upper():6}] {e.get('event_name', e.get('event_key',''))}")
            print(f"           Consensus: {consensus_pct:.1f}%  |  Spread: {spread_pct:.1f}%  |  Confidence: {e.get('confidence','?')}")
            if e.get("narrative"):
                print(f"           {e['narrative']}")
            print()

    print(f"Total events scanned: {len(events)}")
    print("\nFor informational purposes only. Not investment advice.")
    print("Data aggregated from multiple regulated prediction markets.")

if __name__ == "__main__":
    main()
