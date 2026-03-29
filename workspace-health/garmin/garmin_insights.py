"""
Garmin Insights - Local analysis of health data
Generates insights without sending data to external APIs.
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent / "data" / "garmin"


@dataclass
class DailySummary:
    """Summary of daily health metrics."""
    date: str
    steps: int
    steps_goal: int
    resting_hr: Optional[int]
    sleep_hours: Optional[float]
    sleep_score: Optional[int]
    body_battery_max: Optional[int]
    stress_avg: Optional[int]
    calories: Optional[int]
    
    @property
    def steps_percentage(self) -> float:
        if self.steps_goal > 0:
            return (self.steps / self.steps_goal) * 100
        return 0
    
    @property
    def sleep_quality(self) -> str:
        if self.sleep_score is None:
            return "unknown"
        if self.sleep_score >= 80:
            return "excellent"
        elif self.sleep_score >= 60:
            return "good"
        elif self.sleep_score >= 40:
            return "fair"
        return "poor"


class GarminInsights:
    """Generate insights from locally stored Garmin data."""
    
    def __init__(self):
        self.raw_dir = DATA_DIR / "raw"
        self.insights_dir = DATA_DIR / "insights"
        self.insights_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_json(self, filepath: Path) -> Dict[str, Any]:
        """Load JSON file safely."""
        try:
            with open(filepath) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.debug(f"Could not load {filepath}: {e}")
            return {}
    
    def parse_daily_summary(self, date: datetime) -> Optional[DailySummary]:
        """Parse daily stats into a summary object."""
        date_str = date.strftime("%Y-%m-%d")
        date_dir = self.raw_dir / date_str
        
        if not date_dir.exists():
            return None
        
        # Load daily stats
        stats = self._load_json(date_dir / "daily_stats.json")
        sleep = self._load_json(date_dir / "sleep_data.json")
        battery = self._load_json(date_dir / "body_battery.json")
        stress = self._load_json(date_dir / "stress_data.json")
        
        # Extract key metrics
        steps = stats.get("totalSteps", 0)
        steps_goal = stats.get("dailyStepGoal", 10000)
        resting_hr = stats.get("restingHeartRate")
        calories = stats.get("totalKilocalories")
        
        # Sleep data
        sleep_hours = None
        sleep_score = None
        if sleep and "sleepTimeInSeconds" in sleep:
            sleep_hours = sleep["sleepTimeInSeconds"] / 3600
            sleep_score = sleep.get("sleepScore")
        
        # Body battery
        body_battery_max = None
        if battery and isinstance(battery, list) and len(battery) > 0:
            # Get max battery for the day
            battery_values = [b.get("bodyBatteryValue", 0) for b in battery if isinstance(b, dict)]
            if battery_values:
                body_battery_max = max(battery_values)
        
        # Stress average
        stress_avg = None
        if stress and isinstance(stress, list) and len(stress) > 0:
            stress_values = [s.get("stressLevel", 0) for s in stress if isinstance(s, dict) and s.get("stressLevel", -1) >= 0]
            if stress_values:
                stress_avg = sum(stress_values) // len(stress_values)
        
        return DailySummary(
            date=date_str,
            steps=steps,
            steps_goal=steps_goal,
            resting_hr=resting_hr,
            sleep_hours=sleep_hours,
            sleep_score=sleep_score,
            body_battery_max=body_battery_max,
            stress_avg=stress_avg,
            calories=calories
        )
    
    def get_weekly_summary(self, end_date: Optional[datetime] = None) -> List[DailySummary]:
        """Get summary for the past 7 days."""
        end_date = end_date or datetime.now()
        summaries = []
        
        for i in range(7):
            date = end_date - timedelta(days=i)
            summary = self.parse_daily_summary(date)
            if summary:
                summaries.append(summary)
        
        return list(reversed(summaries))
    
    def generate_recovery_recommendation(self, summary: DailySummary) -> str:
        """Generate a recovery recommendation based on metrics."""
        recommendations = []
        
        # Sleep-based recommendations
        if summary.sleep_hours is not None:
            if summary.sleep_hours < 6:
                recommendations.append("⚠️ Low sleep detected. Prioritize rest today.")
            elif summary.sleep_hours < 7:
                recommendations.append("💤 Sleep was shorter than ideal. Consider an early night.")
        
        if summary.sleep_score is not None and summary.sleep_score < 60:
            recommendations.append("😴 Sleep quality was poor. Light activity recommended.")
        
        # Body battery
        if summary.body_battery_max is not None:
            if summary.body_battery_max < 25:
                recommendations.append("🔋 Body battery very low. Take it easy today.")
            elif summary.body_battery_max < 50:
                recommendations.append("🔋 Body battery below average. Moderate intensity.")
        
        # Resting HR trend (would need historical data for proper trend)
        if summary.resting_hr is not None and summary.resting_hr > 70:
            recommendations.append("❤️ Resting HR elevated. Monitor for overtraining.")
        
        # Stress
        if summary.stress_avg is not None:
            if summary.stress_avg > 50:
                recommendations.append("😰 High stress levels. Consider relaxation techniques.")
            elif summary.stress_avg > 35:
                recommendations.append("🧘 Moderate stress. Take breaks during the day.")
        
        if not recommendations:
            return "✅ Metrics look good. Ready for a normal training day!"
        
        return "\n".join(recommendations)
    
    def generate_daily_briefing(self, date: Optional[datetime] = None) -> str:
        """Generate a morning briefing similar to Ihor's Aris."""
        date = date or datetime.now()
        yesterday = date - timedelta(days=1)
        
        # Get yesterday's data for recovery insights
        summary = self.parse_daily_summary(yesterday)
        
        if not summary:
            return f"No data available for {yesterday.strftime('%Y-%m-%d')}. Make sure to sync your Garmin."
        
        lines = [
            f"📊 **Morning Briefing - {date.strftime('%A, %B %d')}**",
            "",
            f"**Yesterday's Recovery:**",
            f"• Sleep: {summary.sleep_hours:.1f}h" if summary.sleep_hours else "• Sleep: No data",
            f"• Sleep Score: {summary.sleep_score}/100 ({summary.sleep_quality})" if summary.sleep_score else "• Sleep Score: No data",
            f"• Resting HR: {summary.resting_hr} bpm" if summary.resting_hr else "• Resting HR: No data",
            f"• Body Battery: {summary.body_battery_max}%" if summary.body_battery_max else "• Body Battery: No data",
            "",
            f"**Steps:** {summary.steps:,} / {summary.steps_goal:,} ({summary.steps_percentage:.0f}%)",
            "",
            "**Today's Recommendation:**",
            self.generate_recovery_recommendation(summary),
        ]
        
        return "\n".join(lines)
    
    def generate_weekly_report(self, end_date: Optional[datetime] = None) -> str:
        """Generate a weekly summary report."""
        summaries = self.get_weekly_summary(end_date)
        
        if not summaries:
            return "No data available for the past week."
        
        # Calculate averages
        avg_steps = sum(s.steps for s in summaries) / len(summaries)
        avg_sleep = sum(s.sleep_hours for s in summaries if s.sleep_hours) / len([s for s in summaries if s.sleep_hours]) if any(s.sleep_hours for s in summaries) else 0
        avg_resting_hr = sum(s.resting_hr for s in summaries if s.resting_hr) / len([s for s in summaries if s.resting_hr]) if any(s.resting_hr for s in summaries) else 0
        
        lines = [
            f"📈 **Weekly Report ({summaries[0].date} to {summaries[-1].date})**",
            "",
            "**Averages:**",
            f"• Steps: {avg_steps:,.0f} / day",
            f"• Sleep: {avg_sleep:.1f}h / night" if avg_sleep else "• Sleep: No data",
            f"• Resting HR: {avg_resting_hr:.0f} bpm" if avg_resting_hr else "• Resting HR: No data",
            "",
            "**Daily Breakdown:**",
        ]
        
        for s in summaries:
            sleep_str = f"{s.sleep_hours:.1f}h" if s.sleep_hours else "-"
            hr_str = f"{s.resting_hr}bpm" if s.resting_hr else "-"
            lines.append(f"• {s.date}: {s.steps:,} steps | {sleep_str} sleep | {hr_str} RHR")
        
        return "\n".join(lines)
    
    def save_insights(self, content: str, name: str, date: datetime):
        """Save generated insights to file."""
        date_dir = self.insights_dir / date.strftime("%Y-%m-%d")
        date_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = date_dir / f"{name}.md"
        with open(filepath, 'w') as f:
            f.write(content)
        
        logger.info(f"Saved insights to {filepath}")
        return filepath


def main():
    """CLI for generating insights."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate insights from Garmin data")
    parser.add_argument("--type", choices=["daily", "weekly"], default="daily",
                       help="Type of report to generate")
    parser.add_argument("--date", type=str, help="Date (YYYY-MM-DD), defaults to today")
    parser.add_argument("--save", action="store_true", help="Save to file")
    
    args = parser.parse_args()
    
    if args.date:
        date = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        date = datetime.now()
    
    insights = GarminInsights()
    
    if args.type == "daily":
        report = insights.generate_daily_briefing(date)
    else:
        report = insights.generate_weekly_report(date)
    
    print(report)
    
    if args.save:
        filepath = insights.save_insights(report, args.type, date)
        print(f"\nSaved to: {filepath}")


if __name__ == "__main__":
    main()