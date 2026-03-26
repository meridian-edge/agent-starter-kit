"""
Daily Briefing Agent
Fetches all events with active consensus data and generates a formatted morning briefing.
Designed to run at market open via cron or scheduler.

For informational purposes only. Not investment advice.
"""
import json
from datetime import datetime
from meridianedge import MeridianEdge


def format_briefing(briefings):
    """Format briefings list into a readable report string."""
    lines = [
        "=" * 60,
        f"MERIDIAN EDGE DAILY BRIEFING — {datetime.now():%B %d, %Y}",
        "For informational purposes only. Not investment advice.",
        "=" * 60,
        "",
    ]

    by_sport = {}
    for b in briefings:
        sport = b.get("sport", "other").upper()
        by_sport.setdefault(sport, []).append(b)

    for sport, items in sorted(by_sport.items()):
        lines.append(f"── {sport} ({len(items)} events) ──")
        for b in sorted(items, key=lambda x: x.get("consensus", 0.5), reverse=True):
            consensus_pct = b.get("consensus", 0.5) * 100
            conf = b.get("confidence", "?")
            mv = b.get("movement", "stable").upper()
            lines.append(f"  {b.get('event_name', b.get('event_key', '')[:50])}")
            lines.append(f"    {consensus_pct:.1f}% consensus  |  {conf} confidence  |  {mv}")
            if b.get("narrative"):
                lines.append(f"    {b['narrative']}")
            lines.append("")

    lines += [
        "-" * 60,
        f"Total events: {len(briefings)}",
        "Data aggregated from multiple regulated prediction markets.",
        "For informational purposes only. Not investment advice.",
        "Contact: support@meridianedge.io",
        "-" * 60,
    ]
    return "\n".join(lines)


def main():
    me = MeridianEdge()

    print("Fetching daily briefings...")
    result = me.briefings_today()
    briefings = result.get("briefings", [])

    if not briefings:
        print("No events found for today's briefing.")
        return

    report = format_briefing(briefings)
    print(report)

    # Optionally save to file
    fname = f"briefing_{datetime.now():%Y%m%d}.txt"
    with open(fname, "w") as f:
        f.write(report)
    print(f"\nBriefing saved to {fname}")

    print("\nFor informational purposes only. Not investment advice.")

if __name__ == "__main__":
    main()
