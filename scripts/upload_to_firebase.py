# scripts/upload_to_firebase.py
import os
import json
import glob
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, storage

def init_bucket():
    raw = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
    if not raw:
        raise RuntimeError("FIREBASE_SERVICE_ACCOUNT empty")
    cred_info = json.loads(raw)
    cred = credentials.Certificate(cred_info)
    firebase_admin.initialize_app(cred, {"storageBucket":"tpmedici.appspot.com"})
    return storage.bucket()

def upload_folder_local(bucket, local_folder, remote_prefix="market/"):
    local_folder = Path(local_folder)
    if not local_folder.exists():
        print(f"Skip, folder not found: {local_folder}")
        return
    for f in local_folder.glob("**/*"):
        if f.is_file():
            rel = f.relative_to(local_folder)
            remote_path = f"{remote_prefix}{local_folder.name}/{rel.as_posix()}"
            blob = bucket.blob(remote_path)
            blob.upload_from_filename(str(f))
            print(f"Uploaded {f} -> {remote_path}")

def main():
    bucket = init_bucket()
    # upload daily, weekly, monthly if present
    upload_folder_local(bucket, "output/daily", remote_prefix="market/")
    upload_folder_local(bucket, "output/weekly", remote_prefix="market/")
    upload_folder_local(bucket, "output/monthly", remote_prefix="market/")
    upload_folder_local(bucket, "output/recommendations", remote_prefix="market/")

if __name__ == "__main__":
    main()
