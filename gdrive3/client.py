import joblib
from pydrive2.fs import GDriveFileSystem
from pydrive2.auth import GoogleAuth
from io import StringIO, BytesIO
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()



class GDrive3:
    '''
    Google Drive Pandas Wrapper

    Note: Google Drive will allow multiple files with the same name in the same directory
    to bypass this files will be read in, deleted on the fs and updated to the fs OR rolled back
    '''
    def __init__(self,verbose=0,landing_bucket_name='datalake-raw') -> None:
        self._verbose = verbose
        self.gdfs = self._auth()
        self.gdfs.find(f'root/{landing_bucket_name}') # Need to define path entry points

    def _auth(self):
        '''
        Automated OAuth2.
        '''
        try:
            client = GDriveFileSystem(
                "root",
                client_id=os.environ.get('GDRIVE_CLIENT_ID'),
                client_secret=os.environ.get('GDRIVE_CLIENT_SECRET'),
                client_json=os.environ.get('GDRIVE_JSON_STRING'),
                trash_only=False,
            )
            return client
        except Exception as e:
            print(e)
            return None

    def get_file(self, key,cols=None):
        try:
            if self._verbose == 1:
                print(f'Getting File from: root/{key}')
            if key.split('.')[-1] == 'csv':
                df_out = pd.read_csv(self.gdfs.open(f'root/{key}'))
            elif key.split('.')[-1] == 'parquet':
                df_out = pd.read_parquet(self.gdfs.open(f'root/{key}'))
            elif key.split('.')[-1] == 'json':
                df_out = pd.read_json(self.gdfs.open(f'root/{key}'))
            else:
                raise Exception(f"Unsupported FileType: {key.split('.')[-1]}")
            df_out = df_out if cols is None else df_out[cols]
            return df_out
        except FileNotFoundError as f:
            if self._verbose == 1:
                print(f)
            return pd.DataFrame()
        except Exception as e:
            raise e

    def get_files(self, key,filter=None,cols=None):
        try:
            keys = self.gdfs.find(f'root/{key}')
            if len(keys) != 0:
                if filter is not None:
                    filtered_keys = []
                    for k in keys:
                        if int(k.replace(f'root/{key}','').split('/')[0]) in filter:
                            filtered_keys.append(k)
                    if len(filtered_keys) != 0:
                        keys = filtered_keys
                    else:
                        return pd.DataFrame()
                dfs = [self.get_file(key.replace('root/', '')) for key in keys]
                df_out = pd.concat(dfs).reset_index().drop(columns='index')
                df_out = df_out if cols is None else df_out[cols]
                return df_out
            else:
                return pd.DataFrame()
        except Exception as e:
            if self._verbose == 1:
                print(e)
            return pd.DataFrame()

    def put_file(self, df, key, mode='upsert',cols=None,dup_cols=None):
        try:
            if mode == 'upsert' and self.gdfs.exists(f'root/{key}'):
                fs_df = self.get_file(key)
                res = self.rm_object(key)
                if dup_cols is None:
                    df = pd.concat([fs_df, df]).drop_duplicates().reset_index().drop(columns='index')
                else:
                    df = pd.concat([fs_df, df]).drop_duplicates(dup_cols,keep='last').reset_index().drop(columns='index')
            elif mode == 'refresh':
                res = self.rm_object(key)
                if not res and self.gdfs.exists(f'root/{key}'):
                    return False
            df = df.loc[:, ~df.columns.duplicated()] ## Remove duplicated column names ['lineopen','lineopen']
            buffer = BytesIO()
            if key.split('.')[-1] == 'csv':
                if cols is None:
                    df.to_csv(buffer, index=False)
                else:
                    df[cols].to_csv(buffer, index=False)
            elif key.split('.')[-1] == 'parquet':
                if cols is None:
                    df.to_parquet(buffer, index=False)
                else:
                    df[cols].to_parquet(buffer, index=False)
            elif key.split('.')[-1] == 'json':
                if cols is None:
                    df.to_json(buffer, index=False)
                else:
                    df[cols].to_json(buffer, index=False)
            else:
                raise Exception(f"Unsupported FileType: {key.split('.')[-1]}")
            self.gdfs.upload_fobj(buffer, f'root/{key}')
            return True
        except Exception as e:
            if self._verbose == 1:
                print(e)
            return False

    def rm_object(self, key):
        try:
            self.gdfs.delete(f'root/{key}')
            return True
        except Exception as e:
            if self._verbose == 1:
                print(e)
            return False

    def get_model(self, key):
        try:
            if key.split('.')[-1] == 'gz':
                fs_model = joblib.load(self.gdfs.open(f'root/{key}'))
            else:
                raise Exception(f"Unsupported ModelType: {key.split('.')[-1]}")
            return fs_model
        except FileNotFoundError as f:
            if self._verbose == 1:
                print(f)
            return None
        except Exception as e:
            raise e

    def put_model(self, model, key):
        try:
            res = self.rm_object(key)
            model_buffer = BytesIO()
            joblib.dump(model, model_buffer)
            self.gdfs.upload_fobj(model_buffer, f'root/{key}')
            return True
        except Exception as e:
            if self._verbose == 1:
                print(e)
            return False

