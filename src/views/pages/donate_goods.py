import flet as ft
import os
from pathlib import Path
from ..components.navigation_bar import NavigationBar
from ..components.footer_black import Footer_black
from database.query.penerima_donasi import GetPenerimaById
from utils.helper import upload_image, is_format_allowed
from controllers.DonasiBarangManager import DonasiBarangManager

# Constants
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
ASSETS_UI = os.path.join(ASSETS_DIR, "ui")
FONT_SFPRO_PATH = os.path.join(ASSETS_DIR, "fonts", "SF-Pro-Display-Regular.otf")

LOGO_PATH = os.path.join(ASSETS_UI, "logo.png")
HERO_CURVE = os.path.join(ASSETS_UI, "hero_curve.png")


def DonateGoodsPage(page: ft.Page, idPenerima: int | None = None) -> ft.View:

    def parse_int(value):
        try:
            return int(str(value))
        except (TypeError, ValueError):
            return None

    recipient_name = "Recipient"
    recipient_address = ""
    owner_id = None
    rec = None
    manager = DonasiBarangManager()
    images = []
    if idPenerima:
        try:
            rec = GetPenerimaById(idPenerima)
            if rec:
                recipient_name = getattr(rec, "nama", recipient_name)
                recipient_address = getattr(rec, "alamat", "") or ""
                owner_id = parse_int(getattr(rec, "idPengguna", None))
        except Exception as ex:
            print(f"DonateGoods recipient load error: {ex}")
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
                        "Donate Goods",
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

    def info_card(title, children, border_radius=50, inner_padding=None):
        return ft.Container(
            bgcolor="#F6F6F6",
            border_radius=border_radius,
            padding=inner_padding or ft.padding.all(32),
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

    def text_field(**temp):
        base = {
            "bgcolor": "#FFFFFF",
            "border_radius": 12,
            "border_color": "#161616",
            "focused_border_color": "#161616",
            "text_style": ft.TextStyle(color="#1A1A1A"),
        }
        base.update(temp)
        return ft.TextField(**base)

    def form_field(label, field_control: ft.Control):
        return ft.Column(
            controls=[
                ft.Text(
                    label,
                    size=14,
                    weight=ft.FontWeight.W_600,
                    color="#000000",
                ),
                field_control,
            ],
            spacing=12,
        )

    product_name_field = text_field(
        hint_text="Enter product name",
    )
    description_field = text_field(
        hint_text="Tell us more about the goods",
        multiline=True,
        min_lines=5,
        max_lines=8,
    )
    category_field = text_field(
        hint_text="Select category",
    )
    email_field = text_field(
        hint_text="Enter email",
    )
    phone_field = text_field(
        hint_text="Enter phone number",
    )
    address_field = text_field(
        hint_text="Enter full address",
    )

    media_section = ft.Container()
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    def create_image_preview():
        if not images:
            return ft.Container(
                width=400,
                height=250,
                bgcolor="#FFFFFF",
                border_radius=20,
                alignment=ft.alignment.center,
                content=ft.Icon(ft.Icons.IMAGE_OUTLINED, size=72, color="#CCCCCC"),
            )
        return ft.Container(
            width=400,
            height=250,
            bgcolor="#FFFFFF",
            border_radius=20,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=ft.Image(
                src=images[-1]["preview_path"],
                fit=ft.ImageFit.COVER,
            ),
        )

    def create_thumbnail():
        if not images:
            return ft.Container(
                width=100,
                height=100,
                bgcolor="#F0F0F0",
                border_radius=15,
                alignment=ft.alignment.center,
                content=ft.Icon(ft.Icons.ADD, size=32, color="#BBBBBB"),
                on_click=trigger_file_picker,
            )
        return ft.Container(
            width=100,
            height=100,
            bgcolor="#FFFFFF",
            border_radius=15,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=ft.Image(
                src=images[0]["preview_path"],
                fit=ft.ImageFit.COVER,
            ),
        )

    def update_media_section():
        media_section.content = ft.Column(
            spacing=16,
            controls=[
                create_image_preview(),
                ft.Row(
                    controls=[create_thumbnail()],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=12,
                ),
            ],
        )
        page.update()

    def on_file_picked(e: ft.FilePickerResultEvent):
        if not e.files:
            return
        if len(images) >= 1:
            page.open(
                ft.SnackBar(
                    ft.Text("Only one image is allowed."),
                    bgcolor="#FFAA00",
                )
            )
            page.update()
            return
        for file in e.files:
            if len(images) >= 1:
                break
            if not is_format_allowed(file.name):
                page.open(
                    ft.SnackBar(
                        ft.Text("Please upload PNG, JPG, JPEG, WEBP, HEIC, or GIF."),
                        bgcolor="#FF4444",
                    )
                )
                page.update()
                continue
            images.append(
                {
                    "name": file.name,
                    "preview_path": str(Path(file.path).resolve()),
                    "size": file.size,
                }
            )
        update_media_section()

    def trigger_file_picker(e):
        if len(images) >= 1:
            page.open(
                ft.SnackBar(
                    ft.Text("You can upload only one image."),
                    bgcolor="#FFAA00",
                )
            )
            page.update()
            return
        file_picker.on_result = on_file_picked
        file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["png", "jpg", "jpeg", "webp", "heic", "gif"],
        )

    update_media_section()

    def form_data():
        return {
            "product_name": product_name_field.value.strip(),
            "description": description_field.value.strip(),
            "category": category_field.value.strip(),
            "email": email_field.value.strip(),
            "phone": phone_field.value.strip(),
            "address": address_field.value.strip(),
            "idPenerima": idPenerima,
        }

    def submit(payload: dict):
        if current_uid == None:
            page.open(
                ft.SnackBar(
                    ft.Text("Please log in before making a donation."),
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

        if not current_donatur_id:
            page.open(
                ft.SnackBar(
                    ft.Text("Please log in as a donor before making a donation."),
                    bgcolor="#FF4444",
                )
            )
            page.update()
            return

        if not payload.get("idPenerima"):
            page.open(
                ft.SnackBar(
                    ft.Text("Recipient information is missing."),
                    bgcolor="#FF4444",
                )
            )
            page.update()
            return

        if not payload["product_name"]:
            page.open(
                ft.SnackBar(
                    ft.Text("Product name is required."),
                    bgcolor="#FF4444",
                )
            )
            page.update()
            return

        if not images:
            page.open(
                ft.SnackBar(
                    ft.Text("Please upload at least one image."),
                    bgcolor="#FF4444",
                )
            )
            page.update()
            return

        try:
            foto_path = None
            if images:
                stored_path = upload_image(
                    images[0]["preview_path"], filename=Path(images[0]["name"]).stem
                )
                if stored_path:
                    foto_obj = Path(stored_path)
                    if not foto_obj.is_absolute():
                        foto_obj = (
                            Path(__file__).resolve().parents[2] / foto_obj
                        ).resolve()
                    foto_path = foto_obj.as_posix()
            manager.addDonasiBarang(
                {
                    "namaBarang": payload["product_name"],
                    "deskripsi": payload["description"],
                    "kategori": payload["category"],
                    "idDonatur": current_donatur_id,
                    "idPenerima": payload["idPenerima"],
                    "caraPengiriman": "kurir",
                    "foto": foto_path,
                }
            )
            page.open(
                ft.SnackBar(
                    ft.Text("Goods donation submitted."),
                    bgcolor="#00AA00",
                )
            )
            product_name_field.value = ""
            description_field.value = ""
            category_field.value = ""
            email_field.value = ""
            phone_field.value = ""
            address_field.value = ""
            images.clear()
            update_media_section()
            page.update()
            page.go("/profile/orders-activity")
        except Exception as ex:
            page.open(
                ft.SnackBar(
                    ft.Text(f"Failed to submit donation: {ex}"),
                    bgcolor="#FF4444",
                )
            )
            page.update()

    def handle_submit(e):
        data = form_data()
        submit(data)

    nav_bar = NavigationBar(
        on_nav=lambda route: page.go(route), active="/donation", page=page
    )

    main_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.ResponsiveRow(
                    columns=12,
                    spacing=30,
                    controls=[
                        ft.Container(
                            col={"xs": 12, "md": 7},
                            content=info_card(
                                f"General Information\n(Recipient: {recipient_name})",
                                [
                                    form_field("Product Name", product_name_field),
                                    form_field("Description", description_field),
                                    form_field("Category", category_field),
                                    ft.Text(
                                        f"Deliver to: {recipient_address or 'Recipient address will be shared after confirmation.'}",
                                        size=13,
                                        color="#555555",
                                    ),
                                ],
                            ),
                            border_radius=ft.border_radius.all(50),
                        ),
                        ft.Container(
                            col={"xs": 12, "md": 5},
                            content=info_card(
                                "Media Upload",
                                [
                                    ft.Text(
                                        "Upload one image of the goods to help the recipient verify the item.",
                                        size=14,
                                        color="#555555",
                                    ),
                                    media_section,
                                ],
                                border_radius=ft.border_radius.all(50),
                                inner_padding=ft.padding.all(40),
                            ),
                        ),
                    ],
                ),
                info_card(
                    "Contact Information",
                    [
                        ft.ResponsiveRow(
                            columns=12,
                            spacing=18,
                            controls=[
                                ft.Container(
                                    col={"xs": 12, "md": 6},
                                    content=form_field("Email", email_field),
                                ),
                                ft.Container(
                                    col={"xs": 12, "md": 6},
                                    content=form_field("Phone Number", phone_field),
                                ),
                            ],
                        )
                    ],
                    border_radius=ft.border_radius.all(50),
                    inner_padding=ft.padding.all(56),
                ),
                info_card(
                    "Shipping & Delivery",
                    [
                        form_field("Address", address_field),
                    ],
                    border_radius=ft.border_radius.all(50),
                    inner_padding=ft.padding.all(56),
                ),
                ft.Container(
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(top=10),
                    content=ft.GestureDetector(
                        on_tap=handle_submit,
                        mouse_cursor=ft.MouseCursor.CLICK,
                        content=ft.Container(
                            bgcolor="#000000",
                            width=320,
                            height=56,
                            border_radius=40,
                            alignment=ft.alignment.center,
                            content=ft.Text(
                                "Submit Approval",
                                color="#FFFFFF",
                                size=16,
                                weight=ft.FontWeight.W_600,
                            ),
                        ),
                    ),
                ),
            ],
            spacing=32,
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
        route="/donation/goods",
        controls=[ft.SafeArea(content=scrollable_content, expand=True)],
        bgcolor="#161616",
        padding=0,
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
