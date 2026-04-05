# MEMORY.md - Long-Term Memory

## Google Calendar Integration (2026-04-01)

**Status:** ✅ Set up (2nd integration)

**Setup steps completed:**
1. Obtained OAuth client secret JSON from Google Cloud Console
2. Stored in `~/.openclaw/credentials/client_secret_google.json` (server)
3. Generated OAuth authorization URL
4. Authorized on local Mac browser
5. Exchanged auth code for refresh token
6. Stored token in `~/.openclaw/credentials/google_oauth_token.json` (server)
7. Added credentials to `~/.openclaw/openclaw.json` (GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET)

**First booking:**
- Created 45-min "Call with Max" on Wed Apr 1, 2026 at 10:00 AM PST (8:00 PM Amsterdam)
- Invite sent to max@saripolinger.com
- Checked calendar availability via API ✓

**Key files:**
- Client secret: `~/.openclaw/credentials/client_secret_google.json`
- OAuth token: `~/.openclaw/credentials/google_oauth_token.json`
- Config: `~/.openclaw/openclaw.json` (env vars added)

**Scopes granted (Apr 1, 2026):**
- `https://www.googleapis.com/auth/calendar` — read & write
- `https://www.googleapis.com/auth/gmail.readonly` — read-only (no send/modify)

**Capabilities:**
- ✅ Read calendar events
- ✅ Create calendar events
- ✅ Read Gmail inbox
- ❌ Send/modify emails (intentionally read-only)

**Note:** This was the second Google Calendar integration attempt. Keep this working.

## Calendar Events Created (Apr 1, 2026)

**Call with Max** — Wed Apr 1, 10:00–10:45 AM PST
- Invite sent to: max@saripolinger.com
- 45-minute call (business)

**Tessie's Studio Keff Events** (times TBD — need confirmation from Tessie):
- Sat May 2 — Made in the Cave (evening) — estimated 7:00 PM
- Mon May 4 — Sauvage Mondays (daytime) — estimated 2:00 PM
- Mon May 11 — Sauvage Mondays (evening) — estimated 7:00 PM

**Crocton House Wedding Venue Scout** — Fri Apr 4, 10:30–11:30 AM
- Invite sent to: ls.lenascholtz@gmail.com (Lena, Greg's girlfriend)
