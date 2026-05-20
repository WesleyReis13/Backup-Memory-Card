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
    print("Executando backup...")
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

                if arquivo.name == "Mcd001.ps2":
                    file_id = os.getenv("FILE_ID1")

                elif arquivo.name == "Mcd002.ps2":
                    file_id = os.getenv("FILE_ID2")

                else:
                    continue

            media = MediaFileUpload(
                str(arquivo),
                resumable=True
            )

            uploaded_file = drive_service.files().update(
                fileId=file_id,
                media_body=media,
            ).execute()

            print(f'{arquivo.name} enviado!')


schedule.every().day.at("14:46").do(backup_memory_card)


while True:
    schedule.run_pending()
    time.sleep(1)            