from pydrive2.fs import GDriveFileSystem

from dotenv import load_dotenv
import os
load_dotenv()
if __name__ == "__main__":
    res = GDriveFileSystem(
        "root",
        client_id=os.environ.get('GDRIVE_CLIENT_ID'),
        client_secret = os.environ.get('GDRIVE_CLIENT_SECRET'),
    )