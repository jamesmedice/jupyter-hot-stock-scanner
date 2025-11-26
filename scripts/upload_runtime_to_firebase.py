
import os
import json
import glob
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, storage
from upload_to_firebase import init_bucket, upload_folder_local

bucket = init_bucket()
upload_folder_local(bucket, "output/runtime", remote_prefix="market/")

upload_folder_local(bucket, "output/hotstocks", remote_prefix="market/")
upload_folder_local(bucket, "output/hotscore", remote_prefix="market/")
upload_folder_local(bucket, "output/volumespike", remote_prefix="market/")
upload_folder_local(bucket, "output/momentum", remote_prefix="market/")

