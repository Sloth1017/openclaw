# Garmin Health Connector

A minimal, secure connector for pulling health data from Garmin Connect.

## Security Principles

1. **Read-only access** - Only fetches data, never writes
2. **Local-only storage** - All data stays in your workspace
3. **No third-party dependencies** beyond `garminconnect` Python package
4. **Audit trail** - All actions logged locally

## Setup

1. Install dependencies:
   ```bash
   pip install garminconnect python-dotenv
   ```

2. Create `.env` file with your Garmin credentials:
   ```
   GARMIN_EMAIL=your-email@example.com
   GARMIN_PASSWORD=your-password
   ```

3. Run the connector:
   ```bash
   python garmin_connector.py
   ```

## Data Storage

- Raw data: `data/garmin/raw/YYYY-MM-DD/`
- Processed insights: `data/garmin/insights/`
- Logs: `logs/garmin/`

## What Data is Fetched

- Daily steps
- Heart rate (resting, min, max)
- Sleep data (duration, score, stages)
- Stress levels
- Body battery
- Activities/workouts

## Files

- `garmin_connector.py` - Main connector script
- `garmin_insights.py` - Insight generation (local analysis)
- `config.py` - Configuration and constants