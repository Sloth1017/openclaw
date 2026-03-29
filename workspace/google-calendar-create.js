#!/usr/bin/env node
/**
 * Google Calendar - Create event
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const TOKEN_PATH = path.join(__dirname, '.secrets', 'google-calendar-token.json');
const CREDENTIALS_PATH = path.join(__dirname, '.secrets', 'google-calendar-credentials.json');

function loadTokens() {
  const content = fs.readFileSync(TOKEN_PATH, 'utf8');
  return JSON.parse(content);
}

function loadCredentials() {
  const content = fs.readFileSync(CREDENTIALS_PATH, 'utf8');
  return JSON.parse(content);
}

function refreshAccessToken(tokens) {
  return new Promise((resolve, reject) => {
    const credentials = loadCredentials();
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
  const now = Math.floor(Date.now() / 1000);
  if (tokens.expiry_date && now >= tokens.expiry_date - 60) {
    return await refreshAccessToken(tokens);
  }
  return tokens.access_token;
}

function createEvent(accessToken, event) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify(event);
    
    const options = {
      hostname: 'www.googleapis.com',
      port: 443,
      path: '/calendar/v3/calendars/primary/events',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
        'Content-Length': postData.length
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
            resolve(result);
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

// Main
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (command === 'reminder') {
    const dateStr = args[1]; // YYYY-MM-DD
    const title = args[2];
    const description = args[3] || '';
    
    if (!dateStr || !title) {
      console.error('Usage: node google-calendar-create.js reminder <YYYY-MM-DD> <title> [description]');
      process.exit(1);
    }
    
    try {
      const accessToken = await getAccessToken();
      
      const event = {
        summary: title,
        description: description,
        start: {
          date: dateStr
        },
        end: {
          date: dateStr
        },
        reminders: {
          useDefault: false,
          overrides: [
            { method: 'popup', minutes: 0 }
          ]
        }
      };
      
      const result = await createEvent(accessToken, event);
      console.log('✓ Reminder created');
      console.log('Event:', result.summary);
      console.log('Date:', result.start.date);
      console.log('Link:', result.htmlLink);
    } catch (err) {
      console.error('Error:', err.message);
      process.exit(1);
    }
  } else {
    console.log('Usage:');
    console.log('  node google-calendar-create.js reminder <YYYY-MM-DD> <title> [description]');
  }
}

main();
