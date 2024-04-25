import csv
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

class CSV(object):
    def __init__(self):
        pass

    def write_csv(self,file_path, head=None, datas=None):
        try:
            with open(file_path, "a+", encoding="utf-8", newline="") as f:
                csv_writer = csv.writer(f)
                if head:
                    csv_writer.writerow(head)
                if datas:
                    csv_writer.writerows(datas)
        except Exception as e:
            log.error(f"failed to write datas to csv: Error.err msg is {str(e)}")