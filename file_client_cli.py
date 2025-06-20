import socket
import json
import base64
import logging
import os

server_address=('0.0.0.0',7777)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall((command_str + "\r\n\r\n").encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received="" #empty string
        while True:
            #socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
            data = sock.recv(16)
            if data:
                #data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                # no more data, stop the process by break
                break
        # at this point, data_received (string) will contain all data coming from the socket
        # to be able to use the data_received as a dict, need to load it using json.loads()
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except:
        logging.warning("error during data receiving")
        return False

def remote_list():
    command_str=f"LIST"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str=f"GET {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        #proses file dalam bentuk base64 ke bentuk bytes
        namafile= hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile,'wb+')
        fp.write(isifile)
        fp.close()
        return True
    else:
        print("Gagal")
        return False

def remote_upload(filepath=""):
    try:
        with open(filepath, 'rb') as f:
            encoded_content = base64.b64encode(f.read()).decode('utf-8').replace('\n', '').replace('\r', '')
        filename = os.path.basename(filepath)
        command_str = f'UPLOAD {filename} {encoded_content}'
        hasil = send_command(command_str)
        print(hasil)
    except Exception as e:
        print(f"Gagal upload: {str(e)}")

def remote_delete(filename=""):
    hasil = send_command(f"DELETE {filename}")
    print(hasil)

def main_menu():
    while True:
        print("\n=== MENU FILE CLIENT ===")
        print("1. Lihat daftar file (LIST)")
        print("2. Ambil file dari server (GET)")
        print("3. Upload file ke server (UPLOAD)")
        print("4. Hapus file dari server (DELETE)")
        print("5. Keluar")
        pilihan = input("Pilih menu [1-5]: ").strip()
        if pilihan == "1":
            remote_list()
        elif pilihan == "2":
            filename = input("Masukkan nama file yang ingin diambil: ")
            remote_get(filename)
        elif pilihan == "3":
            filepath = input("Masukkan path file lokal untuk diupload: ")
            remote_upload(filepath)
        elif pilihan == "4":
            filename = input("Masukkan nama file yang ingin dihapus dari server: ")
            remote_delete(filename)
        elif pilihan == "5":
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

if __name__ == '__main__':
    server_address=('172.16.16.101',6667)
    main_menu()