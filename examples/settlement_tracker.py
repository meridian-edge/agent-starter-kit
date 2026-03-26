"""
Settlement Tracker Agent
Tracks event settlements and builds accuracy database for model calibration.
Compares consensus predictions against actual outcomes.
"""
import csv
import json
from datetime import datetime
from meridianedge import MeridianEdge

def main():
    me = MeridianEdge()
    csv_file = f"settlements_{datetime.now():%Y%m%d}.csv"

    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['settled_at', 'event', 'sport', 'outcome', 'verification'])

    print(f"Settlement Tracker — logging to {csv_file}")
    settlements = me.settlements(limit=20)
    correct = sum(1 for s in settlements if s.get('outcome') == 'correct')
    total = len(settlements)

    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        for s in settlements:
            writer.writerow([
                s.get('settled_at', ''),
                s.get('event_key', ''),
                s.get('sport', ''),
                s.get('outcome', ''),
                s.get('verification', ''),
            ])

    print(f"Fetched {total} settlements. Correct: {correct}/{total}")
    if total > 0:
        print(f"Accuracy rate: {correct/total*100:.1f}%")
    print(f"Data saved to {csv_file}")
    print("\nFor informational purposes only. Not investment advice.")

if __name__ == "__main__":
    main()
