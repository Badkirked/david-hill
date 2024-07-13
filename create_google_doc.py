import pandas as pd
import openai
import pickle
import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive.file']

def rearrange_json(data):
    # Create DataFrame from JSON data
    df1 = pd.DataFrame([data[0]])
    df2 = pd.DataFrame(data[1:])

    # Define new column order with colors next to attributes
    new_columns = [
        'Rack Number', 'Location', 'Bay', 'Rack Brand', 'Rack Dimensions', 'Column', 'Arm', 'Bracing', 
        'Pin', 'Pin Color', 'Clip', 'Clip Color', 'Dyna Bolt', 'Dyna Bolt Color', 'Base', 'Base Color', 
        'Guide Rail', 'Guide Rail Color', 'SWL Chart', 'SWL Chart Color', 'Damaged', 'Damaged Color', 
        'Missing', 'Missing Color', 'Comments'
    ]

    # Reorder DataFrame columns
    df2_reordered = df2[new_columns]

    return df1, df2_reordered

def dataframe_to_markdown(df):
    return df.to_markdown(index=False)

# Load data from output.json
with open('output.json', 'r') as f:
    data = json.load(f)

# Rearrange the JSON data
df1, df2_reordered = rearrange_json(data)

# Generate markdown tables
general_info_table = dataframe_to_markdown(df1)
rack_info_table = dataframe_to_markdown(df2_reordered)

# Combine the tables into a single string
combined_tables = general_info_table + "\n\n" + rack_info_table

# Set up the OpenAI API client
openai.api_key = "sk-proj-VXtxmK5393WW1Q9WHwkpT3BlbkFJpD6PwHRNYfPB5vmCjNvE"

# Function to call OpenAI API
def generate_table_html(markdown_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Convert the following markdown table to HTML:\n\n{markdown_text}"}
        ]
    )
    return response.choices[0].message.content.strip()

# Generate HTML from the markdown tables
html_output = generate_table_html(combined_tables)

# Function to get Google credentials
def get_creds():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_601458169322-oh9e52rp7hoh0slol7vqnfeq362a5s0b.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def create_google_doc(creds, html_content):
    # Create a Google Docs API service
    docs_service = build('docs', 'v1', credentials=creds)

    # Create a new Google Doc
    document = docs_service.documents().create(body={'title': 'HTML Table Document'}).execute()
    document_id = document['documentId']

    # Prepare the request to insert the HTML content as plain text
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1
                },
                'text': html_content
            }
        }
    ]

    # Execute the batch update to insert the HTML content
    docs_service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()

    return document_id

def upload_to_drive(creds, document_id):
    # Create a Google Drive API service
    drive_service = build('drive', 'v3', credentials=creds)

    # Get the file metadata
    file_metadata = {
        'name': 'HTML Table Document',
        'mimeType': 'application/vnd.google-apps.document'
    }

    # Create the file on Google Drive
    drive_service.files().copy(fileId=document_id, body=file_metadata).execute()

def main():
    creds = get_creds()
    document_id = create_google_doc(creds, html_output)
    upload_to_drive(creds, document_id)
    print(f"Document created and uploaded to Drive with ID: {document_id}")

if __name__ == '__main__':
    main()
