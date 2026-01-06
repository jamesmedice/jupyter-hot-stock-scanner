# scripts/upload_to_firebase.py
import os
import json
import glob
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, storage
import upload_to_firebase
from upload_to_firebase import init_bucket, upload_folder_local, upload_folder_local_withCSV

bucket = init_bucket()
upload_folder_local_withCSV(bucket, "output/trend", remote_prefix="market/")