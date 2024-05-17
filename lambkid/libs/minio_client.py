import sys
import time
from minio import Minio
from lambkid import log

class MinIO:
    def upload_file(username,minio_url,access_key,secret_key,bucket_name,object_name,file_path,content_type="text/plain;charset=utf-8",max_retry=10):
        for i in range(max_retry):
            log.info(f"begin to run upload file {file_path} to minio server {minio_url}...")
            minio_client = Minio(
                minio_url,
                access_key=access_key,
                secret_key=secret_key,
            )
            try:
                minio_client.fput_object(
                    bucket_name, object_name, file_path,
                    content_type=content_type
                )
                log.info(f"successful to run upload file {file_path} to minio server {minio_url}: OK.")
                time.sleep(5)
            except Exception as e:
                log.error(f"failed to upload file {file_path} to minio server {minio_url}: Error. err msg is :{str(e)}")
            log.info(f"begin to check wheather bucket_name {bucket_name} object_name {object_name} file_path {file_path} is exist...")
            try:
                stat = minio_client.stat_object(bucket_name, object_name)
                log.info(
                    f"s3 file bucket_name {bucket_name} object_name {object_name} file_path {file_path} is exist: OK.")
                sys.exit(0)
            except Exception as e:
                log.warning(
                    f"s3 file bucket_name {bucket_name} object_name {object_name} file_path {file_path} is not exist, err msg is {str(e)} Try once..")
                if i == max_retry-1:
                    sys.exit(f"s3 file bucket_name {bucket_name} object_name {object_name} file_path {file_path} is not exist: Error.err msg is {str(e)}")