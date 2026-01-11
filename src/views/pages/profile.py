import flet as ft
import os
from ..components.footer_black import Footer_black
from ..components.navigation_bar import NavigationBar
from controllers.UserManager import UserManager
from controllers.BarangManager import BarangManager
from controllers.PenjualanManager import PenjualanManager
from controllers.DonasiBarangManager import DonasiBarangManager
from controllers.DonasiUangManager import DonasiUangManager
from database.query.penerima_donasi import (
    GetPenerimaById,
    GetPenerimaByEmail,
    GetPenerimaByPengguna,
)
from database.query.donatur import GetDonaturByEmail

# Constants
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
ASSETS_UI = os.path.join(ASSETS_DIR, "ui")
FONT_SFPRO_PATH = os.path.join(ASSETS_DIR, "fonts", "SF-Pro-Display-Regular.otf")

LOGO_PATH = os.path.join(ASSETS_UI, "logo.png")
HERO_CURVE = os.path.join(ASSETS_UI, "hero_curve.png")


def ProfilePage(page: ft.Page, active_tab="general-info") -> ft.View:
    page.fonts = {"SFPro": FONT_SFPRO_PATH}

    try:
        user_id = int(str(page.client_storage.get("idPengguna")))
    except (TypeError, ValueError):
        user_id = None
    try:
        pembeli_id = int(str(page.client_storage.get("idPembeli")))
    except (TypeError, ValueError):
        pembeli_id = None
    try:
        penjual_id = int(str(page.client_storage.get("idPenjual")))
    except (TypeError, ValueError):
        penjual_id = None
    try:
        donatur_id = int(str(page.client_storage.get("idDonatur")))
    except (TypeError, ValueError):
        donatur_id = None
    try:
        penerima_id = int(str(page.client_storage.get("idPenerima")))
    except (TypeError, ValueError):
        penerima_id = None

    def store_storage(key, value):
        page.client_storage.set(
            key, str(value) if value not in (None, "", "None") else ""
        )

    profile_data = UserManager.get_profile(user_id, pembeli_id)
    pengguna = profile_data.get("pengguna")
    pembeli = profile_data.get("pembeli")

    if donatur_id is None and pengguna and getattr(pengguna, "email", None):
        try:
            donatur_entity = GetDonaturByEmail(pengguna.email)
            if donatur_entity:
                donatur_id = donatur_entity.idDonatur
                store_storage("idDonatur", donatur_id)
        except Exception as e:
            print(f"Profile donatur fallback error: {e}")

    if penerima_id is None and pengguna:
        try:
            penerima_entity = None
            if getattr(pengguna, "idPengguna", None):
                penerima_entity = GetPenerimaByPengguna(pengguna.idPengguna)
            if penerima_entity is None and getattr(pengguna, "email", None):
                penerima_entity = GetPenerimaByEmail(pengguna.email)
            if penerima_entity:
                penerima_id = penerima_entity.idPenerima
                store_storage("idPenerima", penerima_id)
        except Exception as e:
            print(f"Profile penerima fallback error: {e}")

    user_info = {
        "name": pengguna.nama if pengguna else "Guest",
        "email": pengguna.email if pengguna else "",
        "phone": pengguna.nomorTelepon if pengguna else "",
        "city": pembeli.alamat if pembeli and pembeli.alamat else "",
        "address": pembeli.alamat if pembeli and pembeli.alamat else "",
        "password": pengguna.password if pengguna else "",
    }

    penjualan_manager = PenjualanManager
    barang_manager = BarangManager
    donasi_barang_manager = DonasiBarangManager()
    donasi_uang_manager = DonasiUangManager()

    purchases = []
    if pembeli_id:
        try:
            transaksi_list = penjualan_manager.getTransaksiPembeli(pembeli_id) or []
            for t in transaksi_list:
                if getattr(t, "jenisTransaksi", None) != "jual_beli":
                    continue
                barang = (
                    barang_manager.get_product(t.idBarang)
                    if getattr(t, "idBarang", None)
                    else None
                )
                purchases.append(
                    {
                        "title": getattr(barang, "namaBarang", "-"),
                        "subtitle": f"Quantity: {t.kuantitas or 1}",
                        "price": (
                            f"IDR{int(t.jumlah or 0):,}".replace(",", ".")
                            if t.jumlah
                            else ""
                        ),
                        "status": getattr(t, "status", "-"),
                        "route": f"/product/{getattr(t, 'idBarang', 0) or 0}",
                    }
                )
        except Exception as e:
            print(f"Profile purchases load error: {e}")

    shop_list = []
    if penjual_id:
        try:
            for b in barang_manager.get_by_seller(penjual_id) or []:
                shop_list.append(
                    {
                        "title": getattr(b, "namaBarang", "-"),
                        "subtitle": b.kategori or "",
                        "price": (
                            f"IDR{int(b.harga or 0):,}".replace(",", ".")
                            if getattr(b, "harga", None)
                            else ""
                        ),
                        "status": "Active",
                        "route": f"/product/{getattr(b, 'idBarang', 0) or 0}",
                    }
                )
        except Exception as e:
            print(f"Profile shop load error: {e}")

    donations = []
    if donatur_id:
        try:
            for d in donasi_barang_manager.listByDonatur(donatur_id) or []:
                donations.append(
                    {
                        "title": getattr(d, "namaBarang", "-"),
                        "subtitle": d.kategori or "",
                        "price": "Goods Donation",
                        "status": getattr(d, "status", "-"),
                        "route": f"/donation_recipient_detail?idPenerima={getattr(d, 'idPenerima', 0) or ''}",
                    }
                )
        except Exception as e:
            print(f"Profile donations load error: {e}")

        try:
            for t in donasi_uang_manager.listDonasiUang() or []:
                if getattr(t, "idDonatur", None) != donatur_id:
                    continue
                penerima_name = "-"
                if getattr(t, "idPenerima", None):
                    rec = GetPenerimaById(t.idPenerima)
                    if rec:
                        penerima_name = getattr(rec, "nama", penerima_name)
                donations.append(
                    {
                        "title": f"Funds Donation to {penerima_name}",
                        "subtitle": f"Transaction #{getattr(t, 'idTransaksi', '-')}",
                        "price": (
                            f"IDR{int(t.jumlah or 0):,}".replace(",", ".")
                            if getattr(t, "jumlah", None)
                            else "Funds Donation"
                        ),
                        "status": getattr(t, "status", "-"),
                        "route": f"/donation_recipient_detail?idPenerima={getattr(t, 'idPenerima', 0) or ''}",
                    }
                )
        except Exception as e:
            print(f"Profile cash donations load error: {e}")

    donation_requests = []
    owned_recipients = []
    if pengguna:
        try:
            all_recipients = donasi_barang_manager.listPenerima() or []
        except Exception as e:
            print(f"Profile list recipients error: {e}")
            all_recipients = []

        for rec in all_recipients:
            owner_id = getattr(rec, "idPengguna", None)
            rec_email = (getattr(rec, "email", "") or "").lower()
            if (
                owner_id
                and pengguna
                and getattr(pengguna, "idPengguna", None)
                and owner_id == pengguna.idPengguna
            ) or (
                rec_email
                and pengguna
                and getattr(pengguna, "email", None)
                and rec_email == pengguna.email.lower()
            ):
                owned_recipients.append(rec)

    if not owned_recipients and penerima_id:
        try:
            rec = GetPenerimaById(penerima_id)
            if rec:
                owned_recipients.append(rec)
        except Exception as e:
            print(f"Profile recipient fallback error: {e}")

    for rec in owned_recipients:
        donation_requests.append(
            {
                "title": getattr(rec, "nama", "-"),
                "subtitle": getattr(rec, "alamat", "") or "",
                "price": "",
                "status": "active",
                "route": f"/donation_recipient_detail?idPenerima={getattr(rec, 'idPenerima', 0) or ''}",
            }
        )
        try:
            for d in (
                donasi_barang_manager.listByPenerima(getattr(rec, "idPenerima", 0))
                or []
            ):
                donation_requests.append(
                    {
                        "title": getattr(d, "namaBarang", "-"),
                        "subtitle": f"Target: {getattr(rec, 'nama', '-')}",
                        "price": "Goods Donation",
                        "status": getattr(d, "status", "-"),
                        "route": f"/donation_recipient_detail?idPenerima={getattr(rec, 'idPenerima', 0) or ''}",
                    }
                )
        except Exception as e:
            print(f"Profile donation requests detail error: {e}")

    notifications_list = []
    for p in purchases:
        if p.get("title"):
            notifications_list.append(
                f"Purchase '{p['title']}' status: {p.get('status', '-')}"
            )
    for d in donations:
        if d.get("title"):
            notifications_list.append(
                f"Donation '{d['title']}' status: {d.get('status', '-')}"
            )

    def handle_logout(e):
        for key in ["idPengguna", "idPembeli", "idPenjual", "idDonatur", "idPenerima"]:
            page.client_storage.set(key, "")
        page.go("/login")

    # row information
    def create_info_row(label, value):
        return ft.Row(
            controls=[
                ft.Container(
                    width=200,
                    content=ft.Text(
                        label,
                        size=20,
                        weight="w500",
                        color="#000000",
                        font_family="SFPro",
                    ),
                    alignment=ft.alignment.center_right,
                    padding=ft.padding.only(right=57),
                ),
                ft.Container(
                    width=900,
                    height=72,
                    padding=ft.padding.symmetric(horizontal=30, vertical=20),
                    border_radius=35,
                    border=ft.border.all(2, "#000000"),
                    bgcolor="#FFFFFF",
                    content=ft.Container(
                        content=ft.Text(
                            value,
                            size=21,
                            color="#000000",
                            weight="bold",
                            font_family="SFPro",
                        ),
                        padding=ft.padding.only(left=42),
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # tab function
    def create_profile_tab(label, key):
        is_active = active_tab == key
        return ft.Container(
            bgcolor="#000000" if is_active else "#FFFFFF",
            padding=ft.padding.symmetric(horizontal=30, vertical=16),
            border_radius=35,
            border=None if is_active else ft.border.all(2, "#000000"),
            content=ft.Text(
                label,
                color="#FFFFFF" if is_active else "#000000",
                size=16,
                weight=ft.FontWeight.W_700,
                font_family="SFPro",
            ),
            expand=True,
            alignment=ft.alignment.center,
            ink=True,
            on_click=lambda e: page.go(f"/profile/{key}"),
        )

    show_password = ft.Ref[bool]()
    show_password.current = False
    password_text = ft.Ref[ft.Text]()
    password_eye = ft.Ref[ft.IconButton]()

    def create_password_display(text_password):
        return ft.Container(
            width=900,
            height=72,
            bgcolor="#FFFFFF",
            border_radius=35,
            border=ft.border.all(2, "#000000"),
            padding=ft.padding.symmetric(horizontal=24),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        content=ft.Text(
                            "*" * len(text_password),
                            size=21,
                            weight="bold",
                            font_family="SFPro",
                            color="#000000",
                            ref=password_text,
                        ),
                        padding=ft.padding.only(left=42),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.VISIBILITY_OFF,
                        icon_size=22,
                        icon_color="#000000",
                        ref=password_eye,
                        on_click=lambda e: toggle_password(text_password),
                    ),
                ],
            ),
        )

    def toggle_password(actual_password):
        show_password.current = not show_password.current
        password_text.current.value = (
            actual_password if show_password.current else "*" * len(actual_password)
        )
        password_eye.current.icon = (
            ft.Icons.VISIBILITY if show_password.current else ft.Icons.VISIBILITY_OFF
        )
        page.update()

    # Header with back button and title
    header_section = ft.Container(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK_IOS,
                        icon_size=50,
                        icon_color="#FFFFFF",
                        on_click=lambda e: page.go("/"),
                    ),
                    padding=ft.padding.only(left=50, top=50),
                ),
                ft.Container(
                    content=ft.Text(
                        "Profile",
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

    # kirim tab_content yang sesuai dengan state
    if active_tab == "general-info":
        tab_content = ft.Column(
            spacing=30,
            controls=[
                ft.Container(
                    content=ft.Text(
                        "General\nInformation",
                        size=48,
                        weight=ft.FontWeight.W_700,
                        color="#000000",
                        font_family="SFPro",
                    ),
                    padding=ft.padding.only(left=65),
                ),
                ft.Container(height=10),
                create_info_row("Name", user_info["name"]),
                create_info_row("Email", user_info["email"]),
                create_info_row("Phone Number", user_info["phone"]),
                # create_info_row("City / District", user_info["city"]),
                create_info_row("Address", user_info["address"]),
            ],
        )
    elif active_tab == "security":
        tab_content = ft.Column(
            spacing=30,
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Security &\nAccounts",
                        size=48,
                        weight=ft.FontWeight.W_700,
                        color="#000000",
                        font_family="SFPro",
                    ),
                    padding=ft.padding.only(left=65),
                ),
                ft.Container(height=20),
                create_info_row("Name", user_info["email"]),
                ft.Row(
                    controls=[
                        ft.Container(
                            width=200,
                            alignment=ft.alignment.center_right,
                            content=ft.Text(
                                "Password",
                                size=20,
                                weight="w500",
                                font_family="SFPro",
                                color="#000000",
                            ),
                            padding=ft.padding.only(right=57),
                        ),
                        create_password_display(user_info["password"]),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=20),
                ft.Row(
                    controls=[
                        ft.Container(
                            padding=ft.padding.symmetric(horizontal=40, vertical=18),
                            bgcolor="#000000",
                            border_radius=35,
                            on_click=handle_logout,
                            content=ft.Text(
                                "Log out",
                                size=20,
                                weight=ft.FontWeight.W_700,
                                color="#FFFFFF",
                                font_family="SFPro",
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
        )
    elif active_tab == "orders-activity":

        # item car
        def create_item_card(title, subtitle, price, status="Done", route=None):
            return ft.Container(
                ink=True,
                on_click=(lambda e, r=route: page.go(r)) if route else None,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            spacing=20,
                            controls=[
                                ft.Column(
                                    spacing=5,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text(
                                            title,
                                            size=16,
                                            weight=ft.FontWeight.W_600,
                                            color="#000000",
                                            font_family="SFPro",
                                        ),
                                        ft.Text(
                                            subtitle,
                                            size=14,
                                            color="#666666",
                                            font_family="SFPro",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        ft.Column(
                            spacing=5,
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                            controls=[
                                ft.Text(
                                    price if price else "",
                                    size=16,
                                    weight=ft.FontWeight.W_600,
                                    color="#000000",
                                    font_family="SFPro",
                                ),
                                ft.Row(
                                    spacing=5,
                                    controls=[
                                        ft.Text(
                                            "Status:",
                                            size=14,
                                            color="#000000",
                                            weight=ft.FontWeight.W_600,
                                            font_family="SFPro",
                                        ),
                                        ft.Text(
                                            status if status else "-",
                                            size=14,
                                            color="#0367FD",
                                            weight=ft.FontWeight.W_600,
                                            font_family="SFPro",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                margin=ft.margin.only(left=40, right=40),
            )

        # section yang bisa didropdown
        def create_section(title, subtitle, items, section_key):
            is_expanded = ft.Ref[bool]()
            is_expanded.current = False

            content_container = ft.Ref[ft.Container]()
            arrow_icon = ft.Ref[ft.IconButton]()

            def toggle_section(e):
                is_expanded.current = not is_expanded.current
                content_container.current.visible = is_expanded.current
                arrow_icon.current.icon = (
                    ft.Icons.KEYBOARD_ARROW_UP
                    if is_expanded.current
                    else ft.Icons.KEYBOARD_ARROW_DOWN
                )
                page.update()

            return ft.Container(
                content=ft.Column(
                    spacing=5,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                            controls=[
                                ft.Column(
                                    spacing=5,
                                    controls=[
                                        ft.Container(
                                            content=ft.Text(
                                                title,
                                                size=32,
                                                weight=ft.FontWeight.W_700,
                                                color="#000000",
                                                font_family="SFPro",
                                            ),
                                            padding=ft.padding.only(left=30),
                                        ),
                                        ft.Container(
                                            ft.Text(
                                                subtitle,
                                                size=16,
                                                color="#666666",
                                                font_family="SFPro",
                                            ),
                                            margin=ft.margin.only(left=240),
                                        ),
                                    ],
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.KEYBOARD_ARROW_DOWN,
                                    icon_size=30,
                                    icon_color="#000000",
                                    on_click=toggle_section,
                                    ref=arrow_icon,
                                ),
                            ],
                        ),
                        # divider line
                        ft.Container(
                            height=1,
                            bgcolor="#E0E0E0",
                            margin=ft.margin.only(top=15, bottom=15, left=40, right=40),
                        ),
                        ft.Container(
                            content=items,
                            padding=ft.padding.only(top=0, bottom=10),
                            visible=False,
                            ref=content_container,
                        ),
                        # divider line
                        ft.Container(
                            height=1,
                            bgcolor="#E0E0E0",
                            margin=ft.margin.only(top=15, bottom=15, left=40, right=40),
                        ),
                    ],
                ),
                padding=ft.padding.symmetric(horizontal=40),
            )

        # notifications
        notification_controls = (
            [
                ft.Text(f"- {n}", size=16, color="#000000", font_family="SFPro")
                for n in notifications_list
            ]
            if notifications_list
            else [
                ft.Text(
                    "No notifications yet.",
                    size=16,
                    color="#666666",
                    font_family="SFPro",
                )
            ]
        )
        notification_items = ft.Container(
            content=ft.Column(
                spacing=12,
                controls=notification_controls,
            ),
            margin=ft.margin.only(left=280, top=35, bottom=35),
        )

        # purchases
        purchase_items = ft.Container(
            content=ft.Column(
                spacing=10,
                controls=[
                    create_item_card(
                        p["title"],
                        p["subtitle"],
                        p["price"],
                        p["status"],
                        p.get("route"),
                    )
                    for p in purchases
                ]
                or [
                    ft.Text(
                        "No purchases yet.",
                        size=16,
                        color="#666666",
                        font_family="SFPro",
                    )
                ],
            ),
            margin=ft.margin.only(left=40, right=40, top=35, bottom=35),
        )

        # shop items
        shop_items = ft.Container(
            content=ft.Column(
                spacing=10,
                controls=[
                    create_item_card(
                        p["title"],
                        p["subtitle"],
                        p["price"],
                        p["status"],
                        p.get("route"),
                    )
                    for p in shop_list
                ]
                or [
                    ft.Text(
                        "No shop items yet.",
                        size=16,
                        color="#666666",
                        font_family="SFPro",
                    )
                ],
            ),
            margin=ft.margin.only(left=40, right=40, top=35, bottom=35),
        )

        # donations
        donation_items = ft.Container(
            content=ft.Column(
                spacing=10,
                controls=[
                    create_item_card(
                        p["title"],
                        p["subtitle"],
                        p["price"],
                        p["status"],
                        p.get("route"),
                    )
                    for p in donations
                ]
                or [
                    ft.Text(
                        "No donations yet.",
                        size=16,
                        color="#666666",
                        font_family="SFPro",
                    )
                ],
            ),
            margin=ft.margin.only(left=40, right=40, top=35, bottom=35),
        )

        # donation request
        donation_request_items = ft.Container(
            content=ft.Column(
                spacing=10,
                controls=[
                    create_item_card(
                        p["title"],
                        p["subtitle"],
                        p["price"],
                        p["status"],
                        p.get("route"),
                    )
                    for p in donation_requests
                ]
                or [
                    ft.Text(
                        "No donation requests yet.",
                        size=16,
                        color="#666666",
                        font_family="SFPro",
                    )
                ],
            ),
            margin=ft.margin.only(left=40, right=40, top=35, bottom=35),
        )

        tab_content = ft.Column(
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Orders &\nActivities",
                        size=48,
                        weight=ft.FontWeight.W_700,
                        color="#000000",
                        font_family="SFPro",
                    ),
                    padding=ft.padding.only(left=65, top=20, bottom=20),
                ),
                create_section(
                    "Notifications",
                    "Important updates about your activity",
                    notification_items,
                    "notifications",
                ),
                create_section(
                    "My Purchases",
                    "View and track your orders",
                    purchase_items,
                    "purchases",
                ),
                create_section(
                    "My Shop", "Manage the items you're selling", shop_items, "shop"
                ),
                create_section(
                    "My Donations",
                    "See your contributions",
                    donation_items,
                    "donations",
                ),
                create_section(
                    "My Donations\nRequests",
                    "See your posted requests",
                    donation_request_items,
                    "donation_requests",
                ),
            ],
        )

    main_section = ft.Container(
        content=ft.Column(
            controls=[
                # foto user, nama, dan email
                ft.Container(
                    content=ft.Row(
                        spacing=65,
                        controls=[
                            ft.Container(
                                width=247,
                                height=254,
                                bgcolor="#F0F0F0",
                                border_radius=76,
                            ),
                            ft.Column(
                                spacing=10,
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        user_info["name"],
                                        size=54,
                                        weight="bold",
                                        color="#000000",
                                        font_family="SFPro",
                                    ),
                                    ft.Text(
                                        user_info["email"],
                                        size=22,
                                        color="#000000",
                                        font_family="SFPro",
                                    ),
                                ],
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.only(left=61, right=61, top=40, bottom=40),
                ),
                # tabs
                ft.Container(
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=15,
                        controls=[
                            create_profile_tab("General Information", "general-info"),
                            create_profile_tab("Orders & Activity", "orders-activity"),
                            create_profile_tab("Security & Account", "security"),
                        ],
                    ),
                    padding=ft.padding.symmetric(horizontal=50, vertical=30),
                ),
                # divider line
                ft.Container(
                    height=1,
                    bgcolor="#000000",
                    margin=ft.margin.symmetric(horizontal=61),
                ),
                # main content (tergantung state)
                ft.Container(
                    padding=ft.padding.only(left=0, right=0, top=40, bottom=200),
                    content=tab_content,
                ),
            ],
        ),
        bgcolor="#FFFFFF",
        border_radius=ft.border_radius.only(top_left=99, top_right=99),
    )

    footer_wrapper = ft.Container(
        content=Footer_black(),
        margin=ft.margin.only(top=-150),
    )

    scrollable_content = ft.Column(
        controls=[
            header_section,
            main_section,
            ft.Container(height=50, bgcolor="#FFFFFF"),
            footer_wrapper,
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    nav_bar = NavigationBar(
        on_nav=lambda route: page.go(route), active=f"/profile/{active_tab}", page=page
    )

    return ft.View(
        route="/profile",
        appbar=nav_bar,
        controls=[ft.SafeArea(content=scrollable_content, expand=True)],
        bgcolor="#161616",
        padding=0,
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
