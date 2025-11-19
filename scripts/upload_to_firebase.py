import os
import json
import glob
import re
import datetime
import firebase_admin
from firebase_admin import credentials, storage

# === Configuration ===
upload_files_without_date = True  # True → always upload files without a date, False → skip them

def init_firebase():
    cred_info = json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"])
    cred = credentials.Certificate(cred_info)
    firebase_admin.initialize_app(cred, {"storageBucket": "tpmedici.appspot.com"})
    return storage.bucket()

def upload_folder(bucket, local_pattern, remote_folder="market/"):
    """Upload files matching local_pattern to Firebase under remote_folder.
       Only uploads files with yesterday's date or all if flag is True."""
    
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")

    for f in glob.glob(local_pattern, recursive=True):
        filename = os.path.basename(f)
        
        # Extract YYYYMMDD from filename
        match = re.search(r"(\d{8})", filename)
        if match:
            file_date = match.group(1)
            if file_date != yesterday:
                continue  # skip files not from yesterday
        else:
            if not upload_files_without_date:
                continue  # skip files without a date

        blob = bucket.blob(remote_folder + filename)
        blob.upload_from_filename(f)
        print(f"Uploaded {f} → {remote_folder}{filename}")

def main():
    if "FIREBASE_SERVICE_ACCOUNT" not in os.environ:
        raise Exception("❌ FIREBASE_SERVICE_ACCOUNT is EMPTY!")
    
    bucket = init_firebase()
    
    # Upload different local folders
    upload_folder(bucket, "data/averages/*.csv", remote_folder="market/averages/")
    upload_folder(bucket, "data/daily/*.csv", remote_folder="market/daily/")
    upload_folder(bucket, "data/hotscore/*.csv", remote_folder="market/hotscore/")
    upload_folder(bucket, "output/recommendations/*.csv", remote_folder="market/recommendations/")
    upload_folder(bucket, "output/recommendations/*.png", remote_folder="market/recommendations/")

if __name__ == "__main__":
    main()
