# Gmail_detector
Gmail Email Detector 📧
An automated Python application that monitors your Gmail inbox in real-time and notifies you when new emails arrive. Built using the official Gmail API with secure OAuth2 authentication.
Features ✨

Real-time Monitoring: Continuously checks for new unread emails
Secure Authentication: Uses OAuth2 (no password storage required)
Detailed Email Information: Displays subject, sender, date, and preview
Smart Tracking: Avoids duplicate notifications using email ID tracking
Easy to Use: Simple setup with minimal configuration
Auto Token Management: Automatically refreshes expired tokens

Prerequisites 📋

Python 3.6 or higher
A Google account with Gmail
Internet connection

Installation 🚀
1. Clone or Download the Repository
bashgit clone <your-repository-url>
cd gmail-email-detector
2. Install Required Libraries
bashpip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
Or install from requirements file:
bashpip install -r requirements.txt
Setup Google Cloud Console 🔧
Step 1: Create a Google Cloud Project

Go to Google Cloud Console
Click "Select a project" → "NEW PROJECT"
Enter project name (e.g., "Gmail Email Detector")
Click "CREATE"

Step 2: Enable Gmail API

Navigate to "APIs & Services" → "Library"
Search for "Gmail API"
Click on it and press "ENABLE"

Step 3: Configure OAuth Consent Screen

Go to "APIs & Services" → "OAuth consent screen"
Select "External" user type → "CREATE"
Fill in required fields:

App name: Gmail Email Detector
User support email: Your email
Developer contact email: Your email


Click "SAVE AND CONTINUE"

Add Scopes:

Click "ADD OR REMOVE SCOPES"
Search for gmail.readonly
Select: https://www.googleapis.com/auth/gmail.readonly
Click "UPDATE" → "SAVE AND CONTINUE"

Add Test Users:

Click "ADD USERS"
Enter your Gmail address
Click "ADD" → "SAVE AND CONTINUE"

Step 4: Create OAuth Client ID

Go to "APIs & Services" → "Credentials"
Click "+ CREATE CREDENTIALS" → "OAuth client ID"
Application type: Desktop app
Name: Gmail Detector Client
Click "CREATE"

Step 5: Download Credentials

Click "DOWNLOAD JSON" in the popup
Save the file as credentials.json
Place it in the same directory as your Python script
