# lambkid 命令行

## minio 子命令
* lambkid minio upload_file
param content_type is optional, its defalut value is "text/plain;charset=utf-8",other params must given
```bash
lambkid minio upload_file --minio_url xxx.com --access_key xxx --secret_key xxx --bucket_name bucket_nae --object_name object_name --file_path file_path --content_type content_type
```