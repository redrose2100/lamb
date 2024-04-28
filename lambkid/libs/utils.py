import csv
import json
from pathlib import Path
from lambkid import log

def get_all_files(root_dir, recursive=True, suffix_tuple=()):
    all_files = []
    if Path(root_dir).exists():
        if Path(root_dir).is_dir():
            if recursive:
                for elem in Path(root_dir).glob("**/*"):
                    if Path(elem).is_file():
                        suffix = Path(elem).suffix
                        if not suffix_tuple:
                            all_files.append(elem)
                        else:
                            if suffix in suffix_tuple:
                                all_files.append(elem)
            else:
                for elem in Path(root_dir).iterdir():
                    if Path(elem).is_file():
                        suffix = Path(elem).suffix
                        if not suffix_tuple:
                            all_files.append(elem)
                        else:
                            if suffix in suffix_tuple:
                                all_files.append(elem)
        else:
            all_files.append(root_dir)
    return all_files


def write_csv(file_path, head=None, datas=None):
    try:
        with open(file_path, "a+", encoding="utf-8", newline="") as f:
            csv_writer = csv.writer(f)
            if head:
                csv_writer.writerow(head)
            if datas:
                csv_writer.writerows(datas)
    except Exception as e:
        log.error(f"failed to write datas to csv: Error.err msg is {str(e)}")

def read_csv(file_path):
    datas=[]
    with open(file_path, "r", encoding="utf-8", newline="") as f:
        ctx = csv.reader(f)
        for row in ctx:
            row_list=[row[col] for col in range(2)]
            datas.append(row_list)
    return datas

def read_json(file_path):
    if not Path(file_path).exists():
        log.error(f"json file path {file_path} is not exist, please check...")
        return None
    data=dict()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        log.error(f"failed to load json file {file_path},err msg is {str(e)}")
    finally:
        return data