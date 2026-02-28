# scripts/upload_to_firebase.py
import os
import json
import glob
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, storage
import upload_to_firebase
from upload_to_firebase import init_bucket, upload_folder_local

bucket = init_bucket()
# upload daily, weekly, monthly if present
upload_folder_local(bucket, "reports", remote_prefix="market/")