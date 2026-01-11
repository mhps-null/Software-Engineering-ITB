import flet as ft
import os
import re
from pathlib import Path
import base64
from utils.helper import upload_image, is_format_allowed
from ..components.footer_black import Footer_black
from ..components.navigation_bar import NavigationBar
from database.query.penjual import (
    GetPenjualByEmail,
    InsertPenjual,
    UpdatePenjual,
    GetPenjualById,
)
from database.query.barang import InsertBarang
from controllers.UserManager import UserManager

# Constants
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
ASSETS_UI = os.path.join(ASSETS_DIR, "ui")
FONT_SFPRO_PATH = os.path.join(ASSETS_DIR, "fonts", "SF-Pro-Display-Regular.otf")

DEFAULT_CATEGORIES = [
    "Jacket",
    "Shirt",
    "T-Shirt",
    "Pants",
    "Jeans",
    "Shorts",
    "Dress",
    "Skirt",
    "Shoes",
    "Sneakers",
    "Boots",
    "Sandals",
    "Bag",
    "Backpack",
    "Accessories",
    "Watch",
    "Jewelry",
    "Hat",
    "Scarf",
    "Belt",
    "Sunglasses",
    "Electronics",
    "Books",
    "Sports Equipment",
    "Toys",
    "Home Decor",
    "Vinyl",
    "Other",
]


