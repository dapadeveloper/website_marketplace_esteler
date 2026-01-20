🍧 Es Teler Fatimah - Smart Point of Sales (POS)
Sistem kasir berbasis web yang modern dan responsif untuk mengelola penjualan Es Teler Premium. Aplikasi ini memiliki dua sisi utama: User Interface untuk pelanggan memesan dan Admin Panel untuk manajemen stok serta laporan keuangan.

🚀 Fitur Utama
Sisi Pengguna (User):

Tampilan kartu produk premium dengan gaya Shopee/E-commerce modern.

Sistem keranjang belanja (Cart System) yang interaktif.

Notifikasi toast saat menambah produk.

Efek visual (balloons) dan pesan sukses saat berhasil melakukan pemesanan.

Sisi Admin (Admin Panel):

Login Aman: Sistem autentikasi admin yang tetap login meski halaman di-refresh.

Laporan Penjualan: Dashboard omzet total, jumlah pesanan, dan riwayat transaksi terbaru.

Cetak Struk: Fitur otomatis generate struk belanja dalam format PDF.

Manajemen Inventori: Fitur Data Editor untuk mengubah harga, stok, dan nama produk secara langsung.

Tambah Produk: Form upload produk baru beserta gambar ke database.

Refresh Real-time: Tombol untuk memperbarui data pesanan yang masuk tanpa memuat ulang seluruh halaman.

Struktur folder
Es-Teler-Fatimah/
├── app.py              # File utama untuk halaman Pemesanan User
├── pages/
│   └── admin.py        # Halaman Dashboard Admin & Inventori
├── Assets/             # Folder penyimpanan foto produk (.jpg, .jpeg, .png)
├── database_menu.csv   # Database produk (otomatis terbuat jika tidak ada)
├── database_pesanan.csv# Database riwayat transaksi pelanggan
└── requirements.txt    # Daftar library yang dibutuhkan

Cara Instalasi
Clone atau Download repository ini.

Pastikan Anda sudah menginstal Python 3.8+.

Buka terminal/command prompt di dalam folder proyek dan instal library yang dibutuhkan:
pip install streamlit pandas fpdf

Jalankan aplikasi:
streamlit run app.py

Informasi Login Admin
URL: Klik menu Admin di sidebar aplikasi.

Username: admin

Password: admin


Teknologi yang Digunakan
Python: Bahasa pemrograman utama.

Streamlit: Framework UI untuk membuat aplikasi web dengan cepat.

Pandas: Untuk pengolahan database berbasis CSV.

FPDF: Library untuk membuat dokumen PDF secara otomatis.

CSS: Kustomisasi tampilan agar terlihat premium dan estetik.


Catatan Penting
Pastikan folder Assets tersedia di direktori utama untuk menyimpan gambar produk.

Database menggunakan file .csv, sehingga data akan tersimpan secara lokal di komputer Anda tanpa memerlukan database SQL yang rumit.

Es Teler Fatimah - The Art of Refreshment.