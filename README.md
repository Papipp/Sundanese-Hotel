🏨 Sistem Reservasi Hotel Sederhana (Flask & Bootstrap)

Sistem Reservasi Hotel sederhana yang dibangun menggunakan Python Flask sebagai backend, Jinja2 untuk templating, dan Bootstrap 5 untuk frontend yang responsif dan menarik.

Aplikasi ini mendukung fungsi pencarian kamar, pemesanan (reservasi), dan panel administrasi lengkap dengan operasi CRUD (Create, Read, Update, Delete) untuk manajemen kamar dan reservasi.

✨ Fitur Utama

Pencarian Kamar Dinamis: Mencari kamar berdasarkan tanggal Check-in, Check-out, dan jumlah tamu.

Validasi Tanggal: Mencegah pemesanan di masa lalu, dan memastikan tanggal check-out selalu setelah check-in.

Reservasi User: Proses pemesanan yang mudah untuk tamu.

Panel Administrasi:

CRUD lengkap untuk manajemen data kamar (Tambah, Lihat, Edit, Hapus).

Input URL Gambar untuk setiap kamar.

Manajemen dan pembatalan reservasi yang ada.

Frontend Responsif: Menggunakan Bootstrap 5 untuk tampilan yang mobile-friendly.

Pola PRG (Post-Redirect-Get): Mencegah browser menampilkan notifikasi "Konfirmasi Pengiriman Ulang Formulir" saat refresh atau back.

📂 Struktur Proyek

reservasi-hotel/
├── app.py              # Logika Utama Flask, Routes, dan Controller
├── models.py           # Simulasi Database (Data Kamar & Reservasi dalam list Python)
├── static/
│   └── css/
│       └── style.css   # CSS Kustom untuk Styling Tambahan
└── templates/
    ├── base.html       # Layout Dasar (Header, Footer, link Bootstrap 5)
    ├── index.html      # Halaman Utama (Cari Kamar & Tampilkan Hasil)
    ├── booking.html    # Halaman Konfirmasi dan Detail Booking
    └── admin/
        ├── login.html  # Halaman Login Admin
        └── dashboard.html # Panel Admin (CRUD Kamar dan Reservasi)


🛠 Instalasi dan Menjalankan Proyek

1. Prasyarat

Pastikan Anda telah menginstal Python 3.x dan pip.

2. Instalasi Flask

Instal framework Flask dan paket-paket lain yang diperlukan:

pip install Flask


3. Menjalankan Aplikasi

Jalankan file utama aplikasi dari direktori proyek:

python app.py


Aplikasi akan berjalan di http://127.0.0.1:5000/.

🔒 Akses Administrator

Akses ke Panel Admin dilindungi oleh sesi sederhana.

URL

Rute

/admin/login

Halaman Login Admin

/admin/dashboard

Dashboard Utama Admin

Kredensial Login

Username

Password

admin

password

⚙️ Pengembangan Lanjutan

Database

Saat ini, data disimpan dalam variabel list Python di models.py. Untuk aplikasi siap produksi, Anda dapat menggantinya dengan:

SQLite/PostgreSQL/MySQL menggunakan SQLAlchemy atau Flask-SQLAlchemy.

Firestore/MongoDB untuk solusi NoSQL.

Validasi

Semua validasi (tanggal, guests) saat ini dilakukan secara sederhana di app.py. Untuk validasi formulir yang lebih kuat, pertimbangkan menggunakan Flask-WTF.
