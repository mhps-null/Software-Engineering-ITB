import flet as ft
import os
from controllers.UserManager import UserManager


def NavigationBar(on_nav, active: str = "/", page: ft.Page | None = None):
    logo_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "assets",
        "ui",
        "logo.png",
    )

    def convert(value):
        try:
            return int(str(value))
        except (TypeError, ValueError):
            return None

    user_name = None
    if page is not None:
        user_id = convert(page.client_storage.get("idPengguna"))
        user_name = UserManager.get_username(user_id)

    def nav_button(label, route):
        is_active = active == route
        return ft.TextButton(
            label,
            on_click=lambda e: on_nav(route),
            style=ft.ButtonStyle(
                color="#161616" if is_active else "#B3B3B3",
                overlay_color="#e9e9e9",
            ),
        )

    auth_button = []
    if user_name:
        auth_button.append(
            ft.Container(
                content=ft.Text(
                    f"Hi, {user_name}!",
                    size=14,
                    weight=ft.FontWeight.W_600,
                    color="#FFFFFF",
                ),
                padding=ft.padding.symmetric(horizontal=16, vertical=8),
                bgcolor="#0088ff",
                border_radius=99,
                ink=True,
                on_click=lambda e: on_nav("/profile/general-info"),
            )
        )
    else:
        auth_button.extend(
            [
                nav_button("Login", "/login"),
                ft.Container(
                    content=ft.Text(
                        "Register",
                        size=14,
                        weight=ft.FontWeight.W_500,
                        color="#FFFFFF",
                    ),
                    padding=ft.padding.symmetric(horizontal=15, vertical=7),
                    bgcolor="#0088ff",
                    border_radius=99,
                    ink=True,
                    on_click=lambda e: on_nav("/register"),
                ),
            ]
        )

    nav_content = ft.Container(
        content=ft.Row(
            controls=[
                ft.Image(
                    src=logo_path,
                    width=120,
                    height=40,
                    fit=ft.ImageFit.CONTAIN,
                    error_content=ft.Text(
                        "YAREU",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="#0088ff",
                    ),
                ),
                ft.Container(expand=True),
                nav_button("Home", "/"),
                nav_button("Shop", "/shop"),
                nav_button("Donation", "/donation"),
                ft.Container(expand=True),
                *auth_button,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=1400,
        padding=ft.padding.symmetric(horizontal=40, vertical=16),
        bgcolor="#f0f0f0",
        border_radius=99,
        shadow=ft.BoxShadow(
            color="#00000033",
            blur_radius=24,
            spread_radius=0,
            offset=ft.Offset(0, 4),
        ),
    )

    return ft.AppBar(
        bgcolor="transparent",
        surface_tint_color="transparent",
        shadow_color="transparent",
        elevation=0,
        center_title=True,
        toolbar_height=90,
        leading_width=0,
        automatically_imply_leading=False,
        title=nav_content,
        clip_behavior=ft.ClipBehavior.NONE,
    )
