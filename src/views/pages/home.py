import flet as ft
import os
from ..components.navigation_bar import NavigationBar
from ..components.footer import Footer

# Constants
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
ASSETS_UI = os.path.join(ASSETS_DIR, "ui")

# Image paths
# FONT_SFPRO_PATH = "assets/fonts/SF-Pro-Display-Regular.otf"
HERO_CURVE_PATH = os.path.join(ASSETS_UI, "hero_curve.png")


def HomePage(page: ft.Page) -> ft.View:

    # page.fonts = {"SFPro": FONT_SFPRO_PATH}

    hero_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(height=16),
                ft.Image(
                    src=HERO_CURVE_PATH,
                    height=280,
                    fit=ft.ImageFit.CONTAIN,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                ),
                ft.Container(height=20),
                ft.Column(
                    controls=[
                        ft.Text(
                            "Your Action to",
                            size=58,
                            weight=ft.FontWeight.W_400,
                            font_family="SFPro",
                            color="#FFFFFF",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(height=-50),
                        ft.Row(
                            controls=[
                                ft.Text(
                                    "Reuse",
                                    size=58,
                                    weight=ft.FontWeight.W_700,
                                    font_family="SFPro",
                                    color="#0088ff",
                                ),
                                ft.Text(
                                    " & ",
                                    size=58,
                                    weight=ft.FontWeight.W_400,
                                    font_family="SFPro",
                                    color="#FFFFFF",
                                ),
                                ft.Text(
                                    "Unite",
                                    size=58,
                                    weight=ft.FontWeight.W_700,
                                    font_family="SFPro",
                                    color="#0088ff",
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            wrap=True,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                ft.Container(height=160),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
        padding=ft.padding.symmetric(horizontal=24, vertical=36),
        margin=ft.margin.only(top=10, bottom=30),
        border_radius=60,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#1a1a1a", "#161616"],
        ),
        expand=True,
    )

    def info_card(
        title: str, subtitle: str, description: str, *, dark: bool, route: str, page
    ):
        return ft.GestureDetector(
            on_tap=lambda e: page.go(route),
            content=ft.Container(
                col={"xs": 12, "md": 6},
                content=ft.Column(
                    controls=[
                        ft.Text(
                            title,
                            size=40,
                            weight=ft.FontWeight.W_700,
                            font_family="SFPro",
                            color="#0088ff",
                        ),
                        ft.Text(
                            subtitle,
                            size=18,
                            weight=ft.FontWeight.W_600,
                            font_family="SFPro",
                            color="#FFFFFF" if dark else "#000000",
                        ),
                        ft.Text(
                            description,
                            size=14,
                            weight=ft.FontWeight.W_400,
                            font_family="SFPro",
                            color="#BDBDBD" if dark else "#666666",
                        ),
                    ],
                    spacing=12,
                ),
                padding=ft.padding.all(32),
                height=280,
                bgcolor="#2A2A2A" if dark else "#FFFFFF",
                border_radius=50,
                shadow=ft.BoxShadow(
                    color="#00000066" if dark else "#00000033",
                    blur_radius=26,
                    offset=ft.Offset(0, 12),
                ),
            ),
        )

    info_cards = ft.ResponsiveRow(
        columns=12,
        spacing=30,
        run_spacing=20,
        controls=[
            info_card(
                "Shop",
                "Buy, Sell, and Trade Preloved Items",
                (
                    "Explore a trusted marketplace where users can list items for sale, purchase preloved goods, "
                    "or submit trade-in offers. Integrated chat, secure transactions, and item documentation ensure "
                    "a smooth and transparent experience."
                ),
                dark=True,
                route="/shop",
                page=page,
            ),
            info_card(
                "Donation",
                "Donate Money or Goods to Verified Recipients",
                (
                    "Support meaningful causes by donating funds or sending physical goods. Upload item photos, "
                    "submit details easily, and track donation status -- all through a streamlined and accountable system."
                ),
                dark=False,
                route="/donation",
                page=page,
            ),
        ],
    )

    nav_bar = NavigationBar(on_nav=lambda route: page.go(route), active="/", page=page)
    # footer = Footer()
    footer = ft.Container(
        content=Footer(),
        margin=ft.margin.only(top=-150),
    )
    # body = ft.Container(
    #     content=ft.Column(
    #         controls=[hero_section, info_cards, footer],
    #         spacing=30,
    #         horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    #         expand=True,
    #     ),
    #     alignment=ft.alignment.top_center,
    #     padding=ft.padding.symmetric(horizontal=20, vertical=10),
    #     expand=True,
    # )

    need_padding = ft.Container(
        content=ft.Column(
            controls=[hero_section, info_cards],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.top_center,
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        expand=True,
    )

    scrollable_content = ft.Column(
        controls=[
            need_padding,
            ft.Container(height=200, bgcolor="#161616"),
            footer,
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    return ft.View(
        route="/",
        appbar=nav_bar,
        controls=[ft.SafeArea(content=scrollable_content, expand=True)],
        bgcolor="#161616",
        padding=0,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
