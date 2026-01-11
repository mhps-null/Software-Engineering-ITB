from typing import Optional

from database.query.donatur import GetDonaturByEmail, InsertDonatur
from database.query.pembeli import GetPembeliByEmail, GetPembeliById, InsertPembeli
from database.query.penjual import GetPenjualByEmail, GetPenjualById, InsertPenjual
from database.query.pengguna import GetPenggunaByEmail, GetPenggunaById, InsertPengguna
from database.query.penerima_donasi import GetPenerimaByEmail


class UserManager:

    def get_username(user_id: Optional[int]):
        try:
            if not user_id:
                return None
            pengguna = GetPenggunaById(user_id)
            return pengguna.nama if pengguna else None
        except Exception as e:
            print(f"UserManager.get_username error: {e}")
            return None

    def get_profile(user_id: Optional[int], pembeli_id: Optional[int]):
        pengguna = None
        pembeli = None
        try:
            if user_id:
                pengguna = GetPenggunaById(user_id)
            if pembeli_id:
                pembeli = GetPembeliById(pembeli_id)
        except Exception as e:
            print(f"UserManager.get_profile error: {e}")
        return {"pengguna": pengguna, "pembeli": pembeli}

    def authenticate(email: str, password: str):
        try:
            pengguna = GetPenggunaByEmail(email)
            if pengguna is None or pengguna.password != password:
                return None
            return {
                "pengguna": pengguna,
                "pembeli": GetPembeliByEmail(email),
                "penjual": GetPenjualByEmail(email),
                "donatur": GetDonaturByEmail(email),
                "penerima": GetPenerimaByEmail(email),
            }
        except Exception as e:
            print(f"UserManager.authenticate error: {e}")
            raise

    def register_user(
        name: str,
        email: str,
        phone: str,
        password: str,
        address: str = "",
        city: str = "",
    ):
        try:
            if GetPenggunaByEmail(email) is not None:
                raise ValueError("Email already registered.")

            pengguna = InsertPengguna(
                {
                    "nama": name,
                    "email": email,
                    "password": password,
                    "nomorTelepon": phone,
                }
            )

            alamat = address or city
            pembeli = InsertPembeli(
                {
                    "nama": name,
                    "email": email,
                    "nomorTelepon": phone,
                    "alamat": alamat,
                }
            )
            penjual = InsertPenjual(
                {
                    "nama": name,
                    "email": email,
                    "nomorTelepon": phone,
                    "alamat": alamat,
                }
            )
            donatur = InsertDonatur(
                {
                    "nama": name,
                    "email": email,
                    "nomorTelepon": phone,
                }
            )

            return {
                "pengguna": pengguna,
                "pembeli": pembeli,
                "penjual": penjual,
                "donatur": donatur,
            }
        except Exception as e:
            print(f"UserManager.register_user error: {e}")
            raise
