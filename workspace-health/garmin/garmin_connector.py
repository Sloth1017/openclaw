"""
Garmin Connect - Minimal Secure Connector
Fetches health data with read-only access, stores locally.
"""

import os
import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any

from garminconnect import Garmin
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

# Configuration
DATA_DIR = Path(__file__).parent / "data" / "garmin"
LOGS_DIR = Path(__file__).parent / "logs" / "garmin"
TOKEN_DIR = Path(__file__).parent / ".garmin_tokens"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)
TOKEN_DIR.mkdir(parents=True, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / f"garmin_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class GarminConnector:
    """Minimal Garmin Connect connector with security-first design."""
    
    def __init__(self):
        self.email = os.getenv("GARMIN_EMAIL")
        self.password = os.getenv("GARMIN_PASSWORD")
        self.client: Optional[Garmin] = None
        self.token_file = TOKEN_DIR / "tokens.json"
        
        if not self.email or not self.password:
            raise ValueError("GARMIN_EMAIL and GARMIN_PASSWORD must be set in .env file")
    
    def _save_tokens(self):
        """Save authentication tokens for reuse."""
        if self.client:
            tokens = {
                "oauth1": self.client.garth.oauth1_token,
                "oauth2": self.client.garth.oauth2_token
            }
            with open(self.token_file, 'w') as f:
                json.dump(tokens, f)
            logger.info(f"Saved tokens to {self.token_file}")
    
    def _load_tokens(self) -> bool:
        """Load saved tokens if available."""
        if not self.token_file.exists():
            return False
        
        try:
            with open(self.token_file) as f:
                tokens = json.load(f)
            
            # Create client with tokens
            self.client = Garmin(self.email, self.password)
            self.client.garth.oauth1_token = tokens.get("oauth1")
            self.client.garth.oauth2_token = tokens.get("oauth2")
            
            # Test if tokens are valid
            try:
                self.client.get_full_name()
                logger.info("Authenticated using saved tokens")
                return True
            except Exception as e:
                logger.info(f"Saved tokens expired: {e}")
                self.client = None
                return False
                
        except Exception as e:
            logger.warning(f"Could not load tokens: {e}")
            return False
    
    def connect(self) -> bool:
        """Authenticate with Garmin Connect."""
        # Try tokens first
        if self._load_tokens():
            return True
        
        # Fall back to password login with retry
        max_retries = 5
        base_wait = 60  # Start with 60 seconds
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Connecting to Garmin Connect as {self.email} (attempt {attempt + 1}/{max_retries})")
                
                # Add delay between retries (exponential backoff)
                if attempt > 0:
                    wait_time = base_wait * (2 ** (attempt - 1))  # 60s, 120s, 240s, 480s
                    logger.info(f"Rate limit detected. Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                
                self.client = Garmin(self.email, self.password)
                self.client.login()
                
                # Save tokens for next time
                self._save_tokens()
                
                logger.info("Successfully connected to Garmin Connect")
                return True
                
            except Exception as e:
                error_str = str(e)
                logger.error(f"Connection attempt {attempt + 1} failed: {e}")
                
                # Check if it's a rate limit error
                if "429" in error_str or "Too Many Requests" in error_str:
                    if attempt < max_retries - 1:
                        logger.info("Rate limited by Garmin. Will retry with backoff...")
                        continue
                    else:
                        logger.error("Rate limit persists after all retries. Try again later.")
                else:
                    # Not a rate limit - don't retry
                    logger.error("Authentication failed (not rate limit). Check credentials.")
                    return False
        
        return False
    
    def _save_data(self, data: Dict[str, Any], filename: str, date: datetime) -> Path:
        """Save data to local storage with date-based organization."""
        date_dir = DATA_DIR / "raw" / date.strftime("%Y-%m-%d")
        date_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = date_dir / filename
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        logger.info(f"Saved data to {filepath}")
        return filepath
    
    def fetch_daily_stats(self, date: Optional[datetime] = None) -> Dict[str, Any]:
        """Fetch daily health stats for a given date."""
        if not self.client:
            raise RuntimeError("Not connected. Call connect() first.")
        
        date = date or datetime.now()
        date_str = date.strftime("%Y-%m-%d")
        
        logger.info(f"Fetching daily stats for {date_str}")
        
        try:
            stats = self.client.get_stats(date_str)
            self._save_data(stats, "daily_stats.json", date)
            return stats
        except Exception as e:
            logger.error(f"Failed to fetch daily stats: {e}")
            return {}
    
    def fetch_sleep_data(self, date: Optional[datetime] = None) -> Dict[str, Any]:
        """Fetch sleep data for a given date."""
        if not self.client:
            raise RuntimeError("Not connected. Call connect() first.")
        
        date = date or datetime.now()
        date_str = date.strftime("%Y-%m-%d")
        
        logger.info(f"Fetching sleep data for {date_str}")
        
        try:
            sleep = self.client.get_sleep_data(date_str)
            self._save_data(sleep, "sleep_data.json", date)
            return sleep
        except Exception as e:
            logger.error(f"Failed to fetch sleep data: {e}")
            return {}
    
    def fetch_heart_rate(self, date: Optional[datetime] = None) -> Dict[str, Any]:
        """Fetch heart rate data for a given date."""
        if not self.client:
            raise RuntimeError("Not connected. Call connect() first.")
        
        date = date or datetime.now()
        date_str = date.strftime("%Y-%m-%d")
        
        logger.info(f"Fetching heart rate data for {date_str}")
        
        try:
            hr = self.client.get_heart_rates(date_str)
            self._save_data(hr, "heart_rate.json", date)
            return hr
        except Exception as e:
            logger.error(f"Failed to fetch heart rate data: {e}")
            return {}
    
    def fetch_body_battery(self, date: Optional[datetime] = None) -> Dict[str, Any]:
        """Fetch body battery data for a given date."""
        if not self.client:
            raise RuntimeError("Not connected. Call connect() first.")
        
        date = date or datetime.now()
        date_str = date.strftime("%Y-%m-%d")
        
        logger.info(f"Fetching body battery data for {date_str}")
        
        try:
            bb = self.client.get_body_battery(date_str)
            self._save_data(bb, "body_battery.json", date)
            return bb
        except Exception as e:
            logger.error(f"Failed to fetch body battery data: {e}")
            return {}
    
    def fetch_stress(self, date: Optional[datetime] = None) -> Dict[str, Any]:
        """Fetch stress data for a given date."""
        if not self.client:
            raise RuntimeError("Not connected. Call connect() first.")
        
        date = date or datetime.now()
        date_str = date.strftime("%Y-%m-%d")
        
        logger.info(f"Fetching stress data for {date_str}")
        
        try:
            stress = self.client.get_stress_data(date_str)
            self._save_data(stress, "stress_data.json", date)
            return stress
        except Exception as e:
            logger.error(f"Failed to fetch stress data: {e}")
            return {}
    
    def fetch_activities(self, date: Optional[datetime] = None, limit: int = 10) -> list:
        """Fetch recent activities."""
        if not self.client:
            raise RuntimeError("Not connected. Call connect() first.")
        
        date = date or datetime.now()
        
        logger.info(f"Fetching activities (limit: {limit})")
        
        try:
            activities = self.client.get_activities(0, limit)
            self._save_data(activities, "activities.json", date)
            return activities
        except Exception as e:
            logger.error(f"Failed to fetch activities: {e}")
            return []
    
    def fetch_all(self, date: Optional[datetime] = None) -> Dict[str, Any]:
        """Fetch all available data for a given date."""
        date = date or datetime.now()
        
        logger.info(f"Fetching all data for {date.strftime('%Y-%m-%d')}")
        
        return {
            "date": date.strftime("%Y-%m-%d"),
            "daily_stats": self.fetch_daily_stats(date),
            "sleep": self.fetch_sleep_data(date),
            "heart_rate": self.fetch_heart_rate(date),
            "body_battery": self.fetch_body_battery(date),
            "stress": self.fetch_stress(date),
            "activities": self.fetch_activities(date)
        }


def main():
    """Main entry point for CLI usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Fetch Garmin health data")
    parser.add_argument("--date", type=str, help="Date to fetch (YYYY-MM-DD), defaults to today")
    parser.add_argument("--metric", type=str, choices=["all", "stats", "sleep", "hr", "battery", "stress", "activities"],
                       default="all", help="Which metric to fetch")
    
    args = parser.parse_args()
    
    # Parse date
    if args.date:
        date = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        date = datetime.now()
    
    # Connect and fetch
    connector = GarminConnector()
    
    if not connector.connect():
        logger.error("Failed to connect. Check credentials.")
        return 1
    
    if args.metric == "all":
        data = connector.fetch_all(date)
        print(f"Fetched all metrics for {date.strftime('%Y-%m-%d')}")
    elif args.metric == "stats":
        data = connector.fetch_daily_stats(date)
        print(f"Daily stats: {json.dumps(data, indent=2, default=str)}")
    elif args.metric == "sleep":
        data = connector.fetch_sleep_data(date)
        print(f"Sleep data: {json.dumps(data, indent=2, default=str)}")
    elif args.metric == "hr":
        data = connector.fetch_heart_rate(date)
        print(f"Heart rate: {json.dumps(data, indent=2, default=str)}")
    elif args.metric == "battery":
        data = connector.fetch_body_battery(date)
        print(f"Body battery: {json.dumps(data, indent=2, default=str)}")
    elif args.metric == "stress":
        data = connector.fetch_stress(date)
        print(f"Stress: {json.dumps(data, indent=2, default=str)}")
    elif args.metric == "activities":
        data = connector.fetch_activities(date)
        print(f"Activities: {json.dumps(data, indent=2, default=str)}")
    
    return 0


if __name__ == "__main__":
    exit(main())