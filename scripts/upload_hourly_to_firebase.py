
import os
import json
import glob
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, storage
from upload_to_firebase import init_bucket, upload_folder_local

bucket = init_bucket()
upload_folder_local(bucket, "output/hourly", remote_prefix="market/")

upload_folder_local(bucket, "output/top20", remote_prefix="market/")
upload_folder_local(bucket, "output/recommendations", remote_prefix="market/")
upload_folder_local(bucket, "output/appearances", remote_prefix="market/")