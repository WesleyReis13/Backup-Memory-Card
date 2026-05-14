import os
import pickle
from pathlib import Path
from dotenv import load_dotenv
import schedule
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

def backup_memory_card():
    #print("Executando backup...")
    load_dotenv()
    file_path = os.getenv("FILE_PATH")
    folder_id = os.getenv("FOLDER_ID")

    SCOPES = ['https://www.googleapis.com/auth/drive.file']

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    drive_service = build('drive', 'v3', credentials=creds)

    pasta = Path(file_path)

    for arquivo in pasta.iterdir():

        if arquivo.is_file():

            file_metadata = {
                'name': arquivo.name,
                'parents': [folder_id]
            }

            media = MediaFileUpload(
                str(arquivo),
                resumable=True
            )

            uploaded_file = drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

            print(f'{arquivo.name} enviado!')


schedule.every().day.at("10:31").do(backup_memory_card)


while True:
    schedule.run_pending()
    time.sleep(1)            