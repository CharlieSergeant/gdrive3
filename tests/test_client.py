import unittest

from io import StringIO, BytesIO
import pandas as pd
from dotenv import load_dotenv
import os

from gdrive3.client import GDrive3

load_dotenv()


class GDrive3Test(unittest.TestCase):
    def setUp(self):
        self.gdfs = GDrive3(landing_bucket_name='test')

    def test_get_file(self):
        # Create a dummy file on Google Drive for testing
        dummy_file = 'dummy_file.txt'
        dummy_content = 'This is a test file.'

        # Upload the dummy file
        buffer = StringIO(dummy_content)
        self.gdfs.upload_fobj(buffer, f'root/{dummy_file}')

        # Get the file from Google Drive
        file_content = self.gdfs.get_file_content(f'root/{dummy_file}')

        # Check if the content matches
        self.assertEqual(file_content.decode(), dummy_content)

        # Clean up the dummy file
        self.gdfs.delete(f'root/{dummy_file}')

    def test_put_file(self):
        # Create a dummy DataFrame for testing
        data = {'Name': ['John', 'Jane', 'Bob'], 'Age': [30, 25, 35]}
        df = pd.DataFrame(data)

        # Define the key and mode
        key = 'test_file.csv'
        mode = 'upsert'

        # Put the DataFrame as a file on Google Drive
        self.gdfs.put_file(df, key, mode=mode)

        # Get the file from Google Drive
        file_content = self.gdfs.get_file_content(f'root/{key}')

        # Convert the file content to a DataFrame
        df_retrieved = pd.read_csv(BytesIO(file_content))

        # Check if the retrieved DataFrame matches the original DataFrame
        pd.testing.assert_frame_equal(df_retrieved, df)

        # Clean up the test file
        self.gdfs.delete(f'root/{key}')


if __name__ == '__main__':
    unittest.main()