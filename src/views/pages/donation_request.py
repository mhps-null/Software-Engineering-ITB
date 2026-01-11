import flet as ft
import os
from pathlib import Path

from database.query.penerima_donasi import InsertPenerima
from utils.helper import upload_image, is_format_allowed
from utils.maps_service import MapsService
from ..components.navigation_bar import NavigationBar
from ..components.footer_black import Footer_black

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
FONT_SFPRO_PATH = os.path.join(ASSETS_DIR, "fonts", "SF-Pro-Display-Regular.otf")


# ========================= PAGE =========================
def DonationRequestPage(page: ft.Page) -> ft.View:
    page.fonts = {"SFPro": FONT_SFPRO_PATH}

    # ---------------------- Form State ----------------------
    form_data = {
        "title": "",
        "description": "",
        "search_address": "",
        "address": "",
        "additional_detail": "",
        "email": "",
        "phone": "",
        "needed": "",
        "coordinates": None,
        "city": "",
    }

    def check_form():
        required = ["title", "description", "address", "email", "phone", "needed"]
        all_filled = (
            all((form_data.get(k) or "").strip() for k in required) and len(images) > 0
        )
        submit_button.disabled = not all_filled
        submit_button.bgcolor = "#0066FF" if all_filled else "#8F8F8F"
        page.update()

    # -------------------- Map search --------------------
    def on_search_address_change(e):
        search_query = (e.control.value or "").strip()
        form_data["search_address"] = search_query
        if not search_query:
            return

        dummy_map.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.ProgressRing(width=40, height=40, color="#0066FF"),
                ft.Text(
                    "Searching location...",
                    size=12,
                    color="#666666",
                    font_family="SFPro",
                ),
            ],
        )
        page.update()

        result = MapsService.geocode_address(search_query)
        if result:
            lat, lon = result["lat"], result["lon"]
            form_data["coordinates"] = (lat, lon)
            form_data["city"] = result.get("city", "")

            address_field.value = result["display_name"]
            form_data["address"] = result["display_name"]

            map_url = None
            try:
                map_url = MapsService.get_static_map_url(
                    lat, lon, zoom=15, width=500, height=250
                )
            except Exception as ex:
                print(f"[ERROR] Primary map failed: {ex}")

            if not map_url:
                try:
                    map_url = MapsService.get_static_map_url_alternative(
                        lat, lon, zoom=15, width=500, height=250
                    )
                except Exception as ex:
                    print(f"[ERROR] Alternative map failed: {ex}")

            if map_url:
                dummy_map.content = ft.Image(
                    src=map_url,
                    width=700,
                    height=300,
                    fit=ft.ImageFit.COVER,
                    border_radius=30,
                )
            else:
                dummy_map.content = ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.LOCATION_ON, size=40, color="#0066FF"),
                        ft.Text(
                            f"Lat: {lat:.6f}, Lon: {lon:.6f}",
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
        else:
            dummy_map.content = ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.LOCATION_OFF, size=40, color="#FF0000"),
                    ft.Text(
                        "Address not found. Try again.",
                        size=12,
                        color="#FF0000",
                        font_family="SFPro",
                    ),
                ],
            )
        page.update()
        check_form()

    # ---------------------- TEXT FIELDS ----------------------
    title_field = ft.TextField(
        hint_text="e.g. Essential School Supplies Needed",
        bgcolor="#FAFAFA",
        border_color="#D4D4D4",
        border_radius=30,
        height=48,
        text_size=14,
        text_style=ft.TextStyle(color="#161616"),
        hint_style=ft.TextStyle(color="#9E9E9E"),
        content_padding=15,
        on_change=lambda e: (
            form_data.update({"title": (e.control.value or "").strip()}),
            check_form(),
        ),
    )

    description_field = ft.TextField(
        hint_text="Explain what you need and why.\ne.g. We're collecting clean clothing for families affected by recent floods. All sizes are welcome.",
        bgcolor="#FAFAFA",
        border_color="#D4D4D4",
        border_radius=30,
        multiline=True,
        min_lines=5,
        max_lines=8,
        text_size=14,
        text_style=ft.TextStyle(color="#161616"),
        hint_style=ft.TextStyle(color="#9E9E9E"),
        content_padding=15,
        on_change=lambda e: (
            form_data.update({"description": (e.control.value or "").strip()}),
            check_form(),
        ),
    )

    address_search = ft.TextField(
        hint_text="Search your address (e.g., Jl. Merdeka, Bandung)",
        bgcolor="#FAFAFA",
        border_color="#D4D4D4",
        border_radius=30,
        prefix_icon=ft.Icons.SEARCH,
        height=48,
        text_size=14,
        text_style=ft.TextStyle(color="#161616"),
        hint_style=ft.TextStyle(color="#9E9E9E"),
        content_padding=15,
        on_submit=on_search_address_change,
    )

    address_field = ft.TextField(
        hint_text="Will be auto-filled from search above",
        bgcolor="#FAFAFA",
        border_color="#D4D4D4",
        border_radius=30,
        height=48,
        text_size=14,
        text_style=ft.TextStyle(color="#161616"),
        hint_style=ft.TextStyle(color="#9E9E9E"),
        content_padding=15,
        on_change=lambda e: (
            form_data.update({"address": (e.control.value or "").strip()}),
            check_form(),
        ),
    )

    additional_detail_field = ft.TextField(
        hint_text="Add optional detail",
        bgcolor="#FAFAFA",
        border_color="#D4D4D4",
        border_radius=30,
        height=48,
        text_size=14,
        text_style=ft.TextStyle(color="#161616"),
        hint_style=ft.TextStyle(color="#9E9E9E"),
        content_padding=15,
        on_change=lambda e: form_data.update(
            {"additional_detail": e.control.value or ""}
        ),
    )

    email_field = ft.TextField(
        hint_text="Email*",
        bgcolor="#FAFAFA",
        border_color="#D4D4D4",
        border_radius=30,
        height=48,
        text_size=14,
        text_style=ft.TextStyle(color="#161616"),
        hint_style=ft.TextStyle(color="#9E9E9E"),
        content_padding=15,
        on_change=lambda e: (
            form_data.update({"email": (e.control.value or "").strip()}),
            check_form(),
        ),
    )

    phone_field = ft.TextField(
        hint_text="Phone number*",
        bgcolor="#FAFAFA",
        border_color="#D4D4D4",
        border_radius=30,
        height=48,
        text_size=14,
        text_style=ft.TextStyle(color="#161616"),
        hint_style=ft.TextStyle(color="#9E9E9E"),
        content_padding=15,
        on_change=lambda e: (
            form_data.update({"phone": (e.control.value or "").strip()}),
            check_form(),
        ),
    )

    needed_field = ft.TextField(
        hint_text="e.g. 10 blankets, 5 bottles, hygiene kits…",
        bgcolor="#FAFAFA",
        border_color="#D4D4D4",
        border_radius=30,
        height=48,
        text_size=14,
        text_style=ft.TextStyle(color="#161616"),
        hint_style=ft.TextStyle(color="#9E9E9E"),
        content_padding=15,
        on_change=lambda e: (
            form_data.update({"needed": (e.control.value or "").strip()}),
            check_form(),
        ),
    )

    # ------------------- Media Upload -------------------
    images = []

    def create_image_preview():
        if len(images) == 0:
            return ft.Container(
                width=450,
                height=300,
                bgcolor="#FFFFFF",
                border_radius=20,
                content=ft.Icon(ft.Icons.IMAGE_OUTLINED, size=100, color="#CCCCCC"),
                alignment=ft.alignment.center,
            )
        return ft.Container(
            width=450,
            height=300,
            bgcolor="#FFFFFF",
            border_radius=20,
            content=ft.Image(
                src=images[-1]["preview_path"],
                fit=ft.ImageFit.CONTAIN,
            ),
        )

    def create_thumbnail_slot(index: int):
        if index < len(images):
            return ft.Container(
                width=100,
                height=100,
                bgcolor="#FFFFFF",
                border_radius=15,
                content=ft.Image(
                    src=images[index]["preview_path"],
                    fit=ft.ImageFit.COVER,
                ),
            )
        return ft.Container(
            width=100,
            height=100,
            bgcolor="#F0F0F0",
            border_radius=15,
        )

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
                        ft.Container(
                            width=100,
                            height=100,
                            bgcolor="#FFFFFF" if len(images) < 1 else "#F0F0F0",
                            border_radius=15,
                            border=(
                                ft.border.all(2, "#000000") if len(images) < 1 else None
                            ),
                            content=ft.IconButton(
                                icon=ft.Icons.ADD,
                                icon_size=40,
                                icon_color="#000000" if len(images) < 1 else "#CCCCCC",
                                on_click=lambda e: trigger_file_picker(e),
                                disabled=len(images) >= 1,
                            ),
                        ),
                    ],
                ),
            ],
        )
        page.update()

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            remaining_slots = 1 - len(images)
            for file in e.files[:remaining_slots]:
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
                    images.append(
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
                            content=ft.Text(f"Error uploading {file.name}: {str(ex)}"),
                            bgcolor="#FF0000",
                        )
                    )
                    page.update()
            update_media_section()
            check_form()

    def trigger_file_picker(e):
        if len(images) < 1:
            file_picker.pick_files(
                allow_multiple=False,
                allowed_extensions=["png", "jpg", "jpeg", "webp", "heic", "gif"],
            )
        else:
            page.open(
                ft.SnackBar(
                    content=ft.Text("You can upload only 1 image."),
                    bgcolor="#FFAA00",
                )
            )
            page.update()

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)
    media_section = ft.Container()
    update_media_section()

    # ----------------------- Map Container -------------------------
    dummy_map = ft.Container(
        width=700,
        height=300,
        bgcolor="#EAEAEA",
        border_radius=20,
        alignment=ft.alignment.center,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.MAP_OUTLINED, size=40, color="#999999"),
                ft.Text(
                    "Search an address to view map",
                    size=12,
                    color="#999999",
                    font_family="SFPro",
                ),
            ],
        ),
    )

    # ---------------------- MAIN CARDS -------------------------
    top_bar = ft.Container(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK_IOS,
                        icon_size=50,
                        icon_color="#FFFFFF",
                        on_click=lambda e: page.go("/donation"),
                    ),
                    padding=ft.padding.only(left=61, top=166),
                ),
                ft.Container(
                    content=ft.Text(
                        "Request Donation",
                        size=48,
                        weight="bold",
                        color="#FFFFFF",
                        font_family="SFPro",
                    ),
                    padding=ft.padding.only(right=61, top=166),
                ),
            ],
        ),
        padding=ft.padding.only(top=20, bottom=60),
    )

    general_info_card = ft.Container(
        bgcolor="#F8F8F8",
        border_radius=ft.BorderRadius(
            top_left=54,
            top_right=54,
            bottom_left=54,
            bottom_right=0,
        ),
        padding=ft.padding.all(40),
        expand=True,
        content=ft.Column(
            controls=[
                ft.Text(
                    "General Information",
                    size=24,
                    color="#161616",
                    weight=ft.FontWeight.W_700,
                ),
                ft.Text("Title", size=14, color="#161616", weight=ft.FontWeight.W_600),
                title_field,
                ft.Container(height=20),
                ft.Text(
                    "Description", size=14, color="#161616", weight=ft.FontWeight.W_600
                ),
                description_field,
            ],
            spacing=12,
        ),
    )

    media_upload_card = ft.Container(
        bgcolor="#F8F8F8",
        border_radius=ft.BorderRadius(
            top_left=54,
            top_right=54,
            bottom_left=0,
            bottom_right=54,
        ),
        padding=ft.padding.all(40),
        expand=True,
        content=ft.Column(
            controls=[
                ft.Text(
                    "Media Upload", size=24, color="#161616", weight=ft.FontWeight.W_700
                ),
                ft.Container(height=10),
                media_section,
            ],
            spacing=10,
        ),
    )

    detail_info_card = ft.Container(
        bgcolor="#F8F8F8",
        border_radius=ft.BorderRadius(
            top_left=54,
            top_right=0,
            bottom_left=54,
            bottom_right=54,
        ),
        padding=ft.padding.all(40),
        expand=True,
        content=ft.Column(
            controls=[
                ft.Text(
                    "Detail Information",
                    size=24,
                    color="#161616",
                    weight=ft.FontWeight.W_700,
                ),
                ft.Text(
                    "Search your address",
                    size=14,
                    color="#161616",
                    weight=ft.FontWeight.W_600,
                ),
                address_search,
                ft.Container(height=10),
                dummy_map,
                ft.Container(height=10),
                ft.Text(
                    "Address", size=14, color="#161616", weight=ft.FontWeight.W_600
                ),
                address_field,
                ft.Text(
                    "Additional Detail",
                    size=14,
                    color="#161616",
                    weight=ft.FontWeight.W_600,
                ),
                additional_detail_field,
                ft.Text(
                    "Enter Contact Info",
                    size=14,
                    color="#161616",
                    weight=ft.FontWeight.W_600,
                ),
                ft.Column(
                    controls=[email_field, phone_field],
                ),
            ],
            spacing=12,
        ),
    )

    needed_items_card = ft.Container(
        bgcolor="#F8F8F8",
        border_radius=ft.BorderRadius(
            top_left=0,
            top_right=54,
            bottom_left=0,
            bottom_right=54,
        ),
        padding=ft.padding.all(40),
        expand=True,
        content=ft.Column(
            controls=[
                ft.Text(
                    "Needed Items or Amount",
                    size=24,
                    color="#161616",
                    weight=ft.FontWeight.W_700,
                ),
                ft.Text(
                    "What you need",
                    size=14,
                    color="#161616",
                    weight=ft.FontWeight.W_600,
                ),
                needed_field,
            ],
            spacing=12,
        ),
    )

    def submit_form(e=None):
        # Normalize string fields; keep non-string (e.g., coordinates tuple) as-is
        data = {
            k: ((v or "").strip() if isinstance(v, str) else v)
            for k, v in form_data.items()
        }
        required = ["title", "description", "address", "email", "phone", "needed"]
        if not all((data.get(k) or "").strip() for k in required) or len(images) == 0:
            page.open(
                ft.SnackBar(
                    content=ft.Text(
                        "Please fill all required fields and upload at least one image."
                    ),
                    bgcolor="#FF5252",
                )
            )
            page.update()
            return

        try:
            try:
                current_user_id = int(str(page.client_storage.get("idPengguna")))
            except (TypeError, ValueError):
                current_user_id = None

            uploaded_paths = []
            for img in images:
                stored = upload_image(
                    img["preview_path"], filename=Path(img["name"]).stem
                )
                uploaded_paths.append(stored)

            address_value = (address_field.value or "").strip() or data.get(
                "address", ""
            )
            address_search_value = (address_search.value or "").strip()
            if not address_value and address_search_value:
                address_value = address_search_value
            additional_detail = (additional_detail_field.value or "").strip()
            if additional_detail:
                address_value = (
                    f"{address_value} ({additional_detail})"
                    if address_value
                    else additional_detail
                )

            foto_path = uploaded_paths[0] if uploaded_paths else None
            if foto_path:
                foto_path_obj = Path(foto_path)
                if not foto_path_obj.is_absolute():
                    foto_path_obj = (
                        Path(__file__).resolve().parents[2] / foto_path_obj
                    ).resolve()
                foto_path = foto_path_obj.as_posix()

            penerima_payload = {
                "nama": data["title"],
                "email": data["email"],
                "deskripsi": data["description"],
                "nomorTelepon": data["phone"],
                "alamat": address_value,
                "foto": foto_path,
            }
            if current_user_id:
                penerima_payload["idPengguna"] = current_user_id
            penerima = InsertPenerima(penerima_payload)
            if not getattr(penerima, "idPenerima", None):
                raise ValueError("Recipient could not be created.")

            page.client_storage.set("idPenerima", str(penerima.idPenerima))
            page.open(
                ft.SnackBar(
                    content=ft.Text(
                        "Donation request submitted. Recipient profile is ready for donations."
                    ),
                    bgcolor="#00AA00",
                )
            )
            page.update()

            form_data.update({k: "" for k in form_data})
            title_field.value = ""
            description_field.value = ""
            address_search.value = ""
            address_field.value = ""
            additional_detail_field.value = ""
            email_field.value = ""
            phone_field.value = ""
            needed_field.value = ""
            images.clear()
            update_media_section()
            check_form()
            page.update()
            page.go("/profile/orders-activity")
        except Exception as e:
            page.open(
                ft.SnackBar(
                    content=ft.Text(f"Failed to submit donation request: {e}"),
                    bgcolor="#FF5252",
                )
            )
            page.update()

    submit_button = ft.Container(
        bgcolor="#8F8F8F",
        border_radius=ft.BorderRadius(
            top_left=0,
            top_right=54,
            bottom_left=54,
            bottom_right=54,
        ),
        padding=ft.padding.symmetric(horizontal=50, vertical=12),
        alignment=ft.alignment.center,
        content=ft.Text(
            "Submit",
            color="#FFFFFF",
            size=18,
            weight="bold",
            font_family="SFPro",
        ),
        ink=True,
        on_click=submit_form,
        disabled=True,
    )

    # Initial state for submit button
    check_form()

    # ---------------------- MAIN LAYOUT -------------------------
    footer = Footer_black()
    nav_bar = NavigationBar(on_nav=lambda r: page.go(r), active="/donation", page=page)

    # left_column = ft.Column(
    #     controls=[general_info_card, detail_info_card],
    #     spacing=40,
    #     expand=True,
    #     horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    # )
    left_column = ft.Container(
        expand=True,
        content=ft.Column(
            spacing=30,
            controls=[
                general_info_card,
                detail_info_card,
            ],
        ),
    )

    # right_column = ft.Column(
    #     controls=[media_upload_card, needed_items_card, submit_button],
    #     spacing=40,
    #     expand=True,
    #     horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    # )
    right_column = ft.Container(
        width=550,
        content=ft.Column(
            spacing=30,
            controls=[media_upload_card, needed_items_card, submit_button],
        ),
    )

    main_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(
                        spacing=40,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            left_column,
                            right_column,
                        ],
                    ),
                    padding=ft.padding.symmetric(horizontal=60, vertical=60),
                ),
            ],
        ),
        bgcolor="#ffffff",
        border_radius=ft.border_radius.only(top_left=99, top_right=99),
    )

    footer_wrapper = ft.Container(
        content=Footer_black(),
        margin=ft.margin.only(top=-150),
    )

    scrollable_content = ft.Column(
        controls=[
            top_bar,
            main_section,
            ft.Container(height=150, bgcolor="#FFFFFF"),
            footer_wrapper,
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    return ft.View(
        route="/donation_request",
        appbar=nav_bar,
        # controls=[
        #     ft.SafeArea(
        #         content=ft.Column(
        #             controls=[
        #                 content,
        #             ],
        #             spacing=0,
        #             expand=True,
        #         )
        #     )
        # ],
        controls=[ft.SafeArea(content=scrollable_content, expand=True)],
        bgcolor="#161616",
        padding=0,
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        # scroll=ft.ScrollMode.AUTO,
    )
