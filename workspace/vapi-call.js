#!/usr/bin/env node
/**
 * Vapi - Make phone calls
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

const VAPI_CREDENTIALS_PATH = path.join(__dirname, '.secrets', 'vapi-credentials.json');

function loadCredentials() {
  const content = fs.readFileSync(VAPI_CREDENTIALS_PATH, 'utf8');
  return JSON.parse(content);
}

function makeCall(apiKey, phoneNumber, assistantConfig) {
  return new Promise((resolve, reject) => {
    const payload = {
      phoneNumber: {
        twilioPhoneNumber: assistantConfig.twilioNumber || "+13186433296",
        number: phoneNumber
      }
    };
    
    if (assistantConfig.assistantId) {
      payload.assistantId = assistantConfig.assistantId;
    }
    
    if (assistantConfig.overrides) {
      payload.assistantOverrides = assistantConfig.overrides;
    }
    
    const postData = JSON.stringify(payload);
    
    const options = {
      hostname: 'api.vapi.ai',
      port: 443,
      path: '/call',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
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
            reject(new Error(result.error.message || result.error));
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
  
  if (command === 'call') {
    const phoneNumber = args[1];
    const assistantId = args[2];
    
    if (!phoneNumber) {
      console.error('Usage: node vapi-call.js call <phone-number> [assistant-id]');
      process.exit(1);
    }
    
    try {
      const credentials = loadCredentials();
      const result = await makeCall(credentials.api_key, phoneNumber, {
        assistantId: assistantId || undefined,
        twilioNumber: "+13186433296"
      });
      console.log('Call initiated:', result);
    } catch (err) {
      console.error('Error:', err.message);
      process.exit(1);
    }
  } else if (command === 'calisto') {
    // Call Calisto restaurant
    const phoneNumber = "+31203307429";
    const assistantId = "24224850-342f-4c22-b947-e685ddc4fefd";
    
    try {
      const credentials = loadCredentials();
      const result = await makeCall(credentials.api_key, phoneNumber, {
        assistantId: assistantId,
        twilioNumber: "+13186433296",
        overrides: {
          firstMessage: "Hi, I'd like to make a dinner reservation for this Wednesday evening. It's for 2 people, and the name is Greg. Do you have availability around 7 or 7:30 PM?"
        }
      });
      console.log('✓ Call initiated to Calisto');
      console.log('Call ID:', result.id);
      console.log('Status:', result.status);
    } catch (err) {
      console.error('Error:', err.message);
      process.exit(1);
    }
  } else {
    console.log('Usage:');
    console.log('  node vapi-call.js call <phone-number> [assistant-id]');
    console.log('  node vapi-call.js calisto');
  }
}

main();
