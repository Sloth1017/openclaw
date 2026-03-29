#!/usr/bin/env node
/**
 * Google Calendar OAuth helper
 * Run this to generate an auth URL and exchange the code for tokens
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const querystring = require('querystring');

const CREDENTIALS_PATH = path.join(__dirname, '.secrets', 'google-calendar-credentials.json');
const TOKEN_PATH = path.join(__dirname, '.secrets', 'google-calendar-token.json');

// Scopes needed for calendar access
const SCOPES = [
  'https://www.googleapis.com/auth/calendar.readonly',
  'https://www.googleapis.com/auth/calendar.events'
];

function loadCredentials() {
  const content = fs.readFileSync(CREDENTIALS_PATH, 'utf8');
  return JSON.parse(content);
}

function generateAuthUrl(credentials) {
  const { client_id, redirect_uris } = credentials.installed;
  
  const params = querystring.stringify({
    client_id: client_id,
    redirect_uri: redirect_uris[0],
    response_type: 'code',
    scope: SCOPES.join(' '),
    access_type: 'offline',
    prompt: 'consent'
  });
  
  return `https://accounts.google.com/o/oauth2/auth?${params}`;
}

function exchangeCodeForTokens(code, credentials) {
  return new Promise((resolve, reject) => {
    const { client_id, client_secret, redirect_uris } = credentials.installed;
    
    const postData = querystring.stringify({
      code: code,
      client_id: client_id,
      client_secret: client_secret,
      redirect_uri: redirect_uris[0],
      grant_type: 'authorization_code'
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
          const tokens = JSON.parse(data);
          if (tokens.error) {
            reject(new Error(tokens.error_description || tokens.error));
          } else {
            resolve(tokens);
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

function saveTokens(tokens) {
  fs.writeFileSync(TOKEN_PATH, JSON.stringify(tokens, null, 2));
  console.log('Tokens saved to:', TOKEN_PATH);
}

// Main
const args = process.argv.slice(2);
const command = args[0];

if (command === 'auth-url') {
  const credentials = loadCredentials();
  const authUrl = generateAuthUrl(credentials);
  console.log('\nOpen this URL in your browser:');
  console.log(authUrl);
  console.log('\nAfter authorizing, copy the code from the redirect URL and run:');
  console.log('node google-calendar-auth.js exchange <code>');
} else if (command === 'exchange') {
  const code = args[1];
  if (!code) {
    console.error('Usage: node google-calendar-auth.js exchange <code>');
    process.exit(1);
  }
  const credentials = loadCredentials();
  exchangeCodeForTokens(code, credentials)
    .then(tokens => {
      saveTokens(tokens);
      console.log('\n✓ Authentication successful!');
      console.log('Access token expires in:', tokens.expires_in, 'seconds');
    })
    .catch(err => {
      console.error('Error exchanging code:', err.message);
      process.exit(1);
    });
} else {
  console.log('Usage:');
  console.log('  node google-calendar-auth.js auth-url       # Get authorization URL');
  console.log('  node google-calendar-auth.js exchange <code> # Exchange code for tokens');
}
