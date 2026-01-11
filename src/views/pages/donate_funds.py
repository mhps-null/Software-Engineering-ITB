import flet as ft
import os
from ..components.navigation_bar import NavigationBar
from ..components.footer_black import Footer_black
from database.query.penerima_donasi import GetPenerimaById
from controllers.DonasiUangManager import DonasiUangManager

# Constants
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
ASSETS_UI = os.path.join(ASSETS_DIR, "ui")
FONT_SFPRO_PATH = os.path.join(ASSETS_DIR, "fonts", "SF-Pro-Display-Regular.otf")

LOGO_PATH = os.path.join(ASSETS_UI, "logo.png")
HERO_CURVE = os.path.join(ASSETS_UI, "hero_curve.png")


def DonateFundsPage(page: ft.Page, idPenerima: int | None = None) -> ft.View:

    def parse_int(value):
        try:
            return int(str(value))
        except (TypeError, ValueError):
            return None

    recipient_name = "Recipient"
    recipient_address = ""
    owner_id = None
    rec = None
    donation_manager = DonasiUangManager()

    if idPenerima:
        try:
            rec = GetPenerimaById(idPenerima)
            if rec:
                recipient_name = getattr(rec, "nama", recipient_name)
                recipient_address = getattr(rec, "alamat", "") or ""
                owner_id = parse_int(getattr(rec, "idPengguna", None))
        except Exception as ex:
            print(f"DonateFunds recipient load error: {ex}")
    current_uid = parse_int(page.client_storage.get("idPengguna"))
    current_donatur_id = parse_int(page.client_storage.get("idDonatur"))

    # Header with back button and title
    header_section = ft.Container(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_size=50,
                        icon_color="#FFFFFF",
                        on_click=lambda e: page.go("/"),
                    ),
                    padding=ft.padding.only(left=50, top=50),
                ),
                ft.Container(
                    content=ft.Text(
                        "Donate Funds",
                        size=50,
                        weight="bold",
                        color="#FFFFFF",
                        font_family="SFPro",
                    ),
                    padding=ft.padding.only(right=50, top=50),
                ),
            ],
        ),
        padding=ft.padding.only(top=20, bottom=100),
    )

    def info_card(title, children):
        return ft.Container(
            bgcolor="#F6F6F6",
            border_radius=50,
            padding=ft.padding.all(32),
            content=ft.Column(
                controls=[
                    ft.Text(
                        title,
                        size=22,
                        weight=ft.FontWeight.W_700,
                        color="#1A1A1A",
                        font_family="SFPro",
                    ),
                    *children,
                ],
                spacing=24,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
        )

    def make_input(**overrides):
        base = {
            "bgcolor": "#FFFFFF",
            "border_radius": 12,
            "border_color": "#161616",
            "focused_border_color": "#161616",
            "text_style": ft.TextStyle(color="#000000"),
        }
        base.update(overrides)
        return ft.TextField(**base)

    selected = ft.Ref()
    selected.current = "Gopay"
    chipRefs = []
    amount_field = make_input(
        label="Amount*",
        prefix_text="IDR ",
    )
    subtotal_text = ft.Text(
        "IDR 0",
        size=16,
        weight=ft.FontWeight.W_600,
        color="#000000",
    )
    total_text = ft.Text(
        "IDR 0",
        size=20,
        weight=ft.FontWeight.W_700,
        color="#000000",
    )
    summary_ref = ft.Ref[ft.Column]()

    def parse_amount_value():
        raw = amount_field.value or ""
        digits = "".join(ch for ch in raw if ch.isdigit())
        return int(digits) if digits else 0

    def update_amount_display(e=None):
        formatted = f"IDR {parse_amount_value():,}".replace(",", ".")
        subtotal_text.value = formatted
        total_text.value = formatted
        if getattr(subtotal_text, "page", None):
            subtotal_text.update()
        if getattr(total_text, "page", None):
            total_text.update()
        if summary_ref.current:
            summary_ref.current.controls[0].controls[1].value = formatted
            summary_ref.current.controls[2].controls[1].value = formatted
            summary_ref.current.update()

    amount_field.on_change = update_amount_display

    summary_section = ft.Column(
        ref=summary_ref,
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            ft.Row(
                controls=[
                    ft.Text("Subtotal", size=16, color="#000000"),
                    ft.Text(
                        subtotal_text.value,
                        size=16,
                        weight=ft.FontWeight.W_600,
                        color="#000000",
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Divider(color="#DCDCDC"),
            ft.Row(
                controls=[
                    ft.Text(
                        "Total", size=20, weight=ft.FontWeight.W_600, color="#000000"
                    ),
                    ft.Text(
                        total_text.value,
                        size=20,
                        weight=ft.FontWeight.W_700,
                        color="#000000",
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ],
    )

    def handle_donate_click(e):
        if current_uid == None:
            page.open(
                ft.SnackBar(
                    ft.Text("Please log in before making a donation."),
                    bgcolor="#FFAA00",
                )
            )
            page.update()
            return
        amount = parse_amount_value()
        if amount <= 0:
            page.open(
                ft.SnackBar(
                    ft.Text("Please enter a valid donation amount."),
                    bgcolor="#FF4444",
                )
            )
            page.update()
            return
        if owner_id and current_uid and owner_id == current_uid:
            page.open(
                ft.SnackBar(
                    ft.Text("You cannot donate to your own request."),
                    bgcolor="#FFAA00",
                )
            )
            page.update()
            return
        if current_donatur_id is None:
            page.open(
                ft.SnackBar(
                    ft.Text("Please log in as a donor before making a donation."),
                    bgcolor="#FF4444",
                )
            )
            page.update()
            return
        if idPenerima is None:
            page.open(
                ft.SnackBar(
                    ft.Text("Recipient information is missing."),
                    bgcolor="#FF4444",
                )
            )
            page.update()
            return

        try:
            donation_manager.addDonasiUang(
                {
                    "idDonatur": current_donatur_id,
                    "idPenerima": idPenerima,
                    "jumlah": amount,
                    "metodePembayaran": selected.current,
                }
            )
            page.open(
                ft.SnackBar(
                    ft.Text("Donation submitted."),
                    bgcolor="#0066FF",
                )
            )
            page.update()
            page.go("/profile/orders-activity")
        except Exception as ex:
            page.open(
                ft.SnackBar(
                    ft.Text(f"Donation failed: {ex}"),
                    bgcolor="#FF4444",
                )
            )
            page.update()

    def refreshChip():
        for label, chipRef, tRef in chipRefs:
            is_selected = selected.current == label
            if chipRef.current:
                chipRef.current.bgcolor = "#1A1A1A" if is_selected else "#FFFFFF"
                chipRef.current.border = ft.border.all(1, "#1A1A1A")
                chipRef.current.update()
            if tRef.current:
                tRef.current.color = "#FFFFFF" if is_selected else "#1A1A1A"
                tRef.current.update()

    def chip(label):
        containerRef = ft.Ref()
        textRef = ft.Ref()
        chipRefs.append((label, containerRef, textRef))

        def handleChip(e):
            selected.current = label
            refreshChip()

        return ft.Container(
            ref=containerRef,
            on_click=handleChip,
            padding=ft.padding.symmetric(horizontal=18, vertical=10),
            border_radius=25,
            bgcolor="#1A1A1A" if selected.current == label else "#FFFFFF",
            border=ft.border.all(1, "#1A1A1A"),
            content=ft.Text(
                ref=textRef,
                value=label,
                size=14,
                weight=ft.FontWeight.W_600,
                color="#FFFFFF" if selected.current == label else "#1A1A1A",
            ),
            ink=True,
        )

    nav_bar = NavigationBar(
        on_nav=lambda route: page.go(route), active="/donation", page=page
    )

    main_section = ft.Container(
        content=ft.ResponsiveRow(
            columns=12,
            spacing=30,
            controls=[
                ft.Container(
                    col={"xs": 12, "md": 6},
                    content=ft.Column(
                        controls=[
                            info_card(
                                f"01 General Information\n(Recipient: {recipient_name})",
                                [
                                    ft.Text(
                                        "Name*",
                                        size=14,
                                        weight=ft.FontWeight.W_500,
                                        color="#000000",
                                    ),
                                    make_input(hint_text="Full name"),
                                    ft.Text(
                                        "Enter Contact Info",
                                        size=14,
                                        weight=ft.FontWeight.W_500,
                                        color="#000000",
                                    ),
                                    ft.Row(
                                        controls=[
                                            make_input(label="Email*", expand=True),
                                            ft.Container(width=16),
                                            make_input(
                                                label="Phone number*", expand=True
                                            ),
                                        ],
                                        spacing=0,
                                    ),
                                ],
                            ),
                            info_card(
                                "02 Donation Details",
                                [
                                    amount_field,
                                    make_input(
                                        label="Message",
                                        min_lines=2,
                                        max_lines=4,
                                    ),
                                ],
                            ),
                        ],
                        spacing=24,
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    ),
                ),
                ft.Container(
                    col={"xs": 12, "md": 6},
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                bgcolor="#FFFFFF",
                                border_radius=50,
                                padding=ft.padding.all(24),
                                border=ft.border.all(1, "#D9D9D9"),
                                content=ft.Row(
                                    controls=[
                                        ft.Container(
                                            width=90,
                                            height=90,
                                            bgcolor="#F0F0F0",
                                            border_radius=25,
                                            alignment=ft.alignment.center,
                                            content=ft.Icon(
                                                ft.Icons.VOLUNTEER_ACTIVISM,
                                                size=36,
                                                color="#8A8A8A",
                                            ),
                                        ),
                                        ft.Column(
                                            controls=[
                                                ft.Text(
                                                    recipient_name,
                                                    size=18,
                                                    weight=ft.FontWeight.W_600,
                                                    color="#000000",
                                                ),
                                                ft.Text(
                                                    recipient_address
                                                    or "City not specified",
                                                    size=14,
                                                    color="#8A8A8A",
                                                ),
                                            ],
                                            spacing=4,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.START,
                                        ),
                                    ],
                                    spacing=20,
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                            ),
                            info_card(
                                "03 Payment",
                                [
                                    ft.Text(
                                        "Select one payment method*",
                                        size=14,
                                        color="#000000",
                                    ),
                                    ft.Text(
                                        "E-Wallet",
                                        size=14,
                                        weight=ft.FontWeight.W_600,
                                        color="#000000",
                                    ),
                                    ft.Row(
                                        wrap=True,
                                        spacing=12,
                                        controls=[
                                            chip("Gopay"),
                                            chip("DANA"),
                                            chip("OVO"),
                                            chip("Apple"),
                                        ],
                                    ),
                                    ft.Text(
                                        "Transfer",
                                        size=14,
                                        weight=ft.FontWeight.W_600,
                                        color="#000000",
                                    ),
                                    ft.Row(
                                        controls=[
                                            chip("BCA"),
                                            chip("Mandiri"),
                                        ],
                                        spacing=12,
                                    ),
                                ],
                            ),
                            ft.Container(
                                bgcolor="#F6F6F6",
                                border_radius=50,
                                padding=ft.padding.all(32),
                                content=ft.Column(
                                    controls=[
                                        summary_section,
                                        ft.ElevatedButton(
                                            height=56,
                                            text="Donate",
                                            bgcolor="#3A63FF",
                                            color="#FFFFFF",
                                            expand=True,
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(
                                                    radius=40
                                                ),
                                            ),
                                            on_click=handle_donate_click,
                                        ),
                                    ],
                                    spacing=20,
                                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                                ),
                            ),
                        ],
                        spacing=24,
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    ),
                ),
            ],
        ),
        bgcolor="#FFFFFF",
        border_radius=ft.border_radius.only(top_left=99, top_right=99),
        padding=ft.padding.only(left=48, top=48, right=48, bottom=200),
    )

    footer_wrapper = ft.Container(
        content=Footer_black(),
        margin=ft.margin.only(top=-100),
    )

    scrollable_content = ft.Column(
        controls=[
            header_section,
            main_section,
            footer_wrapper,
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    return ft.View(
        appbar=nav_bar,
        route="/donation/funds",
        controls=[ft.SafeArea(content=scrollable_content, expand=True)],
        bgcolor="#161616",
        padding=0,
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
