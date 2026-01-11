import flet as ft
import os
from ..components.navigation_bar import NavigationBar
from controllers.UserManager import UserManager

# Constants
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
ASSETS_UI = os.path.join(ASSETS_DIR, "ui")
FONT_SFPRO_PATH = os.path.join(ASSETS_DIR, "fonts", "SF-Pro-Display-Regular.otf")

LOGO_PATH = os.path.join(ASSETS_UI, "logo.png")
HERO_CURVE = os.path.join(ASSETS_UI, "hero_curve.png")


def LoginPage(page: ft.Page) -> ft.View:

    page.fonts = {"SFPro": FONT_SFPRO_PATH}

    email_field = ft.Ref[ft.TextField]()
    password_field = ft.Ref[ft.TextField]()

    def handle_sign_in(e):
        email = (email_field.current.value or "").strip() if email_field.current else ""
        password = (
            (password_field.current.value or "").strip()
            if password_field.current
            else ""
        )

        if not email or not password:
            page.open(
                ft.SnackBar(
                    content=ft.Text("Email and password are required."),
                    bgcolor="#FF5252",
                )
            )
            page.update()
            return

        try:
            auth_result = UserManager.authenticate(email, password)
            if auth_result is None:
                page.open(
                    ft.SnackBar(
                        content=ft.Text("Invalid email or password."),
                        bgcolor="#FF5252",
                    )
                )
                page.update()
                return

            pengguna = auth_result.get("pengguna")
            pembeli = auth_result.get("pembeli")
            penjual = auth_result.get("penjual")
            donatur = auth_result.get("donatur")
            penerima = auth_result.get("penerima")

            def store(key, value):
                page.client_storage.set(
                    key, str(value) if value not in (None, "", "None") else ""
                )

            store("idPengguna", getattr(pengguna, "idPengguna", None))
            store("idPembeli", getattr(pembeli, "idPembeli", None))
            store("idPenjual", getattr(penjual, "idPenjual", None))
            store("idDonatur", getattr(donatur, "idDonatur", None))
            store("idPenerima", getattr(penerima, "idPenerima", None))

            page.open(
                ft.SnackBar(
                    content=ft.Text("Login successful."),
                    bgcolor="#00AA00",
                )
            )
            page.update()
            page.go("/profile/general-info")
        except Exception as ex:
            page.open(
                ft.SnackBar(
                    content=ft.Text(f"Login failed: {ex}"),
                    bgcolor="#FF5252",
                )
            )
            page.update()

    def handle_google_sign_in(e):
        # TODO: connect to Google OAuth
        pass

    # I ain't doing google sign in mmf jordhy :>
    def handle_forgot_password(e):
        # TODO: cavigate to password reset page
        pass

    def handle_sign_up(e):
        page.go("/register")

    # LEFT SECTION
    left_section = ft.Container(
        content=ft.Column(
            controls=[
                # ft.Container(height=40),
                ft.Image(
                    src=HERO_CURVE,
                    width=500,
                    fit=ft.ImageFit.CONTAIN,
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Image(
                                src=LOGO_PATH,
                                width=140,
                                height=140,
                                fit=ft.ImageFit.CONTAIN,
                            ),
                            # ft.Text(
                            #     "Yareu",
                            #     size=32,
                            #     weight=ft.FontWeight.W_700,
                            #     font_family="SFPro",
                            #     color="#0088ff",
                            # ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        # spacing=12,
                    ),
                ),
                # ft.Container(height=40),
                ft.Text(
                    "Hi, Welcome Back",
                    size=40,
                    weight=ft.FontWeight.W_700,
                    font_family="SFPro",
                    color="#000000",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=8),
                ft.Text(
                    "Enter your email and password to\naccess your account",
                    size=14,
                    weight=ft.FontWeight.W_400,
                    font_family="SFPro",
                    color="#666666",
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
        ),
        bgcolor="#FFFFFF",
        # border_radius=60,
        # padding=ft.padding.all(60),
        # gradient=ft.LinearGradient(
        #     colors=["#FFFFFF", "#161616"],
        #     begin=ft.alignment.top_center,
        #     end=ft.alignment.bottom_center,
        # ),
        border_radius=ft.border_radius.only(
            top_left=99,
            top_right=99,
        ),
        padding=ft.padding.only(left=40, right=40, top=0, bottom=0),
        expand=True,
    )

    # RIGHT SECTION
    right_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Sign In Account",
                    size=48,
                    weight=ft.FontWeight.W_700,
                    font_family="SFPro",
                    color="#FFFFFF",
                ),
                ft.Container(height=8),
                ft.Text(
                    "Enter your email and password to\naccess your account",
                    size=14,
                    weight=ft.FontWeight.W_400,
                    font_family="SFPro",
                    color="#BDBDBD",
                ),
                ft.Container(height=40),
                # email field
                ft.Column(
                    controls=[
                        ft.Text(
                            "Email",
                            size=14,
                            weight=ft.FontWeight.W_500,
                            font_family="SFPro",
                            color="#FFFFFF",
                        ),
                        ft.Container(height=8),
                        ft.TextField(
                            hint_text="Enter your email",
                            hint_style=ft.TextStyle(
                                color="#666666",
                                size=14,
                                font_family="SFPro",
                            ),
                            text_style=ft.TextStyle(
                                color="#FFFFFF",
                                size=14,
                                font_family="SFPro",
                            ),
                            ref=email_field,
                            border_color="#FFFFFF",
                            focused_border_color="#0088ff",
                            border_radius=28,
                            height=56,
                            content_padding=ft.padding.symmetric(
                                horizontal=24, vertical=16
                            ),
                            cursor_color="#FFFFFF",
                            bgcolor="transparent",
                        ),
                    ],
                    spacing=0,
                ),
                ft.Container(height=20),
                # password field
                ft.Column(
                    controls=[
                        ft.Text(
                            "Password",
                            size=14,
                            weight=ft.FontWeight.W_500,
                            font_family="SFPro",
                            color="#FFFFFF",
                        ),
                        ft.Container(height=8),
                        ft.TextField(
                            hint_text="Enter your password",
                            hint_style=ft.TextStyle(
                                color="#666666",
                                size=14,
                                font_family="SFPro",
                            ),
                            text_style=ft.TextStyle(
                                color="#FFFFFF",
                                size=14,
                                font_family="SFPro",
                            ),
                            password=True,
                            can_reveal_password=True,
                            ref=password_field,
                            border_color="#FFFFFF",
                            focused_border_color="#0088ff",
                            border_radius=28,
                            height=56,
                            content_padding=ft.padding.symmetric(
                                horizontal=24, vertical=16
                            ),
                            cursor_color="#FFFFFF",
                            bgcolor="transparent",
                        ),
                    ],
                    spacing=0,
                ),
                ft.Container(height=12),
                # forgot password link
                ft.Container(
                    content=ft.TextButton(
                        content=ft.Text(
                            "Forgot password?",
                            size=14,
                            weight=ft.FontWeight.W_400,
                            font_family="SFPro",
                            color="#FFFFFF",
                            # underline=True,
                        ),
                        on_click=handle_forgot_password,
                        style=ft.ButtonStyle(
                            overlay_color=ft.Colors.TRANSPARENT,
                            padding=0,
                        ),
                    ),
                    alignment=ft.alignment.center_right,
                ),
                ft.Container(height=24),
                # sign In button
                ft.ElevatedButton(
                    content=ft.Text(
                        "Sign In",
                        size=16,
                        weight=ft.FontWeight.W_600,
                        font_family="SFPro",
                        color="#000000",
                    ),
                    on_click=handle_sign_in,
                    width=float("inf"),
                    height=50,
                    bgcolor="#FFFFFF",
                    color="#000000",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=28),
                        elevation=0,
                    ),
                ),
                ft.Container(height=16),
                ft.Container(height=24),
                # sign Up link
                ft.Row(
                    controls=[
                        ft.Text(
                            "Don't have an account? ",
                            size=14,
                            weight=ft.FontWeight.W_400,
                            font_family="SFPro",
                            color="#BDBDBD",
                        ),
                        ft.TextButton(
                            content=ft.Text(
                                "Sign Up",
                                size=14,
                                weight=ft.FontWeight.W_600,
                                font_family="SFPro",
                                color="#FFFFFF",
                            ),
                            on_click=handle_sign_up,
                            style=ft.ButtonStyle(
                                overlay_color=ft.Colors.TRANSPARENT,
                                padding=0,
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=0,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=0,
        ),
        padding=ft.padding.all(60),
        expand=True,
    )

    login_container = ft.Container(
        content=ft.Row(
            controls=[
                left_section,
                right_section,
            ],
            spacing=0,
            expand=True,
        ),
        # bgcolor="#000000",
        # border_radius=99,
        bgcolor="#161616",
        margin=ft.margin.only(top=30, bottom=0, left=30, right=0),
        expand=True,
    )

    back_button = ft.Container(
        content=ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_size=50,
            icon_color="#FFFFFF",
            on_click=lambda e: page.go("/"),
        ),
        padding=ft.padding.only(left=20, top=30),
    )

    page_content = ft.Column(
        controls=[
            back_button,
            ft.Container(
                content=login_container,
                expand=True,
                alignment=ft.alignment.center,
            ),
        ],
        spacing=0,
        expand=True,
    )

    nav_bar = NavigationBar(
        on_nav=lambda route: page.go(route), active="/login", page=page
    )

    return ft.View(
        route="/login",
        appbar=nav_bar,
        controls=[ft.SafeArea(content=page_content, expand=True)],
        bgcolor="#161616",
        padding=0,
        spacing=0,
    )
