import json
import logging
import shlex

from file_interface import FileInterface

"""
* class FileProtocol bertugas untuk memproses 
data yang masuk, dan menerjemahkannya apakah sesuai dengan
protokol/aturan yang dibuat

* data yang masuk dari client adalah dalam bentuk bytes yang 
pada akhirnya akan diproses dalam bentuk string

* class FileProtocol akan memproses data yang masuk dalam bentuk
string
"""

class FileProtocol:
    def __init__(self):
        self.file = FileInterface()

    def proses_string(self, string_datamasuk=''):
        logging.warning(f"string diproses: {string_datamasuk}")
        try:
            string_datamasuk = string_datamasuk.strip()
            if string_datamasuk.lower().startswith("upload "):
                parts = string_datamasuk.split(" ", 2)
                if len(parts) < 3:
                    return json.dumps(dict(status='ERROR', data='Format UPLOAD tidak lengkap'))
                c_request = parts[0]
                params = [parts[1], parts[2]]
            else:
                parts = string_datamasuk.split(" ", 1)
                c_request = parts[0]
                params = parts[1].split() if len(parts) > 1 else []
            cl = getattr(self.file, c_request.lower())(params)
            return json.dumps(cl)
        except Exception as e:
            return json.dumps(dict(status='ERROR', data=str(e)))

if __name__=='__main__':
    #contoh pemakaian
    fp = FileProtocol()
    print(fp.proses_string("LIST"))
    print(fp.proses_string("GET pokijan.jpg"))