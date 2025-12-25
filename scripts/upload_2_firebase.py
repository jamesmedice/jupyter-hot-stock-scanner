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
upload_folder_local(bucket, "output/hourly", remote_prefix="market/")
upload_folder_local(bucket, "output/daily", remote_prefix="market/")
upload_folder_local(bucket, "output/weekly", remote_prefix="market/")
upload_folder_local(bucket, "output/monthly", remote_prefix="market/")
upload_folder_local(bucket, "output/recommendations", remote_prefix="market/")
upload_folder_local(bucket, "output/top20", remote_prefix="market/")
upload_folder_local(bucket, "output/appearances", remote_prefix="market/")
upload_folder_local(bucket, "output/runtime", remote_prefix="market/")
upload_folder_local(bucket, "output/hotstocks", remote_prefix="market/")
upload_folder_local(bucket, "output/hotscore", remote_prefix="market/")
upload_folder_local(bucket, "output/volumespike", remote_prefix="market/")
upload_folder_local(bucket, "output/momentum", remote_prefix="market/")
upload_folder_local(bucket, "output/periods", remote_prefix="market/")