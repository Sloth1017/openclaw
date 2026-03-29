#!/usr/bin/env python3
"""
Authenticate with Garmin Connect using browser session cookies,
bypassing the login rate limit entirely.
"""

import requests
import json
import os
from datetime import date, timedelta

COOKIE_STRING = """GMN_TRACKABLE=1; _ga=GA1.1.1390478195.1774367093; _cfuvid=lBLr8.UU4M15Xa2AY0NSLBWaVpanEAe2rDFGYAj8Vfg-1774808496587-0.0.1.1-604800000; TAsessionID=bff7c3fd-ef50-4d1b-bdf2-c9b68ed43b72|NEW; notice_behavior=implied,eu; utag_main__sn=2; utag_main_ses_id=1774808498805%3Bexp-session; utag_main__se=2%3Bexp-session; utag_main__ss=0%3Bexp-session; utag_main__st=1774810388137%3Bexp-session; utag_main__pn=2%3Bexp-session; GARMIN-SSO=1; GARMIN-SSO-CUST-GUID=bcabcc89-517f-4385-9978-88d539e49e4c; session=Fe26.2*1*845fc94efbb5d6265e207086e9fd9b565080e05ab3514664ab2a0c636bb5f647*9V7hPFT3QTdosEEvx1s-uQ*mdLKgj5gOcpo-uMD8IXDlEoIiQfIf8q7LVgi_yVpcmj09lwBTKqtPCFpd7Od0ys8Wnbb0E99cQKNeTUDTPwXXLj_7L8GDcFRRPerFy-3O-jIpZkjlzBEtu53Z9-2J8WAx2O-tDWr33MyJgFSJ7TipfQvlvKEUdaVzOhrFBqDdGvAOEU2g2FYuNao2bRyNd-eDkT7EZNd3NECZ_y0NORIOXDjVjHKXP9B6Uy6b6RWeHUFMGaGboadYR0HLNcNO4kvxCyLOPQJ-eZSzXFIFNr2U2tahD3JSxLPZgTjNEcI2XR9iiPttLOD-xpqklofXTYtY-9T0C56Z-rAjKpOoa7EHJVoAOWDROQfWa-5_eWORAWnsWGXmtkF9cxMLgloYcrBZAJ2PO59fRyX8wOVHsUmPMfd7T6ryVI04rj12vRYBW2k_wi0afDDimrc0Yra7iBbl9ubve2j7BO3jpQ4gCzb1JpC2HdFjOQk_XbbC1vDKCJP5pfSctr29i44RJQxNRigQP42r0XXNs0nvaSESV2yfRuybOea9KyZ4-r4F5GuzCI745Ws_V1HUGhtBUH_KiyAIAL0k20VzSt_UOBiyNXnwNxnqGa6P3gZDgySoa3XOF9z6kWWu61J-DnSa2Q6jJQTCQko1uVzdh4QYped96Ld4sz8W-iO0fJtWvPJsSD01Fdf4llfCVlXrVfKTxNt9rMc5nu_6b4OBqLgYS9W2hagy0WQIb2ZkUg-bGWE64kCOZuUiHpDpIam0D2hTX6yhYKXsTq8T0lD-kpktwy7ko-VrwiSjYxqxGTMNzhEPg0KADX_A8SJy53iZhvrkZ8B-acB3AOPxhSdsCpAjPUs5Ov4LsuszAA6O7gy0blvWtlrpzhe7vsXpQueXr0Vz4op1w5Vj57XyIYOAiI1Rlsm2WkcqI8aJk3sQJqBCU5dyW4eif1wPwFmc14loAbtEV9dD-uxYBC2kf7CH0eKOi_YSao-xoPv3_5HEyyHFF9jOELmXPKilMw-Z7mocl2qYvID2eWm2HDKNfTHfdd_aV0KnGMtrAwjQULfG2lvQDrVSmmfHzLpbzQXdJQp-hDo0ruynJWSgl4AaQjmSm9RKcfdlbFY-WSpM5WDMkNAUSerViVmKISqOY4emSw4vFOo6OOdlFSoRI688_iqWB9-Fwakwq_K103BjT-vbzxzEjHNgYaL-ES0_9VQNP3BGmI_P11t2RNDppUnV80y3-ztF9-tS4XAOXJcNIhIh3WXWoxbimBR_ncZzBd4vpbXWCeeC770hKOkTOb4j9FJRTbwGKTVu2t5CsEFephjNXcD5E0eSetF_dclNW1Orbrn-Yi18EC8dAUTy8iEC_Byh6HEZYNZ0vfuLtRQBTJa6TaLBiyeKaHADX6QALka6AMaP5B-G5ZNUPJjido3zoR_132Mp53m8T5aQ0w5Hf8TWu83u99GWWU2XRuu7dlhbcIZ8MHX2ymfhcIAxQZvFZDlTwFb62ESOqMBa-OGcRdkx8ub2hc-SRaaXrXwmDK8qy8_-9aAX4GLZSb-qvNqeI9E1A2E4asX1VziS0X73Ro42seYb_CyHZh3T3I6ABRwiPOt9uHut2cBEhRHDKGTUh1bdLNUWN9OBvwDMtvMTU-YgOQl28UzRFHTHb_rTG_B5dPbjYVzJp3lxA_ivKf-bpI9dGyeE_FTubmpIlyqPEoRycHbAVob42exS68PFRztgx2Hh1S_8ZaquG1AMaVsDiZRojqJcfOPT_IcnQDdGWlFSwam_9o4s3M-gvx6vevjM6TalUs9R19VLJ_sSIppB7CdxsOXjlUQ0J_TBFI6oryCVNv5-pvJ8JUTYBnBeGlVJ-VfQHswCZLiyZ2AtviLyh8hpSnWkiten3zyvfr8TExrxe5bJK-9MhhdYQurI2L7IDc4pKScANxcPqsxl15nc92TY_kzzkZIxhFEgfHn607KfLs6q3T8cZzBeU9akpkBduikymUasKTF2EGxhq6e01ixhpNqaoUk-MMEZFReYO84BStRfsxTw293WRY91JUlHIXQS-hd2I4oNmrqns2A3UeUG6bpwSHizXgyhT7lSihp1Ye-ldg76l5vvqA_iZYOZCBA_9JUIcF2YbCvuKS9ZPwpf-RBNeiEWRJwuMwGEwYe8XQFdgagj9YIZpMc3RfX3QnZNNSo9BXHFBQloUvd5p3E6P8WBnx7F8TJlFllaWDCSlX4E6CCMmhEKlJ1e2GQoHoiTgjBbVUuPVABBee8kiIpGtKp1EEwL7Be7o3FMD84Pd2nIKSa_BkFmwCSYvdWuEgnD1dKFdydMW1tmqV2zbKi1sfXNr5eFunt0C-cukjVIqnZCitoCZneVfp_-VWbNrSswmTF_JDILJ6kT-v8nyKrZrZaG2PAuWNabkGnQbym7xp4vuiMUt4q1UzJBesrD96yJkV7JPjJq0eDM6Vh3tgpfBcrmaXNqVwW-j67-hDtQ-me4FtTQ3vdu7HDcIxquOzM_ZlKzHOKm-CRi6jA4-kGNRTRBs5OluJCuybs3tsIk1gll12t3UEPJ3JDVE6QKbUPM5idRMjdv2hx2-DP4es-ibCAPB1SbzW40Ji1uOz8f5yzt5vsxlCwBEc*1782007606636*7869598769463e9fce71ed0dcf5133c8292e841affbb098eb201ccbc0cf4baae*HNgbEMx7rSS_Gd0_U3oAgNSwR7mdtcSX6wtu07diZ5Y~2; JWT_WEB=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlcyI6WyI0IiwiNyIsIjgiLCI5IiwiUk9MRV9HQVJNSU5fVVNFUiJdLCJleHAiOjE3NzQ4MTU4MDZ9.f2l4WMMw903cFH6aabt68MWJf7Vv5UD6Kmwnla8R04A; SESSIONID=ZjJiNDM0YzktOGZlYi00YWI4LWEwZGUtYTdkNWFmNDUzNWNh; __cflb=02DiuJLbVZHipNWxN8xjvoq496EBZ92PraZtoeG6JwTsi; CONSENTMGR=c1:1%7Cc2:1%7Cc3:1%7Cc4:1%7Cc5:1%7Cc6:1%7Cc7:1%7Cc8:1%7Cc9:1%7Cc10:1%7Cc11:1%7Cc12:1%7Cc13:1%7Cc14:1%7Cc15:1%7Cts:1774808612984%7Cconsent:true; notice_preferences=2:; notice_gdpr_prefs=0,1,2:; notice_poptime=1619726400000; cmapi_gtm_bl=; cmapi_cookie_privacy=permit 1,2,3; _pk_id.6.e3f4=c5a6ac7b608b6924.1774808615.; _pk_ref.6.e3f4=%5B%22%22%2C%22%22%2C1774808670%2C%22https%3A%2F%2Fsso.garmin.com%2F%22%5D; _ga_DHVMQZ6WGH=GS2.1.s1774808613$o3$g0$t1774808670$j3$l0$h0"""

