import os
import json
import glob
import firebase_admin
from firebase_admin import credentials, storage

def init_firebase():
    cred_info = json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"])
    cred = credentials.Certificate(cred_info)
    firebase_admin.initialize_app(cred, {"storageBucket": "tpmedici.appspot.com"})
    return storage.bucket()

def upload_folder(bucket, local_pattern, remote_folder="market/"):
    """Upload all files matching local_pattern to Firebase under remote_folder"""
    for f in glob.glob(local_pattern, recursive=True):
        filename = os.path.basename(f)
        blob = bucket.blob(remote_folder + filename)
        blob.upload_from_filename(f)
        print(f"Uploaded {f} → {remote_folder}{filename}")

def main():
    if "FIREBASE_SERVICE_ACCOUNT" not in os.environ:
        raise Exception("❌ FIREBASE_SERVICE_ACCOUNT is EMPTY!")
    bucket = init_firebase()
    
    # Upload different local folders
    upload_folder(bucket, "data/averages/*.csv")
    upload_folder(bucket, "data/hotscore/*.csv")
    upload_folder(bucket, "output/recommendations/*.csv")

if __name__ == "__main__":
    main()
