# progjar-3
Tugas 3 Pemrograman Jaringan (D) 2025 mengimplementasikan sistem **file server dan client berbasis TCP socket** menggunakan Python. Sistem ini mendukung operasi dasar seperti **menampilkan daftar file, mengambil file, mengunggah file, dan menghapus file** dari server. Komunikasi antara client dan server dilakukan menggunakan protokol teks sederhana dan respons dalam format JSON.



## Fitur

- `LIST` — Menampilkan daftar file di server  
- `GET <filename>` — Mengunduh file dari server  
- `UPLOAD <filename> <base64_content>` — Mengunggah file ke server  
- `DELETE <filename>` — Menghapus file dari server  

Semua komunikasi diakhiri dengan delimiter `\r\n\r\n` untuk memisahkan perintah dan respon.



## Cara Menjalankan

### 1. Jalankan Server
```bash
python3 file_server.py
```

### 2. Jalankan Client
```bash
python3 file_client_cli.py
```

Jalankan Server dan Client di dua mesin yang berbeda.