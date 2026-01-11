import flet as ft
import os

from ..components.navigation_bar import NavigationBar
from ..components.footer_black import Footer_black
from controllers.BarangManager import BarangManager

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
ASSETS_UI = os.path.join(ASSETS_DIR, "ui")
FONT_SFPRO_PATH = os.path.join(ASSETS_DIR, "fonts", "SF-Pro-Display-Regular.otf")


def ProductTradeInPage(page: ft.Page, product_id: int | None = None) -> ft.View:
    page.fonts = {"SFPro": FONT_SFPRO_PATH}

    product = BarangManager.get_product(product_id) if product_id else None
    seller = (
        BarangManager.get_seller(product.idPenjual)
        if product and getattr(product, "idPenjual", None)
        else None
    )

    title = getattr(product, "namaBarang", "Trade In")
    seller_name = getattr(seller, "nama", "Unknown seller")
    phone = getattr(seller, "nomorTelepon", "") or "-"
    email = getattr(seller, "email", "") or "-"
    address = getattr(seller, "alamat", "") or "-"

    info_items = [
        ("Seller", seller_name),
        ("Phone", phone),
        ("Email", email),
        ("Address", address),
    ]

    def info_row(label, value):
        return ft.Row(
            controls=[
                ft.Text(label, size=16, weight=ft.FontWeight.W_700, color="#000000"),
                ft.Container(expand=True),
                ft.Text(value, size=16, color="#000000", selectable=True),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    contact_card = ft.Container(
        bgcolor="#F6F6F6",
        padding=ft.padding.all(24),
        border_radius=20,
        width=600,
        content=ft.Column(
            spacing=16,
            controls=[
                ft.Text(
                    "Trade In Contact",
                    size=24,
                    weight=ft.FontWeight.W_700,
                    color="#000000",
                ),
                ft.Text(f"Product: {title}", size=16, color="#333333"),
                ft.Divider(height=1, color="#E0E0E0"),
                *[info_row(label, value) for label, value in info_items],
            ],
        ),
    )

    nav = NavigationBar(on_nav=lambda r: page.go(r), page=page)
    footer = Footer_black()

    content = ft.Column(
        spacing=30,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_size=30,
                        icon_color="#000000",
                        on_click=lambda e: (
                            page.go(f"/product/{product_id}")
                            if product_id
                            else page.go("/shop")
                        ),
                    ),
                    ft.Text(
                        "Trade In", size=32, weight=ft.FontWeight.W_700, color="#000000"
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            contact_card,
        ],
    )

    return ft.View(
        route="/product_tradein",
        appbar=nav,
        controls=[
            ft.SafeArea(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=content,
                            padding=ft.padding.symmetric(horizontal=40, vertical=30),
                            bgcolor="#FFFFFF",
                            border_radius=ft.border_radius.only(
                                top_left=99, top_right=99
                            ),
                        ),
                        footer,
                    ],
                    spacing=0,
                    expand=True,
                )
            )
        ],
        bgcolor="#161616",
        padding=0,
        scroll=ft.ScrollMode.AUTO,
    )
