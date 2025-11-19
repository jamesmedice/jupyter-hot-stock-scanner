import os
import json
import glob

import firebase_admin
from firebase_admin import credentials, storage


def main():
    # Get JSON from secret
    raw = os.environ.get("FIREBASE_SERVICE_ACCOUNT")

    if not raw:
        raise Exception("❌ FIREBASE_SERVICE_ACCOUNT is EMPTY!")

    # Parse JSON
    cred_info = json.loads(raw)
    cred = credentials.Certificate(cred_info)

    # Initialize Firebase
    firebase_admin.initialize_app(cred, {
        "storageBucket": "tpmedici.appspot.com"
    })

    bucket = storage.bucket()
    folder = "market/"

    # folders to upload
    paths = [
        "data/averages/*.csv",
        "data/hotscore/*.csv",
        "output/recommendations/*.csv"
    ]

    for pattern in paths:
        for f in glob.glob(pattern):
            filename = os.path.basename(f)
            blob = bucket.blob(folder + filename)
            blob.upload_from_filename(f)
            print(f"✔ Uploaded {f} → {folder}{filename}")

    print("🎉 All files uploaded successfully.")


if __name__ == "__main__":
    main()
