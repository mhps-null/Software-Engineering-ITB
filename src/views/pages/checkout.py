import flet as ft
import os
import re
from ..components.footer_black import Footer_black
from ..components.navigation_bar import NavigationBar
from controllers.BarangManager import BarangManager
from database.query.barang import UpdateBarang
from controllers.PengirimanManager import PengirimanManager
from controllers.PenjualanManager import PenjualanManager
from controllers.FullPaymentManager import FullPaymentManager
from utils.maps_service import MapsService

# Constants
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
ASSETS_UI = os.path.join(ASSETS_DIR, "ui")
FONT_SFPRO_PATH = os.path.join(ASSETS_DIR, "fonts", "SF-Pro-Display-Regular.otf")

PLACEHOLDER_PRODUCT = {
    "name": "Loose Fit Jacket with Detail Pocket",
    "price": 699000,
    "image_base64": "",
    "seller_address": "Jl. Contoh Seller No. 123, Bandung",
}

PAYMENT_METHODS = {
    "E-Wallet": ["Gopay", "DANA", "Apple", "OVO"],
    "Transfer": ["BCA", "Mandiri"],
}


def CheckoutPage(page: ft.Page, product_id: int = None) -> ft.View:
    page.fonts = {"SFPro": FONT_SFPRO_PATH}

    # State management
    form_data = {
        "name": "",
        "search_address": "",
        "address": "",
        "optional_detail": "",
        "email": "",
        "phone": "",
        "payment_method": "",
        "coordinates": None,  # store (lat, lon)
        "city": "",
    }

    validation_errors = {"name": "", "email": "", "phone": "", "address": ""}

    barang = BarangManager.get_product(product_id)

    def parse_int(value):
        try:
            return int(str(value))
        except (TypeError, ValueError):
            return None

    current_uid = parse_int(page.client_storage.get("idPengguna"))

    seller_uid = None
    if barang and getattr(barang, "idPenjual", None):
        seller = BarangManager.get_seller(barang.idPenjual)
        if seller:
            seller_uid = parse_int(getattr(seller, "idPengguna", None))

    is_self_purchase = bool(
        barang and seller_uid and current_uid and seller_uid == current_uid
    )
    is_sold_out = bool(getattr(barang, "isSold", False))
    shipping_cost_data = {"cost": 24000, "distance": 0}

    # Fungsi validasi
    def is_valid_email(email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def is_valid_phone(phone):
        pattern = r"^\+?[0-9\s\-\(\)]{8,20}$"
        return re.match(pattern, phone) is not None

    def validate_name(e):
        name = name_field.value.strip()
        if not name:
            validation_errors["name"] = "Name is required"
            name_error_text.value = validation_errors["name"]
            name_error_text.visible = True
        else:
            validation_errors["name"] = ""
            name_error_text.visible = False
        check_form_completion()
        page.update()

    def validate_email(e):
        email = email_field.value.strip()
        if not email:
            validation_errors["email"] = "Email is required"
            email_error_text.value = validation_errors["email"]
            email_error_text.visible = True
        elif not is_valid_email(email):
            validation_errors["email"] = "Please enter a valid email address"
            email_error_text.value = validation_errors["email"]
            email_error_text.visible = True
        else:
            validation_errors["email"] = ""
            email_error_text.visible = False
        check_form_completion()
        page.update()

    def validate_phone(e):
        phone = phone_field.value.strip()
        if not phone:
            validation_errors["phone"] = "Phone number is required"
            phone_error_text.value = validation_errors["phone"]
            phone_error_text.visible = True
        elif not is_valid_phone(phone):
            validation_errors["phone"] = "Please enter a valid phone number"
            phone_error_text.value = validation_errors["phone"]
            phone_error_text.visible = True
        else:
            validation_errors["phone"] = ""
            phone_error_text.visible = False
        check_form_completion()
        page.update()

    def validate_address(e):
        address = address_field.value.strip()
        if not address:
            validation_errors["address"] = "Address is required"
            address_error_text.value = validation_errors["address"]
            address_error_text.visible = True
        else:
            validation_errors["address"] = ""
            address_error_text.visible = False
        check_form_completion()
        page.update()

    def check_form_completion():
        all_filled = (
            form_data["name"].strip() != ""
            and form_data["address"].strip() != ""
            and form_data["email"].strip() != ""
            and is_valid_email(form_data["email"])
            and form_data["phone"].strip() != ""
            and is_valid_phone(form_data["phone"])
            and form_data["payment_method"] != ""
            and validation_errors["name"] == ""
            and validation_errors["email"] == ""
            and validation_errors["phone"] == ""
            and validation_errors["address"] == ""
            and bool(pembeli_id)
            and not is_self_purchase
            and not is_sold_out
        )

        checkout_button.disabled = not all_filled
        checkout_button.bgcolor = "#0066FF" if all_filled else "#CCCCCC"
        page.update()

    def update_shipping_display():
        cost = shipping_cost_data.get("cost", 0)
        distance = shipping_cost_data.get("distance", 0)

        if cost is None:
            shipping_text.value = "Not Available"
            shipping_text.color = "#FF0000"
        else:
            shipping_text.value = f"IDR{cost:,.0f}".replace(",", ".")
            shipping_text.color = "#000000"

        if distance > 0:
            distance_info.value = f"Distance: {distance} km"
            distance_info.visible = True
        else:
            distance_info.visible = False

        page.update()

    def on_search_address_change(e):
        search_query = e.control.value.strip()
        form_data["search_address"] = search_query

        if not search_query:
            return

        # loading state
        map_placeholder.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.ProgressRing(width=50, height=50, color="#0066FF"),
                ft.Text(
                    "Searching location...",
                    size=12,
                    color="#666666",
                    font_family="SFPro",
                ),
            ],
        )
        page.update()

        # Geocode address
        result = MapsService.geocode_address(search_query)

        if result:
            lat, lon = result["lat"], result["lon"]
            form_data["coordinates"] = (lat, lon)
            form_data["city"] = result.get("city", "")

            address_field.value = result["display_name"]
            form_data["address"] = result["display_name"]
            validate_address(None)

            map_url = None

            # OSM tiles
            try:
                map_url = MapsService.get_static_map_url(
                    lat, lon, zoom=15, width=700, height=300
                )
                print(f"[INFO] Using primary map URL: {map_url}")
            except Exception as e:
                print(f"[ERROR] Primary map failed: {e}")

            # alternative service
            if not map_url:
                try:
                    map_url = MapsService.get_static_map_url_alternative(
                        lat, lon, zoom=15, width=700, height=300
                    )
                    print(f"[INFO] Using alternative map URL: {map_url}")
                except Exception as e:
                    print(f"[ERROR] Alternative map failed: {e}")

            if map_url:
                map_placeholder.content = ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        ft.Image(
                            src=map_url,
                            width=700,
                            height=300,
                            fit=ft.ImageFit.COVER,
                            border_radius=54,
                            error_content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(ft.Icons.MAP, size=50, color="#0066FF"),
                                    ft.Text(
                                        f"Location found:",
                                        size=14,
                                        weight="bold",
                                        color="#161616",
                                        font_family="SFPro",
                                    ),
                                    ft.Text(
                                        f"Lat: {lat:.6f}, Lon: {lon:.6f}",
                                        size=12,
                                        color="#666666",
                                        font_family="SFPro",
                                    ),
                                    ft.Text(
                                        f"Zoom: 15",
                                        size=10,
                                        color="#999999",
                                        font_family="SFPro",
                                    ),
                                ],
                            ),
                        ),
                    ],
                )
            else:
                map_placeholder.content = ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.LOCATION_ON, size=50, color="#0066FF"),
                        ft.Text(
                            "Location found!",
                            size=14,
                            weight="bold",
                            color="#0066FF",
                            font_family="SFPro",
                        ),
                        ft.Text(
                            f"Latitude: {lat:.6f}",
                            size=12,
                            color="#666666",
                            font_family="SFPro",
                        ),
                        ft.Text(
                            f"Longitude: {lon:.6f}",
                            size=12,
                            color="#666666",
                            font_family="SFPro",
                        ),
                        ft.Text(
                            "(Map preview unavailable)",
                            size=10,
                            color="#999999",
                            font_family="SFPro",
                            italic=True,
                        ),
                    ],
                )

            seller_coords = MapsService.parse_seller_address(
                getattr(barang, "alamat", "Bandung, Indonesia")
            )

            if seller_coords:
                distance = MapsService.calculate_distance(seller_coords, (lat, lon))
                shipping_result = MapsService.calculate_shipping_cost(distance)

                shipping_cost_data.update(
                    {
                        "cost": shipping_result["cost"],
                        "distance": shipping_result["distance"],
                    }
                )

                update_shipping_display()

            page.update()
        else:
            map_placeholder.content = ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.LOCATION_OFF, size=50, color="#FF0000"),
                    ft.Text(
                        "Address not found. Try again.",
                        size=12,
                        color="#FF0000",
                        font_family="SFPro",
                    ),
                ],
            )
            page.update()

    def on_payment_method_select(method_type, method_name):
        def handler(e):
            form_data["payment_method"] = f"{method_type}:{method_name}"

            for pmt, buttons_dict in payment_buttons.items():
                for pmn, btn_container in buttons_dict.items():
                    if pmt == method_type and pmn == method_name:
                        btn_container.bgcolor = "#161616"
                        btn_container.content.color = "#FFFFFF"
                    else:
                        btn_container.bgcolor = "#FFFFFF"
                        btn_container.content.color = "#000000"

            check_form_completion()
            page.update()

        return handler

    # form fields
    name_field = ft.TextField(
        hint_text="John Doe",
        border_color="#000000",
        focused_border_color="#000000",
        border_radius=35,
        content_padding=ft.padding.symmetric(horizontal=30, vertical=15),
        text_style=ft.TextStyle(font_family="SFPro", size=14, color="#161616"),
        on_change=lambda e: (
            form_data.update({"name": e.control.value}),
            validate_name(e),
        ),
    )

    name_error_text = ft.Text(
        "",
        size=12,
        color="#FF0000",
        font_family="SFPro",
        visible=False,
    )

    search_address_field = ft.TextField(
        hint_text="Search your address (e.g., Jl. Merdeka, Bandung)",
        border_color="#000000",
        focused_border_color="#000000",
        border_radius=35,
        content_padding=ft.padding.symmetric(horizontal=30, vertical=15),
        text_style=ft.TextStyle(font_family="SFPro", size=14, color="#161616"),
        prefix_icon=ft.Icons.SEARCH,
        on_submit=on_search_address_change,
    )

    # Map placeholder with initial state
    map_placeholder = ft.Container(
        width=700,
        height=300,
        bgcolor="#E8E8E8",
        border_radius=54,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.MAP_OUTLINED, size=50, color="#999999"),
                ft.Text(
                    "Search an address to view map",
                    size=12,
                    color="#999999",
                    font_family="SFPro",
                ),
            ],
        ),
    )

    address_field = ft.TextField(
        hint_text="Will be auto-filled from search above",
        border_color="#000000",
        focused_border_color="#000000",
        border_radius=35,
        content_padding=ft.padding.symmetric(horizontal=30, vertical=15),
        text_style=ft.TextStyle(font_family="SFPro", size=14, color="#161616"),
        multiline=True,
        min_lines=2,
        max_lines=3,
        on_change=lambda e: (
            form_data.update({"address": e.control.value}),
            validate_address(e),
        ),
    )

    address_error_text = ft.Text(
        "",
        size=12,
        color="#FF0000",
        font_family="SFPro",
        visible=False,
    )

    optional_detail_field = ft.TextField(
        hint_text="Blok A No. 5, Dekat Masjid",
        border_color="#000000",
        focused_border_color="#000000",
        border_radius=35,
        content_padding=ft.padding.symmetric(horizontal=30, vertical=15),
        text_style=ft.TextStyle(font_family="SFPro", size=14, color="#161616"),
        on_change=lambda e: form_data.update({"optional_detail": e.control.value}),
    )

    email_field = ft.TextField(
        hint_text="example@gmail.com",
        border_color="#000000",
        focused_border_color="#000000",
        border_radius=35,
        content_padding=ft.padding.symmetric(horizontal=30, vertical=15),
        text_style=ft.TextStyle(font_family="SFPro", size=14, color="#161616"),
        on_change=lambda e: (
            form_data.update({"email": e.control.value}),
            validate_email(e),
        ),
    )

    email_error_text = ft.Text(
        "",
        size=12,
        color="#FF0000",
        font_family="SFPro",
        visible=False,
    )

    phone_field = ft.TextField(
        hint_text="+62 812 3456 7890",
        border_color="#000000",
        focused_border_color="#000000",
        border_radius=35,
        content_padding=ft.padding.symmetric(horizontal=30, vertical=15),
        text_style=ft.TextStyle(font_family="SFPro", size=14, color="#161616"),
        on_change=lambda e: (
            form_data.update({"phone": e.control.value}),
            validate_phone(e),
        ),
    )

    phone_error_text = ft.Text(
        "",
        size=12,
        color="#FF0000",
        font_family="SFPro",
        visible=False,
    )

    # Shipping cost display components
    shipping_text = ft.Text(
        f"IDR{shipping_cost_data['cost']:,.0f}".replace(",", "."),
        size=14,
        weight="bold",
        color="#000000",
        font_family="SFPro",
    )

    distance_info = ft.Text(
        "",
        size=12,
        color="#666666",
        font_family="SFPro",
        visible=False,
    )

    payment_buttons = {}

    for method_type, methods in PAYMENT_METHODS.items():
        payment_buttons[method_type] = {}
        for method_name in methods:
            btn = ft.Container(
                bgcolor="#FFFFFF",
                border_radius=35,
                border=ft.border.all(1, "#000000"),
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                content=ft.Text(
                    method_name,
                    size=14,
                    color="#000000",
                    font_family="SFPro",
                    weight="w500",
                ),
                on_click=on_payment_method_select(method_type, method_name),
            )
            payment_buttons[method_type][method_name] = btn

    # Product display
    product_display = ft.Container(
        bgcolor="#F0F0F0",
        border_radius=ft.BorderRadius(
            top_left=54,
            top_right=54,
            bottom_left=0,
            bottom_right=54,
        ),
        padding=ft.padding.all(20),
        content=ft.Row(
            spacing=15,
            controls=[
                ft.Container(
                    width=140,
                    height=140,
                    bgcolor="#FFFFFF",
                    border_radius=30,
                    content=(
                        ft.Icon(ft.Icons.IMAGE_OUTLINED, size=50, color="#CCCCCC")
                        if not getattr(barang, "foto", None)
                        else ft.Image(
                            src_base64=barang.foto,
                            fit=ft.ImageFit.COVER,
                        )
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Column(
                    spacing=5,
                    expand=True,
                    controls=[
                        ft.Text(
                            barang.namaBarang,
                            size=16,
                            weight="w600",
                            color="#000000",
                            font_family="SFPro",
                        ),
                        ft.Text(
                            f"IDR{barang.harga:,.0f}".replace(",", "."),
                            size=14,
                            weight="bold",
                            color="#000000",
                            font_family="SFPro",
                        ),
                    ],
                ),
            ],
        ),
    )

    pembeli_id = page.client_storage.get("idPembeli")

    def handle_checkout(e):
        if is_sold_out:
            page.open(
                ft.SnackBar(
                    ft.Text("This product is already sold out."), bgcolor="#FFAA00"
                )
            )
            return

        if seller_uid and current_uid:
            page.open(
                ft.SnackBar(
                    ft.Text("You cannot checkout your own listing."), bgcolor="#FFAA00"
                )
            )
            return

        if not pembeli_id:
            page.open(
                ft.SnackBar(
                    ft.Text("Please log in as a buyer first."), bgcolor="#FF4444"
                )
            )
            return

        if shipping_cost_data.get("cost") is None:
            page.open(
                ft.SnackBar(
                    ft.Text("Please search and select a valid delivery address."),
                    bgcolor="#FF4444",
                )
            )
            return

        try:
            penjualan = PenjualanManager.buatPenjualan(
                data={
                    "idBarang": barang.idBarang,
                    "idPembeli": int(pembeli_id),
                    "kuantitas": 1,
                    "metodePembayaran": form_data["payment_method"],
                }
            )

            PengirimanManager.buatPengiriman(
                data={
                    "idTransaksi": penjualan.idTransaksi,
                    "alamat": form_data["address"],
                    "detailAlamat": form_data["optional_detail"],
                    "kota": form_data.get("city") or "Unknown",
                    "metodePengiriman": "kurir",
                }
            )

            FullPaymentManager.bayarPembelian(
                penjualan.idTransaksi, form_data["payment_method"]
            )

            try:
                UpdateBarang(barang.idBarang, {"isSold": True})
                barang.isSold = True
            except Exception as update_err:
                print(f"Failed to mark product as sold: {update_err}")

            page.open(
                ft.SnackBar(
                    content=ft.Text("Checkout successful! Order is being processed."),
                    bgcolor="#00AA00",
                )
            )
            page.go("/profile/general-info")

        except Exception as ex:
            page.open(ft.SnackBar(ft.Text(f"Checkout failed: {ex}"), bgcolor="#FF4444"))

        page.update()

    # Checkout button
    checkout_button = ft.ElevatedButton(
        text="Complete Checkout",
        bgcolor="#CCCCCC",
        color="#FFFFFF",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=54),
            padding=ft.padding.symmetric(horizontal=50, vertical=15),
        ),
        disabled=True,
        on_click=handle_checkout,
    )
    if is_self_purchase or is_sold_out:
        checkout_button.disabled = True
        checkout_button.bgcolor = "#CCCCCC"

    # Header section
    header_section = ft.Container(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK_IOS,
                        icon_size=50,
                        icon_color="#FFFFFF",
                        on_click=lambda e: page.go("/shop"),
                    ),
                    padding=ft.padding.only(left=61, top=100),
                ),
                ft.Container(
                    content=ft.Text(
                        "Checkout",
                        size=48,
                        weight="bold",
                        color="#FFFFFF",
                        font_family="SFPro",
                    ),
                    padding=ft.padding.only(right=61, top=100),
                ),
            ],
        ),
        padding=ft.padding.only(top=20, bottom=60),
    )

    main_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(
                        spacing=40,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            # LEFT COL
                            ft.Container(
                                expand=True,
                                content=ft.Column(
                                    spacing=30,
                                    controls=[
                                        # Shipping Section
                                        ft.Container(
                                            bgcolor="#F0F0F0",
                                            border_radius=ft.BorderRadius(
                                                top_left=54,
                                                top_right=54,
                                                bottom_left=54,
                                                bottom_right=0,
                                            ),
                                            padding=ft.padding.all(40),
                                            content=ft.Column(
                                                spacing=20,
                                                controls=[
                                                    ft.Text(
                                                        "01 Shipping",
                                                        size=28,
                                                        weight="bold",
                                                        color="#000000",
                                                        font_family="SFPro",
                                                    ),
                                                    ft.Column(
                                                        spacing=10,
                                                        controls=[
                                                            ft.Text(
                                                                "Name*",
                                                                size=16,
                                                                weight="w500",
                                                                color="#000000",
                                                                font_family="SFPro",
                                                            ),
                                                            name_field,
                                                            name_error_text,
                                                        ],
                                                    ),
                                                    ft.Column(
                                                        spacing=10,
                                                        controls=[
                                                            ft.Text(
                                                                "Search your address",
                                                                size=16,
                                                                weight="w500",
                                                                color="#000000",
                                                                font_family="SFPro",
                                                            ),
                                                            search_address_field,
                                                            ft.Container(height=12),
                                                            map_placeholder,
                                                        ],
                                                    ),
                                                    ft.Column(
                                                        spacing=10,
                                                        controls=[
                                                            ft.Text(
                                                                "Address",
                                                                size=16,
                                                                weight="w500",
                                                                color="#000000",
                                                                font_family="SFPro",
                                                            ),
                                                            address_field,
                                                            address_error_text,
                                                        ],
                                                    ),
                                                    ft.Column(
                                                        spacing=10,
                                                        controls=[
                                                            ft.Text(
                                                                "Add optional detail",
                                                                size=16,
                                                                weight="w500",
                                                                color="#000000",
                                                                font_family="SFPro",
                                                            ),
                                                            optional_detail_field,
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ),
                                        # Contact Information
                                        ft.Container(
                                            bgcolor="#F0F0F0",
                                            border_radius=ft.BorderRadius(
                                                top_left=54,
                                                top_right=0,
                                                bottom_left=54,
                                                bottom_right=54,
                                            ),
                                            padding=ft.padding.all(40),
                                            content=ft.Column(
                                                spacing=20,
                                                controls=[
                                                    ft.Text(
                                                        "Enter Contact Info",
                                                        size=28,
                                                        weight="bold",
                                                        color="#000000",
                                                        font_family="SFPro",
                                                    ),
                                                    ft.Row(
                                                        spacing=20,
                                                        controls=[
                                                            ft.Container(
                                                                expand=True,
                                                                content=ft.Column(
                                                                    spacing=10,
                                                                    controls=[
                                                                        ft.Text(
                                                                            "Email*",
                                                                            size=16,
                                                                            weight="w500",
                                                                            color="#000000",
                                                                            font_family="SFPro",
                                                                        ),
                                                                        email_field,
                                                                        email_error_text,
                                                                    ],
                                                                ),
                                                            ),
                                                            ft.Container(
                                                                expand=True,
                                                                content=ft.Column(
                                                                    spacing=10,
                                                                    controls=[
                                                                        ft.Text(
                                                                            "Phone number*",
                                                                            size=16,
                                                                            weight="w500",
                                                                            color="#000000",
                                                                            font_family="SFPro",
                                                                        ),
                                                                        phone_field,
                                                                        phone_error_text,
                                                                    ],
                                                                ),
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ),
                                    ],
                                ),
                            ),
                            # RIGHT COL
                            ft.Container(
                                width=550,
                                content=ft.Column(
                                    spacing=30,
                                    controls=[
                                        # Product Display
                                        product_display,
                                        # Payment Section
                                        ft.Container(
                                            bgcolor="#F0F0F0",
                                            width=700,
                                            border_radius=ft.BorderRadius(
                                                top_left=0,
                                                top_right=54,
                                                bottom_left=0,
                                                bottom_right=54,
                                            ),
                                            padding=ft.padding.all(40),
                                            content=ft.Column(
                                                spacing=20,
                                                controls=[
                                                    ft.Text(
                                                        "02 Payment",
                                                        size=28,
                                                        weight="bold",
                                                        color="#000000",
                                                        font_family="SFPro",
                                                    ),
                                                    ft.Text(
                                                        "Select one payment method:",
                                                        size=14,
                                                        color="#666666",
                                                        font_family="SFPro",
                                                    ),
                                                    # E-Wallet
                                                    ft.Column(
                                                        spacing=15,
                                                        controls=[
                                                            ft.Text(
                                                                "E-Wallet",
                                                                size=16,
                                                                weight="w600",
                                                                color="#000000",
                                                                font_family="SFPro",
                                                            ),
                                                            ft.Row(
                                                                spacing=10,
                                                                wrap=True,
                                                                controls=[
                                                                    payment_buttons[
                                                                        "E-Wallet"
                                                                    ]["Gopay"],
                                                                    payment_buttons[
                                                                        "E-Wallet"
                                                                    ]["DANA"],
                                                                    payment_buttons[
                                                                        "E-Wallet"
                                                                    ]["Apple"],
                                                                    payment_buttons[
                                                                        "E-Wallet"
                                                                    ]["OVO"],
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                    # Transfer
                                                    ft.Column(
                                                        spacing=15,
                                                        controls=[
                                                            ft.Text(
                                                                "Transfer",
                                                                size=16,
                                                                weight="w600",
                                                                color="#000000",
                                                                font_family="SFPro",
                                                            ),
                                                            ft.Row(
                                                                spacing=10,
                                                                wrap=True,
                                                                controls=[
                                                                    payment_buttons[
                                                                        "Transfer"
                                                                    ]["BCA"],
                                                                    payment_buttons[
                                                                        "Transfer"
                                                                    ]["Mandiri"],
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ),
                                        # Total Cost Summary
                                        ft.Container(
                                            bgcolor="#FFFFFF",
                                            border_radius=35,
                                            padding=ft.padding.all(30),
                                            content=ft.Column(
                                                spacing=15,
                                                controls=[
                                                    ft.Row(
                                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                        controls=[
                                                            ft.Text(
                                                                "Subtotal",
                                                                size=14,
                                                                color="#666666",
                                                                font_family="SFPro",
                                                            ),
                                                            ft.Text(
                                                                f"IDR{barang.harga:,.0f}".replace(
                                                                    ",", "."
                                                                ),
                                                                size=14,
                                                                weight="w500",
                                                                color="#000000",
                                                                font_family="SFPro",
                                                            ),
                                                        ],
                                                    ),
                                                    ft.Row(
                                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                        controls=[
                                                            ft.Column(
                                                                spacing=5,
                                                                controls=[
                                                                    ft.Text(
                                                                        "Shipping costs",
                                                                        size=14,
                                                                        color="#666666",
                                                                        font_family="SFPro",
                                                                    ),
                                                                    distance_info,
                                                                ],
                                                            ),
                                                            shipping_text,
                                                        ],
                                                    ),
                                                    ft.Divider(
                                                        color="#E0E0E0", height=1
                                                    ),
                                                    ft.Row(
                                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                        controls=[
                                                            ft.Text(
                                                                "Total",
                                                                size=18,
                                                                weight="bold",
                                                                color="#000000",
                                                                font_family="SFPro",
                                                            ),
                                                            ft.Text(
                                                                f"IDR{barang.harga + shipping_cost_data['cost']:,.0f}".replace(
                                                                    ",", "."
                                                                ),
                                                                size=18,
                                                                weight="bold",
                                                                color="#000000",
                                                                font_family="SFPro",
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ),
                                        # Checkout Button
                                        checkout_button,
                                    ],
                                ),
                            ),
                        ],
                    ),
                    padding=ft.padding.symmetric(horizontal=61, vertical=60),
                ),
            ],
        ),
        bgcolor="#FFFFFF",
        border_radius=ft.border_radius.only(top_left=99, top_right=99),
    )

    footer_wrapper = ft.Container(
        content=Footer_black(),
        margin=ft.margin.only(top=-100),
    )

    scrollable_content = ft.Column(
        controls=[
            header_section,
            main_section,
            ft.Container(height=150, bgcolor="#FFFFFF"),
            footer_wrapper,
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    nav_bar = NavigationBar(
        on_nav=lambda route: page.go(route), active="/checkout", page=page
    )

    return ft.View(
        route="/checkout",
        appbar=nav_bar,
        controls=[ft.SafeArea(content=scrollable_content, expand=True)],
        bgcolor="#161616",
        padding=0,
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
