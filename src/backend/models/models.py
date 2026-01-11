from sqlmodel import SQLModel, Field
from typing import Optional


# C-00 (Untuk keperluan autentikasi)
class PenggunaEntity(SQLModel, table=True):
    idPengguna: Optional[int] = Field(default=None, primary_key=True)
    nama: str
    email: str
    password: str
    nomorTelepon: Optional[str] = None


# C-01
class DonaturEntity(SQLModel, table=True):
    idDonatur: Optional[int] = Field(default=None, primary_key=True)
    nama: str
    email: Optional[str] = None
    nomorTelepon: Optional[str] = None


# C-05
class PenerimaDonasiEntity(SQLModel, table=True):
    idPenerima: Optional[int] = Field(default=None, primary_key=True)
    nama: str
    email: Optional[str] = None
    nomorTelepon: Optional[str] = None
    alamat: Optional[str] = None


# C-06
class PenjualEntity(SQLModel, table=True):
    idPenjual: Optional[int] = Field(default=None, primary_key=True)
    nama: str
    email: Optional[str] = None
    nomorTelepon: Optional[str] = None
    alamat: Optional[str] = None


# C-07
class PembeliEntity(SQLModel, table=True):
    idPembeli: Optional[int] = Field(default=None, primary_key=True)
    nama: str
    email: Optional[str] = None
    nomorTelepon: Optional[str] = None
    alamat: Optional[str] = None


# C-03
class BarangEntity(SQLModel, table=True):
    idBarang: Optional[int] = Field(default=None, primary_key=True)
    namaBarang: str
    deskripsi: Optional[str] = None
    kategori: Optional[str] = None
    foto: Optional[str] = None
    video: Optional[str] = None
    idPenjual: Optional[int] = Field(
        default=None,
        foreign_key="penjualentity.idPenjual"
    )
    harga: Optional[int] = None


# C-04
class BarangDonasiEntity(SQLModel, table=True):
    idBarangDonasi: Optional[int] = Field(default=None, primary_key=True)
    namaBarang: str
    deskripsi: Optional[str] = None
    kategori: Optional[str] = None
    idDonatur: Optional[int] = Field(
        default=None,
        foreign_key="donaturentity.idDonatur"
    )
    idPenerima: Optional[int] = Field(
        default=None,
        foreign_key="penerimadonasientity.idPenerima"
    )
    status: str = "pending"
    caraPengiriman: Optional[str] = None


# C-02
class TransaksiEntity(SQLModel, table=True):
    idTransaksi: Optional[int] = Field(default=None, primary_key=True)
    # Jual Beli
    idBarang: Optional[int] = Field(
        default=None,
        foreign_key="barangentity.idBarang"
    )
    idPembeli: Optional[int] = Field(
        default=None,
        foreign_key="pembelientity.idPembeli"
    )
    # Donasi
    idDonatur: Optional[int] = Field(default=None, foreign_key="donaturentity.idDonatur")
    idPenerima: Optional[int] = Field(default=None, foreign_key="penerimadonasientity.idPenerima")

    jumlah: Optional[int] = None
    kuantitas: Optional[int] = None
    
    metodePembayaran: Optional[str] = None
    status: str = "pending"
    jenisTransaksi: str # "donasi_uang", "donasi_barang", "jual_beli", "tukar_tambah"
    tanggal: Optional[str] = None


# C-08
class PengirimanEntity(SQLModel, table=True):
    idPengiriman: Optional[int] = Field(default=None, primary_key=True)

    idTransaksi: Optional[int] = Field(
        default=None,
        foreign_key="transaksientity.idTransaksi"
    )

    alamat: str
    detailAlamat: Optional[str] = None
    kota: Optional[str] = None
    metodePengiriman: Optional[str] = None
    status: str = "pending"
