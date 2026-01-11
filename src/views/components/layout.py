from typing import Sequence

import flet as ft

from .footer import Footer
from .footer_black import Footer_black
from .navigation_bar import NavigationBar


def Layout(
    page: ft.Page, route: str, children: Sequence[ft.Control], bgcolor: str = "#161616"
):
    nav = NavigationBar(on_nav=lambda r: page.go(r), active=route, page=page)
    if route == "/":
        footer = Footer()
    else:
        footer = Footer_black()

    body_column = ft.Column(
        controls=list(children),
        spacing=30,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        expand=True,
    )

    content_column = ft.Column(
        controls=[body_column, footer],
        spacing=30,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        expand=True,
    )

    safe_body = ft.Container(
        content=content_column,
        alignment=ft.alignment.top_center,
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        expand=True,
    )

    return ft.View(
        route=route,
        appbar=nav,
        controls=[ft.SafeArea(content=safe_body, expand=True)],
        bgcolor=bgcolor,
        padding=0,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
