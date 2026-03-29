#!/usr/bin/env python3
"""
Garmin Connect Token-based Authentication
More reliable than password login, avoids rate limits.
"""

import os
import json
import logging
from pathlib import Path
from getpass import getpass

try:
    from garth.http import Garmin as GarthGarmin
except ImportError:
    print("Installing garth...")
    import subprocess
    subprocess.check_call(["pip", "install", "garth", "-q"])
    from garth.http import Garmin as GarthGarmin

# Setup
TOKEN_DIR = Path(__file__).parent / ".garmin_tokens"
TOKEN_DIR.mkdir(exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def authenticate_with_tokens():
    """Authenticate using stored tokens or create new ones."""
    token_file = TOKEN_DIR / "garmin_tokens.json"
    
    client = GarthGarmin()
    
    # Try to load existing tokens
    if token_file.exists():
        try:
            with open(token_file) as f:
                tokens = json.load(f)
            client.oauth1_token = tokens.get("oauth1")
            client.oauth2_token = tokens.get("oauth2")
            
            # Test if tokens are still valid
            try:
                client.get("https://connect.garmin.com/modern/proxy/userprofile-service/userprofile", params={"_": str(int(os.times().system * 1000))})
                logger.info("✅ Authenticated with existing tokens")
                return client
            except Exception as e:
                logger.info(f"Existing tokens expired: {e}")
        except Exception as e:
            logger.warning(f"Could not load tokens: {e}")
    
    # Need to authenticate with password
    email = os.getenv("GARMIN_EMAIL") or input("Garmin email: ")
    password = os.getenv("GARMIN_PASSWORD") or getpass("Garmin password: ")
    
    logger.info(f"Authenticating as {email}...")
    client.login(email, password)
    
    # Save tokens for future use
    tokens = {
        "oauth1": client.oauth1_token,
        "oauth2": client.oauth2_token
    }
    with open(token_file, 'w') as f:
        json.dump(tokens, f)
    
    logger.info(f"✅ Authenticated and saved tokens to {token_file}")
    return client


def get_garmin_client():
    """Get authenticated Garmin client."""
    return authenticate_with_tokens()


if __name__ == "__main__":
    client = get_garmin_client()
    print("✅ Successfully authenticated with Garmin Connect!")