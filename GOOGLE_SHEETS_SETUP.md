# Google Sheets Setup Guide

## Issue: "Public Spreadsheet cannot be written to"

This error occurs when your Google Sheet is set to "Anyone with the link can view" (read-only mode).

## Solution Options

### Option 1: Make Sheet Editable (Simplest - Recommended for Testing)

1. Open your Google Sheet
2. Click the **"Share"** button (top right)
3. Under "General access", change from **"Viewer"** to **"Editor"**
4. Or change to **"Anyone with the link can edit"**
5. Refresh your Streamlit app
6. Try saving a record again

**Pros:**
- Quick and easy
- No additional setup required
- Good for testing and demos

**Cons:**
- Less secure (anyone with link can edit)
- Not recommended for production with sensitive data

### Option 2: Use Service Account (More Secure - Recommended for Production)

1. **Create Google Cloud Project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one

2. **Enable Google Sheets API:**
   - Navigate to "APIs & Services" → "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

3. **Create Service Account:**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "Service Account"
   - Fill in name (e.g., "swasthya-monitor")
   - Click "Create and Continue"
   - Skip optional steps, click "Done"

4. **Create Key:**
   - Click on the created service account
   - Go to "Keys" tab
   - Click "Add Key" → "Create new key"
   - Choose "JSON" format
   - Download the JSON file

5. **Share Sheet with Service Account:**
   - Open your Google Sheet
   - Click "Share"
   - Add the service account email (found in JSON file, looks like `xxx@xxx.iam.gserviceaccount.com`)
   - Give it "Editor" permission
   - Click "Send"

6. **Add to Streamlit Secrets:**
   - Open `.streamlit/secrets.toml`
   - Add the service account credentials:
   
   ```toml
   [connections.gsheets]
   spreadsheet = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID"
   type = "service_account"
   project_id = "your-project-id"
   private_key_id = "your-private-key-id"
   private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   client_email = "your-service-account@project.iam.gserviceaccount.com"
   client_id = "your-client-id"
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "your-cert-url"
   ```

   **Note:** Copy values from the downloaded JSON file. For `private_key`, keep the `\n` characters.

**Pros:**
- More secure
- Better for production
- Proper authentication

**Cons:**
- More setup steps
- Requires Google Cloud account

## Current Behavior

If write access is not available:
- ✅ App continues to work normally
- ✅ All features function (risk calculation, AI advice, PDF generation)
- ✅ Records are displayed (if readable)
- ⚠️ Records are NOT saved to Google Sheets
- ℹ️ Warning message displayed to user

## Testing Without Google Sheets

The app works completely without Google Sheets:
- All calculations work
- AI advice works
- PDF generation works
- WhatsApp sharing works
- Only data persistence is disabled

You can test all features without configuring Google Sheets!

