README – Single-Folder Google Drive Uploader (Colab)

This script automatically uploads all files inside a local folder (e.g., runs/rfdetr_nano_traffic) into a single folder in Google Drive (MyDrive).
It is designed for Google Colab and uses OAuth authentication (no Service Account required).

Features

Automatically authenticates with your Google account via Colab.

Ensures the upload target folder is created directly inside MyDrive/root.

Enforces a flat structure: no subfolders are uploaded.

All files are uploaded into one Google Drive folder.

Folder Structure

Local folder (example):

runs/
└── rfdetr_nano_traffic/
    ├── checkpoint.pth
    ├── checkpoint_best_ema.pth
    ├── checkpoint_best_regular.pth
    ├── log.txt
    ├── results.json
    ├── metrics_plot.png
    └── events.out.tfevents...


Google Drive output:

MyDrive/
└── kaggle-upload/
    ├── checkpoint.pth
    ├── checkpoint_best_ema.pth
    ├── checkpoint_best_regular.pth
    ├── log.txt
    ├── results.json
    ├── metrics_plot.png
    └── events.out.tfevents...

Usage in Google Colab
1. Copy the script

Paste the following Python script into a Colab cell:

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
        "parents": ["root"],
    }
    f = drive.files().create(body=folder_metadata, fields="id").execute()
    return f["id"]

TARGET_ID = create_folder_in_root(TARGET_FOLDER_NAME)

# ------------------------------------------------------------
# Upload all files (flat structure)
# ------------------------------------------------------------
def upload_file(path, folder_id):
    metadata = {"name": os.path.basename(path), "parents": [folder_id]}
    media = MediaFileUpload(path, resumable=True)
    result = drive.files().create(
        body=metadata, media_body=media, fields="id"
    ).execute()
    print(f"Uploaded: {path} → {result['id']}")

print("Uploading all files into MyDrive folder:", TARGET_FOLDER_NAME)

for file in os.listdir(LOCAL_FOLDER):
    filepath = os.path.join(LOCAL_FOLDER, file)
    if os.path.isfile(filepath):
        upload_file(filepath, TARGET_ID)

print("\nDONE — all files now inside:  MyDrive /", TARGET_FOLDER_NAME)

2. Run the script

Colab will ask for Google login.

Authorize the requested permissions.

All files will upload to:

MyDrive / kaggle-upload

Requirements

Google Colab environment

googleapiclient library (already available in Colab)

Google Drive API enabled internally by Colab (no manual setup needed)

Notes

This uploader does not include subfolders; only files are uploaded.

If the target folder already exists in MyDrive, it will be reused automatically.

The script avoids service accounts to ensure files go directly to your Drive, not a shared or quota-restricted drive.
