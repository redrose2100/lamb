import csv
from lambkid import log

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