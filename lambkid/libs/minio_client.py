from minio import Minio
from lambkid import log

class MinIO:
    def upload_file(username,minio_url,access_key,secret_key,bucket_name,object_name,file_path,content_type="text/plain;charset=utf-8"):

        try:
            minio_client = Minio(
                minio_url,
                access_key=access_key,
                secret_key=secret_key,
            )
            minio_client.fput_object(
                bucket_name, object_name, file_path,
                content_type=content_type
            )
            log.info(f"successful to upload file {file_path} to minio server {minio_url}: OK.")
            return True
        except Exception as e:
            log.error(f"failed to upload file {file_path} to minio server {minio_url}: Error. err msg is :{str(e)}")
            return False