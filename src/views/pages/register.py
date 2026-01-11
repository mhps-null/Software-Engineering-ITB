import flet as ft
import os
import re
from ..components.navigation_bar import NavigationBar
from controllers.UserManager import UserManager

# constants
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
ASSETS_UI = os.path.join(ASSETS_DIR, "ui")
FONT_SFPRO_PATH = os.path.join(ASSETS_DIR, "fonts", "SF-Pro-Display-Regular.otf")

LOGO_PATH = os.path.join(ASSETS_UI, "logo.png")
HERO_CURVE = os.path.join(ASSETS_UI, "hero_curve.png")


def RegisterPage(page: ft.Page) -> ft.View:

    page.fonts = {"SFPro": FONT_SFPRO_PATH}

    # validation indicators
    password_length_check = ft.Icon(name=ft.Icons.CIRCLE, color="#666666", size=12)
    password_capital_check = ft.Icon(name=ft.Icons.CIRCLE, color="#666666", size=12)
    password_special_check = ft.Icon(name=ft.Icons.CIRCLE, color="#666666", size=12)

    password_length_text = ft.Text(
        "At least 8 characters", size=12, font_family="SFPro", color="#666666"
    )
    password_capital_text = ft.Text(
        "One uppercase letter", size=12, font_family="SFPro", color="#666666"
    )
    password_special_text = ft.Text(
        "One special character", size=12, font_family="SFPro", color="#666666"
    )

    # form fields refs
    name_field = ft.Ref[ft.TextField]()
    city_field = ft.Ref[ft.TextField]()
    address_field = ft.Ref[ft.TextField]()
    phone_field = ft.Ref[ft.TextField]()
    email_field = ft.Ref[ft.TextField]()
    password_field = ft.Ref[ft.TextField]()

    def validate_email(email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def validate_phone(phone):
        # basic phone validation
        pattern = r"^[\d\s\+\-\(\)]+$"
        return (
            re.match(pattern, phone) is not None
            and len(
                phone.replace(" ", "")
                .replace("-", "")
                .replace("(", "")
                .replace(")", "")
                .replace("+", "")
            )
            >= 10
        )

    def validate_password(password):
        has_length = len(password) >= 8
        has_capital = any(c.isupper() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?/~`" for c in password)
        return has_length, has_capital, has_special

    def on_password_change(e):
        password = password_field.current.value or ""
        has_length, has_capital, has_special = validate_password(password)

        # length check
        if has_length:
            password_length_check.name = ft.Icons.CHECK_CIRCLE
            password_length_check.color = "#00C853"
            password_length_text.color = "#00C853"
        else:
            password_length_check.name = ft.Icons.CIRCLE
            password_length_check.color = "#666666"
            password_length_text.color = "#666666"

        # capital check
        if has_capital:
            password_capital_check.name = ft.Icons.CHECK_CIRCLE
            password_capital_check.color = "#00C853"
            password_capital_text.color = "#00C853"
        else:
            password_capital_check.name = ft.Icons.CIRCLE
            password_capital_check.color = "#666666"
            password_capital_text.color = "#666666"

        # special check
        if has_special:
            password_special_check.name = ft.Icons.CHECK_CIRCLE
            password_special_check.color = "#00C853"
            password_special_text.color = "#00C853"
        else:
            password_special_check.name = ft.Icons.CIRCLE
            password_special_check.color = "#666666"
            password_special_text.color = "#666666"

        page.update()

    def handle_sign_up(e):
        errors = []
        name = (name_field.current.value or "").strip() if name_field.current else ""
        email = (email_field.current.value or "").strip() if email_field.current else ""
        phone = (phone_field.current.value or "").strip() if phone_field.current else ""
        city = (city_field.current.value or "").strip() if city_field.current else ""
        address = (
            (address_field.current.value or "").strip() if address_field.current else ""
        )
        password = (
            (password_field.current.value or "").strip()
            if password_field.current
            else ""
        )

        if not name:
            errors.append("Name is required")

        if not email:
            errors.append("Email is required")
        elif not validate_email(email):
            errors.append("Invalid email format")

        if not phone:
            errors.append("Phone number is required")
        elif not validate_phone(phone):
            errors.append("Invalid phone number format")

        if not password:
            errors.append("Password is required")
        else:
            has_length, has_capital, has_special = validate_password(password)
            if not (has_length and has_capital and has_special):
                errors.append("Password does not meet requirements")

        if errors:
            page.open(
                ft.SnackBar(
                    content=ft.Text(" | ".join(errors)),
                    bgcolor="#FF5252",
                )
            )
            page.update()
            return

        try:
            result = UserManager.register_user(
                name=name,
                email=email,
                phone=phone,
                password=password,
                address=address,
                city=city,
            )

            pengguna = result.get("pengguna")
            pembeli = result.get("pembeli")
            penjual = result.get("penjual")
            donatur = result.get("donatur")

            def store(key, value):
                page.client_storage.set(
                    key, str(value) if value not in (None, "", "None") else ""
                )

            store("idPengguna", getattr(pengguna, "idPengguna", None))
            store("idPembeli", getattr(pembeli, "idPembeli", None))
            store("idPenjual", getattr(penjual, "idPenjual", None))
            store("idDonatur", getattr(donatur, "idDonatur", None))

            page.open(
                ft.SnackBar(
                    content=ft.Text("Registration successful. Please sign in."),
                    bgcolor="#00AA00",
                )
            )
            page.update()
            page.go("/login")
        except ValueError as ex:
            page.open(
                ft.SnackBar(
                    content=ft.Text(str(ex)),
                    bgcolor="#FF5252",
                )
            )
            page.update()
        except Exception as ex:
            page.open(
                ft.SnackBar(
                    content=ft.Text(f"Registration failed: {ex}"),
                    bgcolor="#FF5252",
                )
            )
            page.update()

    def handle_sign_in(e):
        page.go("/login")

    # LEFT SECTION
    left_section = ft.Container(
        content=ft.Column(
            controls=[
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
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ),
                ft.Text(
                    "Get Started with Us",
                    size=40,
                    weight=ft.FontWeight.W_700,
                    font_family="SFPro",
                    color="#000000",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=8),
                ft.Text(
                    "Complete these easy steps to\nregister your account",
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
                    "Sign Up Account",
                    size=48,
                    weight=ft.FontWeight.W_700,
                    font_family="SFPro",
                    color="#FFFFFF",
                ),
                ft.Container(height=8),
                ft.Text(
                    "Enter your personal data to\ncreate your account",
                    size=14,
                    weight=ft.FontWeight.W_400,
                    font_family="SFPro",
                    color="#BDBDBD",
                ),
                ft.Container(height=32),
                ft.Container(height=16),
                ft.Container(height=16),
                # name field
                ft.Column(
                    controls=[
                        ft.Text(
                            "Name",
                            size=14,
                            weight=ft.FontWeight.W_500,
                            font_family="SFPro",
                            color="#FFFFFF",
                        ),
                        ft.Container(height=8),
                        ft.TextField(
                            ref=name_field,
                            hint_text="e.g. Stevanus Agust",
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
                ft.Container(height=16),
                # city and address fields
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "City",
                                    size=14,
                                    weight=ft.FontWeight.W_500,
                                    font_family="SFPro",
                                    color="#FFFFFF",
                                ),
                                ft.Container(height=8),
                                ft.TextField(
                                    ref=city_field,
                                    hint_text="",
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
                            expand=True,
                        ),
                        ft.Container(width=16),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Address",
                                    size=14,
                                    weight=ft.FontWeight.W_500,
                                    font_family="SFPro",
                                    color="#FFFFFF",
                                ),
                                ft.Container(height=8),
                                ft.TextField(
                                    ref=address_field,
                                    hint_text="",
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
                            expand=True,
                        ),
                    ],
                    spacing=0,
                ),
                ft.Container(height=16),
                # phone number and email fields
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Phone Number",
                                    size=14,
                                    weight=ft.FontWeight.W_500,
                                    font_family="SFPro",
                                    color="#FFFFFF",
                                ),
                                ft.Container(height=8),
                                ft.TextField(
                                    ref=phone_field,
                                    hint_text="",
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
                            expand=True,
                        ),
                        ft.Container(width=16),
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
                                    ref=email_field,
                                    hint_text="",
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
                            expand=True,
                        ),
                    ],
                    spacing=0,
                ),
                ft.Container(height=16),
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
                            ref=password_field,
                            hint_text="",
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
                            border_color="#FFFFFF",
                            focused_border_color="#0088ff",
                            border_radius=28,
                            height=56,
                            content_padding=ft.padding.symmetric(
                                horizontal=24, vertical=16
                            ),
                            cursor_color="#FFFFFF",
                            bgcolor="transparent",
                            on_change=on_password_change,
                        ),
                    ],
                    spacing=0,
                ),
                ft.Container(height=8),
                # password validation indicators
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                password_length_check,
                                ft.Container(width=8),
                                password_length_text,
                            ],
                            spacing=0,
                        ),
                        ft.Container(height=4),
                        ft.Row(
                            controls=[
                                password_capital_check,
                                ft.Container(width=8),
                                password_capital_text,
                            ],
                            spacing=0,
                        ),
                        ft.Container(height=4),
                        ft.Row(
                            controls=[
                                password_special_check,
                                ft.Container(width=8),
                                password_special_text,
                            ],
                            spacing=0,
                        ),
                    ],
                    spacing=0,
                ),
                ft.Container(height=24),
                # sign up button
                ft.ElevatedButton(
                    content=ft.Text(
                        "Sign Up",
                        size=16,
                        weight=ft.FontWeight.W_600,
                        font_family="SFPro",
                        color="#000000",
                    ),
                    on_click=handle_sign_up,
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
                # sign in link
                ft.Row(
                    controls=[
                        ft.Text(
                            "Already have an account? ",
                            size=14,
                            weight=ft.FontWeight.W_400,
                            font_family="SFPro",
                            color="#BDBDBD",
                        ),
                        ft.TextButton(
                            content=ft.Text(
                                "Sign In",
                                size=14,
                                weight=ft.FontWeight.W_600,
                                font_family="SFPro",
                                color="#FFFFFF",
                            ),
                            on_click=handle_sign_in,
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
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=ft.padding.all(60),
        expand=True,
    )

    register_container = ft.Container(
        content=ft.Row(
            controls=[
                left_section,
                right_section,
            ],
            spacing=0,
            expand=True,
        ),
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
                content=register_container,
                expand=True,
                alignment=ft.alignment.center,
            ),
        ],
        spacing=0,
        expand=True,
    )

    nav_bar = NavigationBar(
        on_nav=lambda route: page.go(route), active="/register", page=page
    )

    return ft.View(
        route="/register",
        appbar=nav_bar,
        controls=[ft.SafeArea(content=page_content, expand=True)],
        bgcolor="#161616",
        padding=0,
        spacing=0,
    )
