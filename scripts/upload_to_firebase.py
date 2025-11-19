import os, json, glob
import firebase_admin
from firebase_admin import credentials, storage

cred_info = json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"])
cred = credentials.Certificate(cred_info)
firebase_admin.initialize_app(cred, {"storageBucket": "tpmedici.appspot.com"})

bucket = storage.bucket()
folder = "market/"


# Recursively find all CSVs in the repo
for f in glob.glob("**/*.csv", recursive=True):
    filename = os.path.basename(f)
    blob = bucket.blob(folder + filename)
    blob.upload_from_filename(f)
    print(f"Uploaded {f} → {folder}{filename}")
