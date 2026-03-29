# Garmin Connector Configuration

# Data directories
RAW_DATA_DIR = "data/garmin/raw"
INSIGHTS_DIR = "data/garmin/insights"
LOGS_DIR = "logs/garmin"

# Metrics to fetch
METRICS = {
    "daily_stats": True,
    "sleep": True,
    "heart_rate": True,
    "body_battery": True,
    "stress": True,
    "activities": True,
}

# Default goals (fallback if not in Garmin data)
DEFAULT_STEP_GOAL = 10000
DEFAULT_SLEEP_GOAL = 8.0  # hours

# Insight thresholds
SLEEP_QUALITY_THRESHOLDS = {
    "excellent": 80,
    "good": 60,
    "fair": 40,
    "poor": 0,
}

BODY_BATTERY_THRESHOLDS = {
    "high": 75,
    "medium": 50,
    "low": 25,
}

STRESS_THRESHOLDS = {
    "low": 25,
    "moderate": 50,
    "high": 75,
}