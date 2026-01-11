import flet as ft
import os


def Footer():

    ASSETS_UI = os.path.join(os.path.dirname(__file__), "..", "assets", "ui")
    ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
    ASSETS_UI = os.path.join(ASSETS_DIR, "ui")

    HERO_CURVE_PATH = os.path.join(ASSETS_UI, "hero_curve.png")

    # return ft.Container(
    #     content=ft.Row(
    #         controls=[
    #             ft.Text(
    #                 "© 2024 YAREU. All rights reserved.",
    #                 size=14,
    #                 weight=ft.FontWeight.W_400,
    #                 color="#B3B3B3",
    #             ),
    #         ],
    #         alignment=ft.MainAxisAlignment.CENTER,
    #     ),
    #     width=1200,
    #     padding=ft.padding.symmetric(horizontal=40, vertical=20),
    #     bgcolor="#161616",
    #     border_radius=99,
    #     shadow=ft.BoxShadow(
    #         color="#00000044",
    #         blur_radius=20,
    #         offset=ft.Offset(0, -4),
    #     ),
    # )

    # ASSETS_UI = "assets/ui"

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(height=30),
                ft.Text(
                    "Empowering communities through\ngiving and sharing.",
                    size=28,
                    weight=ft.FontWeight.W_700,
                    font_family="SFPro",
                    color="#000000",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=20),
                ft.Image(
                    src=HERO_CURVE_PATH,
                    height=240,
                    fit=ft.ImageFit.CONTAIN,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
        padding=ft.padding.all(32),
        margin=ft.margin.only(top=30, bottom=0),
        bgcolor="#FFFFFF",
        border_radius=ft.border_radius.only(
            top_left=99,
            top_right=99,
            bottom_left=0,
            bottom_right=0,
        ),
        shadow=ft.BoxShadow(
            color="#00000033",
            blur_radius=20,
            offset=ft.Offset(0, 8),
        ),
        expand=True,
    )
