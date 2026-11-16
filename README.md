# Student Data & Grade Processor CLI

Aplikasi command line (CLI) berbasis Python untuk mengelola data nilai dan kehadiran mahasiswa, memvalidasi input, menentukan status kelulusan otomatis, menghitung statistik & ranking, serta mengekspor laporan ke format CSV dan JSON.

Dibuat untuk memenuhi Ujian Tengah Semester (UTS) Mata Kuliah **TK091 - Pemrograman Dasar** (Universitas Amikom Yogyakarta).

## Struktur Program

```text
student-grade-cli/
├── main.py                     # Antarmuka CLI (menu, input/output, logging)
├── student_app/                # Package buatan sendiri
│   ├── __init__.py             # Ekspor fungsi utama package
│   ├── validator.py            # Validasi input, custom exception, deduplikasi NIM
│   ├── analyzer.py             # Penentuan status, filter, ranking, statistik
│   └── storage.py              # Baca/tulis JSON dan ekspor laporan CSV
├── data/
│   └── students_input.json     # Contoh data input mahasiswa (termasuk edge case)
├── output/
│   ├── laporan_mahasiswa.csv   # Contoh hasil ekspor tabel CSV
│   └── hasil_analisis.json     # Contoh hasil ekspor ringkasan analisis JSON
├── requirements.txt            # Keterangan dependency (hanya standard library)
└── README.md                   # Dokumentasi proyek
```

## Package & Dependency

- **Python**: versi 3.10 atau lebih baru.
- **Dependency**: Hanya menggunakan **Python Standard Library** (`csv`, `json`, `logging`, `pathlib`, `operator`). Tidak memerlukan instalasi library eksternal.

## Cara Menjalankan Aplikasi

1. Pastikan Python 3.10+ sudah terpasang:
   ```bash
   python --version
   ```
   *(atau `python3 --version` di Linux/macOS)*

2. Masuk ke folder proyek:
   ```bash
   cd student-grade-cli
   ```

3. *(Opsional)* Buat dan aktifkan virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

4. Jalankan program utama:
   ```bash
   python main.py
   ```

## Fitur Utama

1. **Tampilkan Semua Mahasiswa**: Menampilkan daftar bernomor berisi NIM, nama, prodi, nilai, kehadiran, dan status.
2. **Tambah Mahasiswa Baru**: Menambah data dengan validasi teks tak kosong, nilai & kehadiran bilangan bulat `0–100` (nilai `0` diterima, `True`/teks ditolak), serta penolakan NIM duplikat.
3. **Cari Mahasiswa (NIM)**: Pencarian cepat berdasarkan NIM menggunakan dictionary index.
4. **Prodi Unik & Filter Status**: Menampilkan daftar program studi unik menggunakan `set` dan memfilter mahasiswa berdasarkan status kelulusan.
5. **Ranking & Statistik Nilai**: Mengurutkan mahasiswa tanpa mengubah list asli (`sorted()`), serta menghitung rata-rata, nilai tertinggi/terendah, jumlah lulus, dan rekap per status.
6. **Ekspor Laporan (CSV & JSON)**: Menyimpan hasil ranking ke `output/laporan_mahasiswa.csv` dan ringkasan analisis ke `output/hasil_analisis.json`.

## Aturan Penentuan Status

Evaluasi dilakukan secara berurutan (prioritas dari atas ke bawah):
1. `Kehadiran < 75` → **Peringatan Kehadiran**
2. `Nilai >= 90` dan `Kehadiran >= 90` → **Lulus dengan Pujian**
3. `Nilai >= 80` → **Lulus**
4. `Nilai >= 60` → **Remedial**
5. Selain itu → **Tidak Lulus**
