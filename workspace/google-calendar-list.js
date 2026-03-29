#!/usr/bin/env node
/**
 * Google Calendar - List events
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const TOKEN_PATH = path.join(__dirname, '.secrets', 'google-calendar-token.json');

function loadTokens() {
  const content = fs.readFileSync(TOKEN_PATH, 'utf8');
  return JSON.parse(content);
}

function refreshAccessToken(tokens) {
  return new Promise((resolve, reject) => {
    const credentials = JSON.parse(fs.readFileSync(path.join(__dirname, '.secrets', 'google-calendar-credentials.json'), 'utf8'));
    const querystring = require('querystring');
    
    const postData = querystring.stringify({
      refresh_token: tokens.refresh_token,
      client_id: credentials.installed.client_id,
      client_secret: credentials.installed.client_secret,
      grant_type: 'refresh_token'
    });
    
    const options = {
      hostname: 'oauth2.googleapis.com',
      port: 443,
      path: '/token',
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': postData.length
      }
    };
    
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const newTokens = JSON.parse(data);
          if (newTokens.error) {
            reject(new Error(newTokens.error_description || newTokens.error));
          } else {
            // Update stored tokens
            const updatedTokens = { ...tokens, ...newTokens };
            fs.writeFileSync(TOKEN_PATH, JSON.stringify(updatedTokens, null, 2));
            resolve(updatedTokens.access_token);
          }
        } catch (e) {
          reject(e);
        }
      });
    });
    
    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

async function getAccessToken() {
  const tokens = loadTokens();
  // Check if token is expired (with 60 second buffer)
  const now = Math.floor(Date.now() / 1000);
  if (tokens.expiry_date && now >= tokens.expiry_date - 60) {
    return await refreshAccessToken(tokens);
  }
  return tokens.access_token;
}

function listEvents(accessToken, timeMin, timeMax) {
  return new Promise((resolve, reject) => {
    const params = new URLSearchParams({
      timeMin: timeMin,
      timeMax: timeMax,
      singleEvents: 'true',
      orderBy: 'startTime'
    });
    
    const options = {
      hostname: 'www.googleapis.com',
      port: 443,
      path: `/calendar/v3/calendars/primary/events?${params.toString()}`,
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    };
    
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.error) {
            reject(new Error(result.error.message));
          } else {
            resolve(result.items || []);
          }
        } catch (e) {
          reject(e);
        }
      });
    });
    
    req.on('error', reject);
    req.end();
  });
}

function formatDate(dateStr) {
  const date = new Date(dateStr);
  return date.toLocaleString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit'
  });
}

// Main
async function main() {
  try {
    const accessToken = await getAccessToken();
    
    // Get the day after tomorrow's date range
    const now = new Date();
    const tomorrow = new Date(now);
    tomorrow.setDate(tomorrow.getDate() + 2);  // Day after tomorrow (Wednesday)
    tomorrow.setHours(0, 0, 0, 0);
    
    const dayAfter = new Date(tomorrow);
    dayAfter.setDate(dayAfter.getDate() + 1);
    
    const timeMin = tomorrow.toISOString();
    const timeMax = dayAfter.toISOString();
    
    const events = await listEvents(accessToken, timeMin, timeMax);
    
    if (events.length === 0) {
      console.log('No events scheduled for tomorrow.');
    } else {
      console.log(`\n📅 Events for ${tomorrow.toDateString()}:\n`);
      events.forEach(event => {
        const start = event.start.dateTime || event.start.date;
        const end = event.end.dateTime || event.end.date;
        const isAllDay = !event.start.dateTime;
        
        if (isAllDay) {
          console.log(`  📌 ${event.summary} (All day)`);
        } else {
          const startTime = new Date(start).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
          const endTime = new Date(end).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
          console.log(`  🕐 ${startTime} - ${endTime}: ${event.summary}`);
        }
        
        if (event.location) {
          console.log(`     📍 ${event.location}`);
        }
      });
    }
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

main();