def SellPage(page: ft.Page) -> ft.View:
    page.fonts = {"SFPro": FONT_SFPRO_PATH}

    # state management
    uploaded_images = []
    form_data = {
        "product_name": "",
        "description": "",
        "category": "",
        "custom_category": "",
        "email": "",
        "phone": "",
        "address": "",
        "price": "",
    }

    validation_errors = {"email": "", "phone": ""}

    # fungsi validasi
    def is_valid_email(email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def is_valid_phone(phone):
        pattern = r"^\+?[0-9\s\-\(\)]{8,20}$"
        return re.match(pattern, phone) is not None

    def validate_email(e):
        email = email_field.value.strip()
        if email and not is_valid_email(email):
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
        if phone and not is_valid_phone(phone):
            validation_errors["phone"] = "Please enter a valid phone number"
            phone_error_text.value = validation_errors["phone"]
            phone_error_text.visible = True
        else:
            validation_errors["phone"] = ""
            phone_error_text.visible = False
        check_form_completion()
        page.update()

    def check_form_completion():
        actual_category = (
            form_data["custom_category"]
            if form_data["category"] == "Other"
            else form_data["category"]
        )

        all_filled = (
            form_data["product_name"].strip() != ""
            and form_data["description"].strip() != ""
            and actual_category.strip() != ""
            and form_data["email"].strip() != ""
            and is_valid_email(form_data["email"])
            and form_data["phone"].strip() != ""
            and is_valid_phone(form_data["phone"])
            and form_data["address"].strip() != ""
            and form_data["price"].strip() != ""
            and len(uploaded_images) > 0
            and validation_errors["email"] == ""
            and validation_errors["phone"] == ""
        )

        submit_button.disabled = not all_filled
        submit_button.bgcolor = "#000000" if all_filled else "#CCCCCC"
        page.update()

    def create_image_preview():
        if len(uploaded_images) == 0:
            return ft.Container(
                width=450,
                height=450,
                bgcolor="#FFFFFF",
                border_radius=20,
                content=ft.Icon(ft.Icons.IMAGE_OUTLINED, size=100, color="#CCCCCC"),
                alignment=ft.alignment.center,
            )

        return ft.Container(
            width=450,
            height=450,
            bgcolor="#FFFFFF",
            border_radius=20,
            content=ft.Image(
                src=uploaded_images[-1]["preview_path"],
                fit=ft.ImageFit.CONTAIN,
            ),
        )

    def create_thumbnail_slot(index):
        if index < len(uploaded_images):
            return ft.Container(
                width=100,
                height=100,
                bgcolor="#FFFFFF",
                border_radius=15,
                content=ft.Image(
                    src=uploaded_images[index]["preview_path"],
                    fit=ft.ImageFit.COVER,
                ),
            )
        else:
            return ft.Container(
                width=100,
                height=100,
                bgcolor="#F0F0F0",
                border_radius=15,
            )

    # ini buat media upload and sh
    # def on_file_picked(e: ft.FilePickerResultEvent):
    #     if e.files and len(uploaded_images) < 3:
    #         for file in e.files[:3 - len(uploaded_images)]:
    #             file_ext = file.name.lower().split('.')[-1]

    #             #validasi file
    #             if file_ext in ['png', 'jpg', 'jpeg', 'heic']:
    #                 try:
    #                     with open(file.path, "rb") as f:
    #                         file_bytes = f.read()
    #                         base64_image = base64.b64encode(file_bytes).decode()

    #                     uploaded_images.append({
    #                         "name": file.name,
    #                         "base64": base64_image,
    #                         "size": file.size
    #                     })
    #                 except Exception as ex:
    #                     print(f"Error reading file: {ex}")
    #                     page.open(ft.SnackBar(
    #                         content=ft.Text(f"Error uploading {file.name}"),
    #                         bgcolor="#FF0000",
    #                     )
    #                     page.snack_bar.open = True
    #             else:
    #                 page.open(ft.SnackBar(
    #                     content=ft.Text("Please upload PNG, JPG, JPEG, or HEIC files only."),
    #                     bgcolor="#FF0000",
    #                 )
    #                 page.snack_bar.open = True

    #         update_media_section()
    #         check_form_completion()
    #         page.update()

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            if len(uploaded_images) < 3:
                remaining_slots = 3 - len(uploaded_images)

                for idx, file in enumerate(e.files[:remaining_slots]):
                    try:
                        if not is_format_allowed(file.name):
                            page.open(
                                ft.SnackBar(
                                    content=ft.Text(
                                        "Please upload PNG, JPG, JPEG, WEBP, HEIC, or GIF files only."
                                    ),
                                    bgcolor="#FF0000",
                                )
                            )
                            page.update()
                            continue

                        abs_path = Path(file.path).resolve()
                        uploaded_images.append(
                            {
                                "name": file.name,
                                "preview_path": str(abs_path),
                                "size": file.size,
                            }
                        )
                    except Exception as ex:
                        import traceback

                        traceback.print_exc()

                        page.open(
                            ft.SnackBar(
                                content=ft.Text(
                                    f"Error uploading {file.name}: {str(ex)}"
                                ),
                                bgcolor="#FF0000",
                            )
                        )
                        page.update()

                update_media_section()
                check_form_completion()
                page.update()
                print("UI updated successfully")
            else:
                print("You cannot upload more than three images.")
        else:
            print("No files selected")

    def trigger_file_picker(e):
        if len(uploaded_images) < 3:
            file_picker.pick_files(
                allow_multiple=True,
                allowed_extensions=["png", "jpg", "jpeg", "heic", "webp", "gif"],
            )
        else:
            page.open(
                ft.SnackBar(
                    content=ft.Text("You cannot upload more than three images."),
                    bgcolor="#FFAA00",
                )
            )
            page.update()

    def update_media_section():
        media_section.content = ft.Column(
            spacing=20,
            controls=[
                create_image_preview(),
                ft.Row(
                    spacing=15,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        create_thumbnail_slot(0),
                        create_thumbnail_slot(1),
                        create_thumbnail_slot(2),
                        ft.Container(
                            width=100,
                            height=100,
                            bgcolor=(
                                "#FFFFFF" if len(uploaded_images) < 3 else "#F0F0F0"
                            ),
                            border_radius=15,
                            border=(
                                ft.border.all(2, "#000000")
                                if len(uploaded_images) < 3
                                else None
                            ),
                            content=ft.IconButton(
                                icon=ft.Icons.ADD,
                                icon_size=40,
                                icon_color=(
                                    "#000000" if len(uploaded_images) < 3 else "#CCCCCC"
                                ),
                                on_click=trigger_file_picker,
                                disabled=len(uploaded_images) >= 3,
                            ),
                        ),
                    ],
                ),
            ],
        )
        page.update()

    def on_category_change(e):
        if e.control.value == "Other":
            custom_category_field.visible = True
            form_data["category"] = "Other"
        else:
            custom_category_field.visible = False
            form_data["category"] = e.control.value
            form_data["custom_category"] = ""
        check_form_completion()
        page.update()

    # FORM FIELDS
    product_name_field = ft.TextField(
        hint_text="Loose Fit Jacket with Detail Pocket",
        border_color="#000000",
        focused_border_color="#000000",
        border_radius=35,
        content_padding=ft.padding.symmetric(horizontal=30, vertical=10),
        text_style=ft.TextStyle(font_family="SFPro", size=14, color="#161616"),
        max_length=100,
        on_change=lambda e: (
            form_data.update({"product_name": e.control.value}),
            check_form_completion(),
        ),
    )

    description_field = ft.TextField(
        hint_text="Lorem ipsum dolor sit amet, consectetur adipiscing elit...",
        border_color="#000000",
        focused_border_color="#000000",
        border_radius=35,
        content_padding=ft.padding.symmetric(horizontal=30, vertical=10),
        # text_style=ft.TextStyle(font_family="SFPro", size=16),
        text_style=ft.TextStyle(font_family="SFPro", size=14, color="#161616"),
        multiline=True,
        min_lines=5,
        max_lines=8,
        on_change=lambda e: (
            form_data.update({"description": e.control.value}),
            check_form_completion(),
        ),
    )

    category_dropdown = ft.Dropdown(
        hint_text="Select category",
        options=[ft.dropdown.Option(cat) for cat in DEFAULT_CATEGORIES],
        border_color="#000000",
        focused_border_color="#000000",
        border_radius=35,
        content_padding=ft.padding.symmetric(horizontal=30, vertical=10),
        text_style=ft.TextStyle(font_family="SFPro", size=14, color="#161616"),
        on_change=on_category_change,
    )

    custom_category_field = ft.TextField(
        hint_text="Enter your custom category",
        border_color="#000000",
        focused_border_color="#000000",
        border_radius=35,
        content_padding=ft.padding.symmetric(horizontal=30, vertical=10),
        # text_style=ft.TextStyle(font_family="SFPro", size=16),
        text_style=ft.TextStyle(font_family="SFPro", size=14, color="#161616"),
        visible=False,
        on_change=lambda e: (
            form_data.update({"custom_category": e.control.value}),
            check_form_completion(),
        ),
    )

    email_field = ft.TextField(
        hint_text="example@gmail.com",
        border_color="#000000",
        focused_border_color="#000000",
        border_radius=35,
        content_padding=ft.padding.symmetric(horizontal=30, vertical=10),
        # text_style=ft.TextStyle(font_family="SFPro", size=16),
        text_style=ft.TextStyle(font_family="SFPro", size=14, color="#161616"),
        on_change=lambda e: (form_data.update({"email": e.control.value}),),
        on_blur=validate_email,
    )

    email_error_text = ft.Text(
        "",
        size=12,
        color="#FF0000",
        font_family="SFPro",
        visible=False,
    )

    phone_field = ft.TextField(
        # hint_text="00000000000",
        border_color="#000000",
        focused_border_color="#000000",
        border_radius=35,
        content_padding=ft.padding.symmetric(horizontal=30, vertical=10),
        # text_style=ft.TextStyle(font_family="SFPro", size=16),
        text_style=ft.TextStyle(font_family="SFPro", size=14, color="#161616"),
        on_change=lambda e: (form_data.update({"phone": e.control.value}),),
        on_blur=validate_phone,
    )

    phone_error_text = ft.Text(
        "",
        size=12,
        color="#FF0000",
        font_family="SFPro",
        visible=False,
    )

    address_field = ft.TextField(
        hint_text="Jl. Lorem Ipsum",
        border_color="#000000",
        focused_border_color="#000000",
        border_radius=35,
        content_padding=ft.padding.symmetric(horizontal=30, vertical=10),
        # text_style=ft.TextStyle(font_family="SFPro", size=16),
        text_style=ft.TextStyle(font_family="SFPro", size=14, color="#161616"),
        on_change=lambda e: (
            form_data.update({"address": e.control.value}),
            check_form_completion(),
        ),
    )

    price_field = ft.TextField(
        hint_text="150000",
        border_color="#000000",
        focused_border_color="#000000",
        border_radius=35,
        content_padding=ft.padding.symmetric(horizontal=30, vertical=10),
        # text_style=ft.TextStyle(font_family="SFPro", size=16),
        text_style=ft.TextStyle(font_family="SFPro", size=16, color="#161616"),
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=lambda e: (
            form_data.update({"price": e.control.value}),
            check_form_completion(),
        ),
    )

    def submit_product(e):
        actual_category = (
            form_data["custom_category"]
            if form_data["category"] == "Other"
            else form_data["category"]
        )

        if form_data["category"] == "Other" and form_data["custom_category"].strip():
            new_cat = form_data["custom_category"].strip()
            if new_cat not in DEFAULT_CATEGORIES:
                DEFAULT_CATEGORIES.insert(-1, new_cat)

        try:
            # ensure seller exists
            seller = None
            try:
                current_penjual_id = int(str(page.client_storage.get("idPenjual")))
            except (TypeError, ValueError):
                current_penjual_id = None
            try:
                current_user_id = int(str(page.client_storage.get("idPengguna")))
            except (TypeError, ValueError):
                current_user_id = None

            if current_penjual_id:
                try:
                    seller = GetPenjualById(current_penjual_id)
                except Exception as ex:
                    print(f"GetPenjualById error: {ex}")

            if seller is None:
                try:
                    seller = GetPenjualByEmail(form_data["email"])
                except Exception as ex:
                    print(f"GetPenjualByEmail error: {ex}")

            seller_name = form_data["product_name"] or "Seller"
            if current_user_id:
                resolved_name = UserManager.get_username(current_user_id)
                if resolved_name:
                    seller_name = resolved_name

            if seller is None:
                try:
                    seller = InsertPenjual(
                        {
                            "nama": seller_name,
                            "email": form_data["email"],
                            "nomorTelepon": form_data["phone"],
                            "alamat": form_data["address"],
                        }
                    )
                except Exception as ex:
                    raise ValueError(f"Failed to create seller: {ex}")
            else:
                try:
                    UpdatePenjual(
                        getattr(seller, "idPenjual", None),
                        {
                            "nomorTelepon": form_data["phone"],
                            "alamat": form_data["address"],
                        },
                    )
                    # refresh seller reference with updated info
                    seller = GetPenjualByEmail(form_data["email"])
                except Exception as ex:
                    print(f"Failed to update seller info: {ex}")
            if getattr(seller, "idPenjual", None):
                try:
                    page.client_storage.set("idPenjual", seller.idPenjual)
                except Exception:
                    pass

            foto_base64 = None
            if uploaded_images:
                first = uploaded_images[0]
                try:
                    with open(first["preview_path"], "rb") as f:
                        foto_base64 = base64.b64encode(f.read()).decode("utf-8")
                except Exception as ex:
                    print(f"Image encode error: {ex}")

            payload = {
                "namaBarang": form_data["product_name"],
                "deskripsi": form_data["description"],
                "kategori": actual_category,
                "foto": foto_base64,
                "video": None,
                "idPenjual": getattr(seller, "idPenjual", None),
                "harga": (
                    int(form_data["price"]) if str(form_data["price"]).isdigit() else 0
                ),
            }

            barang = InsertBarang(payload)
            page.open(
                ft.SnackBar(
                    content=ft.Text("Product submitted successfully!"),
                    bgcolor="#00AA00",
                )
            )
            page.update()
            if getattr(barang, "idBarang", None):
                page.go(f"/product/{barang.idBarang}")
        except Exception as ex:
            page.open(
                ft.SnackBar(
                    content=ft.Text(f"Failed to submit product: {ex}"),
                    bgcolor="#FF5252",
                )
            )
            page.update()

    submit_button = ft.Container(
        bgcolor="#8F8F8F",
        # border_radius=35,
        border_radius=ft.BorderRadius(
            top_left=0,
            top_right=54,
            bottom_left=54,
            bottom_right=54,
        ),
        padding=ft.padding.symmetric(horizontal=50, vertical=12),
        content=ft.Text(
            "Submit",
            color="#FFFFFF",
            size=18,
            weight="bold",
            font_family="SFPro",
        ),
        alignment=ft.alignment.center,
        on_click=submit_product,
        disabled=True,
    )

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)
    page.update()

    print(f"File picker registered: {file_picker}")
    print(f"Page overlay count: {len(page.overlay)}")
    media_section = ft.Container()
    update_media_section()

    # header: judul sell page
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
                    padding=ft.padding.only(left=61, top=166),
                ),
                ft.Container(
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        spacing=0,
                        controls=[
                            ft.Text(
                                "Sell Your",
                                size=48,
                                weight="bold",
                                color="#FFFFFF",
                                font_family="SFPro",
                            ),
                            ft.Text(
                                "Preloved Items",
                                size=48,
                                weight="bold",
                                color="#FFFFFF",
                                font_family="SFPro",
                            ),
                        ],
                    ),
                    padding=ft.padding.only(right=61, top=166),
                ),
            ],
        ),
        padding=ft.padding.only(top=20, bottom=60),
    )

    media_section = ft.Container()
    update_media_section()

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
                                    spacing=40,
                                    controls=[
                                        # General Information
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
                                                        "General Information",
                                                        size=28,
                                                        weight="bold",
                                                        color="#000000",
                                                        font_family="SFPro",
                                                    ),
                                                    ft.Column(
                                                        spacing=15,
                                                        controls=[
                                                            ft.Text(
                                                                "Product Name",
                                                                size=16,
                                                                weight="w500",
                                                                color="#000000",
                                                                font_family="SFPro",
                                                            ),
                                                            product_name_field,
                                                        ],
                                                    ),
                                                    ft.Column(
                                                        spacing=15,
                                                        controls=[
                                                            ft.Text(
                                                                "Description",
                                                                size=16,
                                                                weight="w500",
                                                                color="#000000",
                                                                font_family="SFPro",
                                                            ),
                                                            description_field,
                                                        ],
                                                    ),
                                                    ft.Column(
                                                        spacing=15,
                                                        controls=[
                                                            ft.Text(
                                                                "Category",
                                                                size=16,
                                                                weight="w500",
                                                                color="#000000",
                                                                font_family="SFPro",
                                                            ),
                                                            category_dropdown,
                                                            custom_category_field,
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
                                                bottom_right=0,
                                            ),
                                            padding=ft.padding.all(40),
                                            content=ft.Column(
                                                spacing=20,
                                                controls=[
                                                    ft.Text(
                                                        "Contact Information",
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
                                                                    spacing=5,
                                                                    controls=[
                                                                        ft.Text(
                                                                            "Email",
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
                                                                    spacing=5,
                                                                    controls=[
                                                                        ft.Text(
                                                                            "Phone Number",
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
                                        # Shipping & Delivery
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
                                                        "Shipping & Delivery",
                                                        size=28,
                                                        weight="bold",
                                                        color="#000000",
                                                        font_family="SFPro",
                                                    ),
                                                    ft.Column(
                                                        spacing=15,
                                                        controls=[
                                                            ft.Text(
                                                                "Address",
                                                                size=16,
                                                                weight="w500",
                                                                color="#000000",
                                                                font_family="SFPro",
                                                            ),
                                                            address_field,
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
                                    spacing=40,
                                    controls=[
                                        # Media Upload
                                        ft.Container(
                                            bgcolor="#F0F0F0",
                                            border_radius=ft.BorderRadius(
                                                top_left=54,
                                                top_right=54,
                                                bottom_left=0,
                                                bottom_right=54,
                                            ),
                                            padding=ft.padding.all(40),
                                            content=ft.Column(
                                                spacing=20,
                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                controls=[
                                                    ft.Text(
                                                        "Media Upload",
                                                        size=28,
                                                        weight="bold",
                                                        color="#000000",
                                                        font_family="SFPro",
                                                    ),
                                                    media_section,
                                                ],
                                            ),
                                        ),
                                        # Pricing
                                        ft.Container(
                                            bgcolor="#F0F0F0",
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
                                                        "Pricing",
                                                        size=28,
                                                        weight="bold",
                                                        color="#000000",
                                                        font_family="SFPro",
                                                    ),
                                                    ft.Text(
                                                        "Set a competitive price that reflects the value and condition of your item.",
                                                        size=14,
                                                        color="#666666",
                                                        font_family="SFPro",
                                                    ),
                                                    price_field,
                                                ],
                                            ),
                                        ),
                                        # Submit Button
                                        submit_button,
                                    ],
                                ),
                            ),
                        ],
                    ),
                    padding=ft.padding.symmetric(horizontal=61, vertical=60),
                ),
            ],
            # ft.Container(height=100),
        ),
        # height=100,
        bgcolor="#FFFFFF",
        border_radius=ft.border_radius.only(top_left=99, top_right=99),
    )

    footer_wrapper = ft.Container(
        content=Footer_black(),
        margin=ft.margin.only(top=-100),
    )

    # scrollable_content=ft.Column(
    #     controls=[
    #         main_section,
    #         footer_wrapper,
    #     ],
    #     spacing=0,
    #     scroll=ft.ScrollMode.AUTO,
    #     expand=True,
    # )
    scrollable_content = ft.Column(
        controls=[
            # header_section,
            # main_section,
            # footer_wrapper,
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
        on_nav=lambda route: page.go(route), active="/shop", page=page
    )

    return ft.View(
        route="/sell",
        # controls=[
        #     header_section,
        #     main_section,
        #     # footer,
        #     footer_wrapper,
        # ],
        appbar=nav_bar,
        controls=[ft.SafeArea(content=scrollable_content, expand=True)],
        bgcolor="#161616",
        padding=0,
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        # scroll=ft.ScrollMode.AUTO,
    )
