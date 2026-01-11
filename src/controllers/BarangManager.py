from typing import Any, List, Optional

from database.query.barang import (
    GetAllBarang,
    GetBarangById,
    GetBarangByPenjual,
)
from database.query.penjual import GetPenjualById


class BarangManager:
    def list_products():
        try:
            return GetAllBarang() or []
        except Exception as e:
            print(f"BarangManager.list_products error: {e}")
            return []

    def get_product(product_id: int):
        try:
            return GetBarangById(product_id)
        except Exception as e:
            print(f"BarangManager.get_product error: {e}")
            return None

    def get_seller(penjual_id: Optional[int]):
        try:
            if penjual_id is None:
                return None
            return GetPenjualById(penjual_id)
        except Exception as e:
            print(f"BarangManager.get_seller error: {e}")
            return None

    def get_by_seller(penjual_id: Optional[int]):
        try:
            if penjual_id is None:
                return []
            return GetBarangByPenjual(penjual_id) or []
        except Exception as e:
            print(f"BarangManager.get_by_seller error: {e}")
            return []

    def get_recommendations(product: Any):
        recs: List[Any] = []
        if product is None:
            return recs

        try:
            if getattr(product, "idPenjual", None):
                recs.extend(
                    [
                        p
                        for p in BarangManager.get_by_seller(product.idPenjual)
                        if getattr(p, "idBarang", None)
                        != getattr(product, "idBarang", None)
                    ]
                )
        except Exception as e:
            print(f"BarangManager.get_recommendations seller error: {e}")

        if len(recs) < 4:
            try:
                for p in BarangManager.list_products():
                    if getattr(p, "idBarang", None) == getattr(
                        product, "idBarang", None
                    ):
                        continue
                    if (
                        getattr(product, "kategori", None)
                        and p.kategori != product.kategori
                    ):
                        continue
                    if p not in recs:
                        recs.append(p)
                    if len(recs) >= 4:
                        break
            except Exception as e:
                print(f"BarangManager.get_recommendations category error: {e}")

        return recs[:4]
