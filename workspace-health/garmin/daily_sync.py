#!/usr/bin/env python3
"""
Daily Garmin Sync - Automated data fetch and insights generation
Runs via OpenClaw cron scheduler
"""

import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Add garmin directory to path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from garmin_connector import GarminConnector
from garmin_insights import GarminInsights


def main():
    """Run daily sync and generate insights."""
    start_time = datetime.now()
    print(f"🔄 Starting daily Garmin sync at {start_time.isoformat()}")
    
    # Connect and fetch data
    connector = GarminConnector()
    
    if not connector.connect():
        print("❌ Failed to connect to Garmin Connect")
        print("💡 This is often due to Garmin rate limiting. The next run will retry automatically.")
        return 1
    
    print("✅ Connected to Garmin Connect")
    
    # Fetch yesterday's data (today's data might not be complete yet)
    yesterday = datetime.now() - timedelta(days=1)
    print(f"📊 Fetching data for {yesterday.strftime('%Y-%m-%d')}...")
    
    data = connector.fetch_all(yesterday)
    
    # Check what we got
    metrics_fetched = []
    if data.get("daily_stats"):
        metrics_fetched.append("daily stats")
    if data.get("sleep"):
        metrics_fetched.append("sleep")
    if data.get("heart_rate"):
        metrics_fetched.append("heart rate")
    if data.get("body_battery"):
        metrics_fetched.append("body battery")
    if data.get("stress"):
        metrics_fetched.append("stress")
    if data.get("activities"):
        metrics_fetched.append("activities")
    
    print(f"✅ Fetched: {', '.join(metrics_fetched)}")
    
    # Generate insights
    print("🧠 Generating insights...")
    insights = GarminInsights()
    
    # Daily briefing (for today, based on yesterday's recovery)
    today = datetime.now()
    briefing = insights.generate_daily_briefing(today)
    insights.save_insights(briefing, "daily_briefing", today)
    print("✅ Daily briefing saved")
    
    # Also save to a consistent location for easy reading
    latest_file = script_dir / "data" / "garmin" / "insights" / "LATEST_DAILY.md"
    latest_file.parent.mkdir(parents=True, exist_ok=True)
    with open(latest_file, 'w') as f:
        f.write(briefing)
    print(f"✅ Latest briefing saved to {latest_file}")
    
    # Weekly report (on Sundays)
    if today.weekday() == 6:  # Sunday
        weekly = insights.generate_weekly_report(today)
        insights.save_insights(weekly, "weekly_report", today)
        # Also save as latest weekly
        latest_weekly = script_dir / "data" / "garmin" / "insights" / "LATEST_WEEKLY.md"
        with open(latest_weekly, 'w') as f:
            f.write(weekly)
        print("✅ Weekly report saved")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"✅ Daily sync complete in {duration:.1f}s at {end_time.isoformat()}")
    return 0


if __name__ == "__main__":
    exit(main())