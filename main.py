import imaplib
import email
from email.header import decode_header
import time
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os
import base64

class GmailDetector:
    def __init__(self, credentials_file='credentials.json'):
        """
        Initialize Gmail detector using OAuth2
        
        Args:
            credentials_file: Path to your OAuth2 credentials JSON file
        """
        self.credentials_file = credentials_file
        self.service = None
        self.seen_emails = set()
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    def connect(self):
        """Connect to Gmail using OAuth2"""
        try:
            creds = None
            
            # Token file stores access and refresh tokens
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            
            # If no valid credentials, let user log in
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, self.SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Save credentials for next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
            
            self.service = build('gmail', 'v1', credentials=creds)
            print("✓ Connected to Gmail successfully")
            return True
            
        except Exception as e:
            print(f"✗ Connection failed: {str(e)}")
            return False
    
    def decode_text(self, text):
        """Decode base64 encoded text"""
        if text:
            return base64.urlsafe_b64decode(text).decode('utf-8', errors='ignore')
        return ""
    
    def get_email_body(self, payload):
        """Extract email body from payload"""
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body = self.decode_text(part['body']['data'])
                        break
                elif 'parts' in part:
                    body = self.get_email_body(part)
                    if body:
                        break
        elif 'body' in payload and 'data' in payload['body']:
            body = self.decode_text(payload['body']['data'])
        
        return body
    
    def read_email(self, email_id):
        """Read a specific email"""
        try:
            message = self.service.users().messages().get(
                userId='me', 
                id=email_id,
                format='full'
            ).execute()
            
            # Extract headers
            headers = message['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            from_addr = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')
            
            # Extract body
            body = self.get_email_body(message['payload'])
            
            email_data = {
                'id': email_id,
                'subject': subject,
                'from': from_addr,
                'date': date,
                'body': body[:500],  # First 500 chars
                'snippet': message.get('snippet', '')
            }
            
            return email_data
            
        except Exception as e:
            print(f"Error reading email: {str(e)}")
            return None
    
    def check_new_emails(self):
        """Check for new unread emails"""
        try:
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=10
            ).execute()
            
            messages = results.get('messages', [])
            new_emails = []
            
            for message in messages:
                email_id = message['id']
                
                if email_id not in self.seen_emails:
                    email_data = self.read_email(email_id)
                    if email_data:
                        new_emails.append(email_data)
                        self.seen_emails.add(email_id)
            
            return new_emails
            
        except Exception as e:
            print(f"Error checking emails: {str(e)}")
            return []
    
    def monitor_emails(self, interval=30):
        """
        Monitor for new emails continuously
        
        Args:
            interval: Time in seconds between checks
        """
        print(f"\n📧 Starting email monitoring (checking every {interval}s)")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                try:
                    new_emails = self.check_new_emails()
                    
                    if new_emails:
                        print(f"\n🔔 {len(new_emails)} new email(s) detected!")
                        print("=" * 70)
                        
                        for email_data in new_emails:
                            print(f"\nSubject: {email_data['subject']}")
                            print(f"From: {email_data['from']}")
                            print(f"Date: {email_data['date']}")
                            print(f"Preview: {email_data['body'][:200]}...")
                            print("-" * 70)
                    
                    time.sleep(interval)
                    
                except KeyboardInterrupt:
                    raise  # Re-raise to outer except block
                except Exception as e:
                    print(f"Error during monitoring: {str(e)}")
                    time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n✓ Monitoring stopped")
            self.disconnect()
        finally:
            print("✓ Program terminated")
    
    def disconnect(self):
        """Disconnect from Gmail"""
        print("✓ Gmail session closed")

# Example usage 
if __name__ == "__main__":
    # Create detector instance
    detector = GmailDetector(credentials_file='credentials.json')
    
    # Connect and start monitoring
    if detector.connect(): 
        detector.monitor_emails(interval=30) # Check every 30 seconds 
