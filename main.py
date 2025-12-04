# ============================================================
# FORCE ALL FILES INTO A SINGLE FOLDER IN MYDRIVE
# ============================================================

import os
from google.colab import auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

auth.authenticate_user()
drive = build("drive", "v3")

LOCAL_FOLDER = "runs/rfdetr_nano_traffic"
TARGET_FOLDER_NAME = "kaggle-upload"   # <--- folder final di MyDrive

# ------------------------------------------------------------
# Create MyDrive folder (always inside root, no exception)
# ------------------------------------------------------------
def create_folder_in_root(name):
    q = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and 'root' in parents"
    r = drive.files().list(q=q, fields="files(id)").execute()
    if r["files"]:
        return r["files"][0]["id"]

    folder_metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": ["root"],        # <–– memastikan di MyDrive, bukan tempat lain
    }
    f = drive.files().create(body=folder_metadata, fields="id").execute()
    return f["id"]

TARGET_ID = create_folder_in_root(TARGET_FOLDER_NAME)

# ------------------------------------------------------------
# Upload all files (since no subfolders)
# ------------------------------------------------------------
def upload_file(path, folder_id):
    metadata = {"name": os.path.basename(path), "parents": [folder_id]}
    media = MediaFileUpload(path, resumable=True)
    result = drive.files().create(
        body=metadata, media_body=media, fields="id"
    ).execute()
    print(f"Uploaded: {path} → {result['id']}")

print("Uploading all files into RFDETR_Models...")

for file in os.listdir(LOCAL_FOLDER):
    filepath = os.path.join(LOCAL_FOLDER, file)
    if os.path.isfile(filepath):
        upload_file(filepath, TARGET_ID)

print("\nDONE — all files now inside:  MyDrive / RFDETR_Models")