headers = {
    "Cookie": COOKIE_STRING,
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "NK": "NT",
    "Accept": "application/json",
    "Origin": "https://connect.garmin.com",
    "Referer": "https://connect.garmin.com/",
}

BASE = "https://connectapi.garmin.com"

def test_auth():
    """Quick check — fetch user profile"""
    r = requests.get(f"{BASE}/userprofile-service/socialProfile", headers=headers)
    print(f"Status: {r.status_code}")
    if r.ok:
        data = r.json()
        print(f"✅ Logged in as: {data.get('displayName', data.get('userName', 'unknown'))}")
        return True
    else:
        print(f"❌ Auth failed: {r.text[:300]}")
        return False

def get_activities(limit=20):
    """Fetch recent activities"""
    r = requests.get(
        f"{BASE}/activitylist-service/activities/search/activities",
        headers=headers,
        params={"limit": limit, "start": 0}
    )
    if r.ok:
        activities = r.json()
        print(f"\n✅ Got {len(activities)} activities")
        for a in activities[:5]:
            print(f"  - {a.get('startTimeLocal', '?')} | {a.get('activityName', '?')} | {a.get('activityType', {}).get('typeKey', '?')}")
        return activities
    else:
        print(f"❌ Activities failed: {r.status_code} {r.text[:200]}")
        return []

def get_daily_stats(date_str=None):
    """Fetch daily wellness stats"""
    if not date_str:
        date_str = date.today().strftime("%Y-%m-%d")
    r = requests.get(
        f"{BASE}/wellness-service/wellness/dailySummaryChart/{date_str}",
        headers=headers
    )
    print(f"\nDaily stats ({date_str}): {r.status_code}")
    if r.ok:
        data = r.json()
        print(f"✅ Got daily stats")
        return data
    else:
        print(f"❌ {r.text[:200]}")
        return None

if __name__ == "__main__":
    print("=== Garmin Cookie Auth Test ===\n")
    if test_auth():
        get_activities(limit=5)
        get_daily_stats()
