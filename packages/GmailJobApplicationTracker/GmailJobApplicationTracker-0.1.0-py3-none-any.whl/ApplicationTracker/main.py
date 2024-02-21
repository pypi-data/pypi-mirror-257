from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os, pickle
import spacy
from spacy.matcher import PhraseMatcher
import pandas as pd


email_df = pd.DataFrame(columns=['Subject', 'From', 'Date'])

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize the PhraseMatcher
phrase_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

# Phrases to match
phrases = [
    "thank you for applying",
    "thanks for applying",
    "application received",
    "we have received your application",
    "thanks for your application",
    "thank you for your application",
    "acknowledgement of application",
    "thanks for your interest in",
]

# Convert each phrase to a Doc object and add to the matcher
patterns = [nlp.make_doc(text) for text in phrases]
phrase_matcher.add("APPLICATION_ACKNOWLEDGEMENTS", patterns)


def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('../token.pickle'):
        with open('../token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'ApplicationTracker/client_secret_143185963962-uttnaoj357r9cb4mgfibn1phlni74tg5.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('../token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().messages().list(userId='me', maxResults=50).execute()
    messages = results.get('messages', [])

    # Stores fetched email objects
    email_list = []
    print("Fetching emails.")
    if not messages:
        print('No new emails found.')
    else:
        print('Emails Fetched.')
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'], format='metadata', metadataHeaders=['Subject', 'From', 'Date']).execute()
            message_details = {
                'Subject': None,
                'From': None,
                'Date': None
            }
            headers = msg['payload']['headers']
            for header in headers:
                if header['name'] == 'Subject':
                    message_details['Subject'] = header['value']
                elif header['name'] == 'From':
                    message_details['From'] = header['value']
                elif header['name'] == 'Date':
                    message_details['Date'] = header['value']
            email_list.append(message_details)

    for email in email_list:
        subject = email['Subject']
        doc = nlp(subject)
        matches = phrase_matcher(doc)
        if matches:
            print(email)
            email_df.loc[len(email_df)] = email

    print("Exporting to Excel")
    # Specify the Excel file name
    filename = '../application_tracker.xlsx'
    # Save the DataFrame to an Excel file
    email_df.to_excel(filename, index=False, engine='openpyxl')
    print(f'DataFrame is written to Excel File {filename} successfully.')


if __name__ == '__main__':
    main()
