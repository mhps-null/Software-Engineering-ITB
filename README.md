# YAREU - Your Action to Reuse & Unite

## Penjelasan Singkat Mengenai Aplikasi

YAREU (Your Action to Reuse & Unite)

- **Jual Beli Barang**: Platform marketplace untuk menjual dan membeli barang bekas atau baru
- **Donasi Uang**: Fitur untuk melakukan donasi uang kepada penerima donasi
- **Donasi Barang**: Fitur untuk mendonasikan barang kepada penerima donasi
- **Tukar Tambah**: Sistem untuk melakukan pertukaran atau tukar tambah barang

Aplikasi ini dibangun menggunakan **Flet** (Python) dengan arsitektur **MVC (Model-View-Controller)** dan menggunakan **PostgreSQL** sebagai database.

## Prasyarat dan Instalasi

### Prasyarat

1. **Python**

   - Download dari [python.org](https://www.python.org/downloads/)
   - Pastikan Python sudah terinstall dengan mengecek versi:
     ```bash
     python --version
     ```

2. **PostgreSQL**

   - Pastikan PostgreSQL service berjalan dengan membuatnya terlebih dahulu
   - Default database: `yareu`
   - Default user: `postgres`
   - Default password: `postgres`
   - Default port: `5432`

3.

### Instalasi

1. **Clone repository** (jika belum)

   ```bash
   git clone <repository-url>
   cd IF2150-2025-K01-G03-YAREU
   ```

2. **Buat virtual environment**

   - Windows
     ```powershell
     python -m venv .venv
     ```
   - macOS/Linux
     ```bash
     python3 -m venv .venv
     ```

3. **Aktifkan virtual environment**

   - Windows
     ```powershell
     .venv\Scripts\activate
     ```
   - macOS/Linux
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**

   Menggunakan pip:

   ```bash
   pip install -r requirements.txt
   ```

   Atau menggunakan uv:

   ```bash
   uv pip install -r requirements.txt
   ```

5. **Setup database**
   - Pastikan PostgreSQL sudah berjalan
   - Atau bisa mengubah konfigurasi database di `src/database/connection.py` jika diperlukan

## Cara Menjalankan Aplikasi

### Development Mode

1. **Pastikan virtual environment sudah aktif**

2. **Jalankan aplikasi**

   Menggunakan uv:

   ```bash
   uv run flet run src/views
   ```

   Atau menggunakan flet langsung:

   ```bash
   flet run src/views
   ```

3. **Aplikasi akan terbuka di browser atau window desktop**

### Production

1. Build aplikasi

```bash
flet build windows
```

2. Lalu buka .exe yang telah dihasilkan

### Command Lainnya

Untuk memperbarui `requirements.txt` setelah meng-install dependencies baru:

```bash
pip freeze > requirements.txt
```

Untuk melakukan formatting agar codebase memiliki penulisan yang seragam:

```bash
black .
```

## Daftar Modul yang Diimplementasi

### 2.3.1. Subsistem Donasi

| Nama Modul                    | Jenis      | Penjelasan                                       |
| ----------------------------- | ---------- | ------------------------------------------------ |
| `DonaturEntity`               | Model      | Menyimpan data donatur                           |
| `TransaksiEntity`             | Model      | Menyimpan detail transaksi                       |
| `DonasiUangManager`           | Controller | Mengatur logika terkait donasi uang              |
| `DonateFundsPage`             | View       | Menampilkan informasi donasi uang                |
| `BarangEntity`                | Model      | Menyimpan data barang                            |
| `BarangDonasiEntity`          | Model      | Menyimpan data barang yang telah didonasikan     |
| `DonateGoodsPage`             | View       | Menampilkan informasi donasi barang              |
| `DonasiBarangManager`         | Controller | Mengatur logika terkait donasi barang            |
| `PenerimaDonasiEntity`        | Model      | Menyimpan data penerima donasi                   |
| `TerimaDonasiUangManager`     | Controller | Mengatur logika terkait terima donasi uang       |
| `DonationRecipientDetailPage` | View       | Menampilkan informasi penerimaan donasi uang     |
| `KonfirmasiDonasiManager`     | Controller | Mengatur logika terkait konfirmasi donasi        |
| `DonationPage`                | View       | Menampilkan form konfirmasi donasi               |
| `TerimaDonasiBarangManager`   | Controller | Mengatur logika terkait penerimaan donasi barang |
| `DonationRequestPage`         | View       | Menampilkan form penerimaan donasi barang        |

### 2.3.2. Subsistem Penjualan & Pembelian

| Nama Modul           | Jenis      | Penjelasan                               |
| -------------------- | ---------- | ---------------------------------------- |
| `PenjualEntity`      | Model      | Menyimpan data penjual                   |
| `PenjualanManager`   | Controller | Mengatur logika terkait penjualan        |
| `SellPage`           | View       | Menampilkan form penjualan               |
| `PembeliEntity`      | Model      | Menyimpan data pembeli                   |
| `FullPaymentManager` | Controller | Mengatur logika terkait pembelian        |
| `CheckoutPage`       | View       | Menampilkan form pembayaran full payment |

### 2.3.3. Subsistem Tukar Tambah

| Nama Modul                | Jenis      | Penjelasan                                                    |
| ------------------------- | ---------- | ------------------------------------------------------------- |
| `TukarTambahManager`      | Controller | Mengatur logika terkait tukar tambah                          |
| `ShopPage`                | View       | Menampilkan form tukar tambah                                 |
| `AjuanTukarTambahManager` | Controller | Mengatur logika terkait pengajuan tukar tambah                |
| `ProductDetailPage`       | View       | Menampilkan form dan informasi terkait pengajuan tukar tambah |

### 2.3.4. Subsistem Pengiriman & Penerimaan Barang

| Nama Modul                    | Jenis      | Penjelasan                                                 |
| ----------------------------- | ---------- | ---------------------------------------------------------- |
| `PengirimanManager`           | Controller | Mengatur logika terkait pengiriman barang                  |
| `CheckoutPage`                | View       | Menampilkan form dan informasi terkait pengiriman barang   |
| `KonfirmasiPenerimaanManager` | Controller | Mengatur logika terkait konfirmasi penerimaan barang       |
| `ProfilePage`                 | View       | Menampilkan informasi terkait konfirmasi penerimaan barang |

## Daftar Tabel Basis Data yang Diimplementasi

### 1. PenggunaEntity

Tabel untuk menyimpan data pengguna sistem (autentikasi).

| Atribut        | Tipe Data          | Keterangan              |
| -------------- | ------------------ | ----------------------- |
| `idPengguna`   | INTEGER (PK)       | ID unik pengguna        |
| `nama`         | VARCHAR            | Nama pengguna           |
| `email`        | VARCHAR            | Email pengguna (unique) |
| `password`     | VARCHAR            | Password terenkripsi    |
| `nomorTelepon` | VARCHAR (nullable) | Nomor telepon pengguna  |

### 2. DonaturEntity (C-01)

Tabel untuk menyimpan data donatur.

| Atribut        | Tipe Data          | Keterangan            |
| -------------- | ------------------ | --------------------- |
| `idDonatur`    | INTEGER (PK)       | ID unik donatur       |
| `nama`         | VARCHAR            | Nama donatur          |
| `email`        | VARCHAR (nullable) | Email donatur         |
| `nomorTelepon` | VARCHAR (nullable) | Nomor telepon donatur |

### 3. PenerimaDonasiEntity (C-05)

Tabel untuk menyimpan data penerima donasi.

| Atribut        | Tipe Data          | Keterangan                    |
| -------------- | ------------------ | ----------------------------- |
| `idPenerima`   | INTEGER (PK)       | ID unik penerima donasi       |
| `nama`         | VARCHAR            | Nama penerima donasi          |
| `email`        | VARCHAR (nullable) | Email penerima donasi         |
| `nomorTelepon` | VARCHAR (nullable) | Nomor telepon penerima donasi |
| `alamat`       | VARCHAR (nullable) | Alamat penerima donasi        |

### 4. PenjualEntity (C-06)

Tabel untuk menyimpan data penjual.

| Atribut        | Tipe Data          | Keterangan            |
| -------------- | ------------------ | --------------------- |
| `idPenjual`    | INTEGER (PK)       | ID unik penjual       |
| `nama`         | VARCHAR            | Nama penjual          |
| `email`        | VARCHAR (nullable) | Email penjual         |
| `nomorTelepon` | VARCHAR (nullable) | Nomor telepon penjual |
| `alamat`       | VARCHAR (nullable) | Alamat penjual        |

### 5. PembeliEntity (C-07)

Tabel untuk menyimpan data pembeli.

| Atribut        | Tipe Data          | Keterangan            |
| -------------- | ------------------ | --------------------- |
| `idPembeli`    | INTEGER (PK)       | ID unik pembeli       |
| `nama`         | VARCHAR            | Nama pembeli          |
| `email`        | VARCHAR (nullable) | Email pembeli         |
| `nomorTelepon` | VARCHAR (nullable) | Nomor telepon pembeli |
| `alamat`       | VARCHAR (nullable) | Alamat pembeli        |

### 6. BarangEntity (C-03)

Tabel untuk menyimpan data barang yang dijual.

| Atribut      | Tipe Data          | Keterangan                                |
| ------------ | ------------------ | ----------------------------------------- |
| `idBarang`   | INTEGER (PK)       | ID unik barang                            |
| `namaBarang` | VARCHAR            | Nama barang                               |
| `deskripsi`  | VARCHAR (nullable) | Deskripsi barang                          |
| `kategori`   | VARCHAR (nullable) | Kategori barang                           |
| `foto`       | VARCHAR (nullable) | Path/link foto barang                     |
| `video`      | VARCHAR (nullable) | Path/link video barang                    |
| `idPenjual`  | INTEGER (FK)       | ID penjual (foreign key ke PenjualEntity) |
| `harga`      | INTEGER (nullable) | Harga barang                              |

### 7. BarangDonasiEntity (C-04)

Tabel untuk menyimpan data barang yang didonasikan.

| Atribut          | Tipe Data              | Keterangan                                        |
| ---------------- | ---------------------- | ------------------------------------------------- |
| `idBarangDonasi` | INTEGER (PK)           | ID unik barang donasi                             |
| `namaBarang`     | VARCHAR                | Nama barang donasi                                |
| `deskripsi`      | VARCHAR (nullable)     | Deskripsi barang donasi                           |
| `kategori`       | VARCHAR (nullable)     | Kategori barang donasi                            |
| `idDonatur`      | INTEGER (FK)           | ID donatur (foreign key ke DonaturEntity)         |
| `idPenerima`     | INTEGER (FK, nullable) | ID penerima (foreign key ke PenerimaDonasiEntity) |
| `status`         | VARCHAR                | Status barang donasi (default: "pending")         |
| `caraPengiriman` | VARCHAR (nullable)     | Cara pengiriman barang donasi                     |

### 8. TransaksiEntity (C-02)

Tabel untuk menyimpan data transaksi (jual beli, donasi, tukar tambah).

| Atribut            | Tipe Data              | Keterangan                                                                   |
| ------------------ | ---------------------- | ---------------------------------------------------------------------------- |
| `idTransaksi`      | INTEGER (PK)           | ID unik transaksi                                                            |
| `idBarang`         | INTEGER (FK, nullable) | ID barang (foreign key ke BarangEntity) - untuk jual beli                    |
| `idPembeli`        | INTEGER (FK, nullable) | ID pembeli (foreign key ke PembeliEntity) - untuk jual beli                  |
| `idDonatur`        | INTEGER (FK, nullable) | ID donatur (foreign key ke DonaturEntity) - untuk donasi                     |
| `idPenerima`       | INTEGER (FK, nullable) | ID penerima (foreign key ke PenerimaDonasiEntity) - untuk donasi             |
| `jumlah`           | INTEGER (nullable)     | Jumlah uang (untuk donasi uang atau pembayaran)                              |
| `kuantitas`        | INTEGER (nullable)     | Kuantitas barang                                                             |
| `metodePembayaran` | VARCHAR (nullable)     | Metode pembayaran                                                            |
| `status`           | VARCHAR                | Status transaksi (default: "pending")                                        |
| `jenisTransaksi`   | VARCHAR                | Jenis transaksi: "donasi_uang", "donasi_barang", "jual_beli", "tukar_tambah" |
| `tanggal`          | VARCHAR (nullable)     | Tanggal transaksi                                                            |

### 9. PengirimanEntity (C-08)

Tabel untuk menyimpan data pengiriman.

| Atribut            | Tipe Data          | Keterangan                                    |
| ------------------ | ------------------ | --------------------------------------------- |
| `idPengiriman`     | INTEGER (PK)       | ID unik pengiriman                            |
| `idTransaksi`      | INTEGER (FK)       | ID transaksi (foreign key ke TransaksiEntity) |
| `alamat`           | VARCHAR            | Alamat pengiriman                             |
| `detailAlamat`     | VARCHAR (nullable) | Detail alamat pengiriman                      |
| `kota`             | VARCHAR (nullable) | Kota tujuan pengiriman                        |
| `metodePengiriman` | VARCHAR (nullable) | Metode pengiriman                             |
| `status`           | VARCHAR            | Status pengiriman (default: "pending")        |

## Struktur Codebase

- `controllers/`: Kelas Manager untuk business logic
- `models/`: Kelas Entity dan Schema untuk data models
- `database/`: Koneksi database dan query functions
- `views/`: Kelas Form & Display untuk UI (Flet)
