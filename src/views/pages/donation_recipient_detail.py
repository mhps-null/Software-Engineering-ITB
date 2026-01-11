import flet as ft
import os
from pathlib import Path
from sqlmodel import Session, select
from ..components.navigation_bar import NavigationBar
from ..components.footer_black import Footer_black
from controllers.DonasiBarangManager import DonasiBarangManager
from database.query.penerima_donasi import GetPenerimaById, GetAllPenerima
from database.query.barang_donasi import GetBarangDonasiByPenerima
from database.query.donatur import GetDonaturById
from database.connection import engine
from models.models import TransaksiEntity

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
ASSETS_UI = os.path.join(ASSETS_DIR, "ui")
FONT_SFPRO_PATH = os.path.join(ASSETS_DIR, "fonts", "SF-Pro-Display-Regular.otf")
DEFAULT_IMG = os.path.join(ASSETS_UI, "product_sample.jpg")
BASE_DIR = Path(__file__).resolve().parents[2]
ROOT_DIR = Path(__file__).resolve().parents[3]


def resolve(path: str | None):
    if not path:
        return Path(DEFAULT_IMG).resolve().as_posix()

    def as_path(p):
        try:
            return Path(p)
        except Exception:
            return None

    candidates = []
    p = as_path(path)
    if p:
        candidates.append(p)
        if not p.is_absolute():
            candidates.append(BASE_DIR / p)
            candidates.append(ROOT_DIR / p)
    for c in candidates:
        if c and c.exists():
            return c.resolve().as_posix()
    return Path(DEFAULT_IMG).resolve().as_posix()


def DonationRecipientDetailPage(
    page: ft.Page, idPenerima: int | None = None
) -> ft.View:

    page.fonts = {"SFPro": FONT_SFPRO_PATH}

    manager = DonasiBarangManager()
    recipient = None
    if idPenerima:
        try:
            recipient = GetPenerimaById(idPenerima)
        except Exception as e:
            print(f"Recipient detail load error: {e}")
    if recipient is None:
        try:
            all_rec = GetAllPenerima() or []
            recipient = all_rec[0] if all_rec else None
        except Exception as e:
            print(f"Recipient fallback load error: {e}")

    recipient_name = getattr(recipient, "nama", "Recipient")
    deliverable = getattr(recipient, "alamat", "") or "" + (
        getattr(recipient, "nomorTelepon", "") or ""
    )
    desc = getattr(recipient, "deskripsi", "") or ""
    main_img_src = resolve(getattr(recipient, "foto", None))

    def handle_donate(e, route: str):
        try:
            my_recipient_id = int(str(page.client_storage.get("idPenerima")))
        except (TypeError, ValueError):
            my_recipient_id = None
        if my_recipient_id and idPenerima and my_recipient_id == idPenerima:
            page.open(
                ft.SnackBar(
                    content=ft.Text("You cannot donate to your own request."),
                    bgcolor="#FFAA00",
                )
            )
            page.update()
            return
        page.go(route)

    # MAIN PHOTO (big)
    main_photo = ft.Container(
        width=380,
        height=300,
        bgcolor="#EDEDED",
        border_radius=25,
        alignment=ft.alignment.center,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=ft.Image(
            src=main_img_src,
            fit=ft.ImageFit.COVER,
            width=380,
            height=300,
        ),
    )

    # SUB PHOTOS (reuse main or placeholders)
    sub_photos = ft.Row(
        controls=[
            ft.Container(
                width=100,
                height=100,
                bgcolor="#EDEDED",
                border_radius=20,
                alignment=ft.alignment.center,
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                content=ft.Image(src=main_img_src, fit=ft.ImageFit.COVER),
            )
            for _ in range(3)
        ],
        spacing=15,
    )

    # TITLE + BUTTONS
    title_section = ft.Column(
        controls=[
            ft.Text(
                recipient_name,
                size=28,
                weight=ft.FontWeight.W_700,
                color="#161616",
                font_family="SFPro",
            ),
            ft.Container(height=10),
            # Donate Funds
            ft.Container(
                width=220,
                height=42,
                bgcolor="black",
                border_radius=25,
                alignment=ft.alignment.center,
                ink=True,
                on_click=lambda e, pid=idPenerima: handle_donate(
                    e, f"/donation/funds?idPenerima={pid or 0}"
                ),
                content=ft.Text(
                    "Donate Funds", color="white", weight=ft.FontWeight.W_600
                ),
            ),
            ft.Container(height=10),
            # Donate Goods
            ft.Container(
                width=220,
                height=42,
                bgcolor="black",
                border_radius=25,
                alignment=ft.alignment.center,
                ink=True,
                on_click=lambda e, pid=idPenerima: handle_donate(
                    e, f"/donation/goods?idPenerima={pid or 0}"
                ),
                content=ft.Text(
                    "Donate Goods", color="white", weight=ft.FontWeight.W_600
                ),
            ),
        ],
        spacing=8,
    )

    # HEADER BACK BUTTON
    top_bar = ft.Container(
        padding=ft.padding.only(left=20, top=10, bottom=10),
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color="#161616",
                    icon_size=26,
                    on_click=lambda e: page.go("/donation"),
                )
            ]
        ),
    )

    # DESCRIPTION (expand/collapse)
    def create_expandable(title, text):
        expanded = ft.Ref[bool]()
        expanded.current = False

        content_container = ft.Ref[ft.Container]()

        def toggle(e):
            expanded.current = not expanded.current
            content_container.current.visible = expanded.current
            page.update()

        return ft.Container(
            bgcolor="#FFFFFF",
            border_radius=30,
            border=ft.border.all(1, "#E2E2E2"),
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                title,
                                size=16,
                                weight=ft.FontWeight.W_700,
                                color="#161616",
                            ),
                            ft.Container(expand=True),
                            ft.IconButton(
                                icon=ft.Icons.KEYBOARD_ARROW_DOWN,
                                icon_size=20,
                                on_click=toggle,
                            ),
                        ]
                    ),
                    ft.Container(
                        ref=content_container,
                        visible=False,
                        content=ft.Text(
                            text,
                            size=13,
                            color="#555555",
                            selectable=True,
                        ),
                    ),
                ],
                spacing=10,
            ),
        )

    section_description = create_expandable("Description", desc)
    section_deliverables = create_expandable("Deliverables", deliverable)

    # DAFTAR DONATUR
    def get_donations_list():
        donations = []
        if not idPenerima:
            return donations

        try:
            goods_donations = GetBarangDonasiByPenerima(idPenerima) or []
            for item in goods_donations:
                donatur_id = getattr(item, "idDonatur", None)
                if donatur_id:
                    try:
                        donatur = GetDonaturById(donatur_id)
                        donations.append(
                            {
                                "id": getattr(item, "idBarangDonasi", 0),
                                "type": "goods",
                                "donatur_name": (
                                    getattr(donatur, "nama", "Anonymous")
                                    if donatur
                                    else "Anonymous"
                                ),
                                "item_name": getattr(item, "namaBarang", "-"),
                                "amount": None,
                            }
                        )
                    except Exception as e:
                        print(f"Error fetching donatur for goods: {e}")

            with Session(engine) as session:
                funds_donations = session.exec(
                    select(TransaksiEntity).where(
                        TransaksiEntity.idPenerima == idPenerima,
                        TransaksiEntity.jenisTransaksi == "donasi_uang",
                    )
                ).all()

                for trans in funds_donations:
                    donatur_id = getattr(trans, "idDonatur", None)
                    if donatur_id:
                        try:
                            donatur = GetDonaturById(donatur_id)
                            donations.append(
                                {
                                    "id": getattr(trans, "idTransaksi", 0),
                                    "type": "funds",
                                    "donatur_name": (
                                        getattr(donatur, "nama", "Anonymous")
                                        if donatur
                                        else "Anonymous"
                                    ),
                                    "item_name": None,
                                    "amount": getattr(trans, "jumlah", 0),
                                }
                            )
                        except Exception as e:
                            print(f"Error fetching donatur for funds: {e}")

            donations.sort(key=lambda x: x["id"], reverse=True)

        except Exception as e:
            print(f"Error getting donations list: {e}")

        return donations

    def create_donations_section():
        expanded = ft.Ref[bool]()
        expanded.current = False
        content_container = ft.Ref[ft.Container]()
        arrow_icon = ft.Ref[ft.IconButton]()

        donations = get_donations_list()
        total_donors = len(donations)
        total_funds = sum(
            d["amount"] for d in donations if d["type"] == "funds" and d["amount"]
        )

        def toggle(e):
            expanded.current = not expanded.current
            content_container.current.visible = expanded.current
            arrow_icon.current.icon = (
                ft.Icons.KEYBOARD_ARROW_UP
                if expanded.current
                else ft.Icons.KEYBOARD_ARROW_DOWN
            )
            page.update()

        donation_items = []

        if not donations:
            # empty state
            donation_items.append(
                ft.Container(
                    padding=ft.padding.all(20),
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.INBOX_OUTLINED, size=40, color="#CCCCCC"),
                            ft.Container(width=15),
                            ft.Text(
                                "No donations yet",
                                size=14,
                                color="#999999",
                                italic=True,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                )
            )
        else:
            for idx, donation in enumerate(donations):
                if donation["type"] == "funds":
                    icon = ft.Icon(ft.Icons.ATTACH_MONEY, size=24, color="#4CAF50")
                    type_label = "Funds Donation"
                    detail = f"Amount: IDR {int(donation['amount'] or 0):,}".replace(
                        ",", "."
                    )
                else:
                    icon = ft.Icon(ft.Icons.CARD_GIFTCARD, size=24, color="#1188ff")
                    type_label = "Goods Donation"
                    detail = f"Item: {donation['item_name']}"

                # single donation item
                item = ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                icon,
                                ft.Container(width=10),
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            donation["donatur_name"],
                                            size=14,
                                            weight=ft.FontWeight.W_600,
                                            color="#161616",
                                        ),
                                        ft.Text(
                                            type_label,
                                            size=12,
                                            color="#666666",
                                        ),
                                        ft.Text(
                                            detail,
                                            size=13,
                                            color="#333333",
                                            weight=ft.FontWeight.W_500,
                                        ),
                                    ],
                                    spacing=2,
                                ),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.START,
                        ),
                    ],
                    spacing=0,
                )

                donation_items.append(item)

                if idx < len(donations) - 1:
                    donation_items.append(
                        ft.Container(
                            height=1,
                            bgcolor="#E8E8E8",
                            margin=ft.margin.symmetric(vertical=15),
                        )
                    )

        # Summary header text
        summary_text = f"{total_donors} donor(s)"
        if total_funds > 0:
            summary_text += f" • Total Funds: IDR {int(total_funds):,}".replace(
                ",", "."
            )

        return ft.Container(
            bgcolor="#FFFFFF",
            border_radius=30,
            border=ft.border.all(1, "#E2E2E2"),
            padding=20,
            content=ft.Column(
                controls=[
                    # Header with summary
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "Daftar Donatur",
                                        size=16,
                                        weight=ft.FontWeight.W_700,
                                        color="#161616",
                                    ),
                                    ft.Text(
                                        summary_text,
                                        size=12,
                                        color="#666666",
                                    ),
                                ],
                                spacing=2,
                            ),
                            ft.Container(expand=True),
                            ft.IconButton(
                                ref=arrow_icon,
                                icon=ft.Icons.KEYBOARD_ARROW_DOWN,
                                icon_size=20,
                                on_click=toggle,
                            ),
                        ]
                    ),
                    # Content (donations list)
                    ft.Container(
                        ref=content_container,
                        visible=False,
                        content=ft.Column(
                            controls=donation_items,
                            spacing=0,
                        ),
                        padding=ft.padding.only(top=10),
                    ),
                ],
                spacing=10,
            ),
        )

    section_donations = create_donations_section()

    def recipient_card(item):
        rid = getattr(item, "idPenerima", 0)
        name = getattr(item, "nama", "Recipient")
        thumb = resolve(getattr(item, "foto", None))
        return ft.Column(
            spacing=8,
            width=220,
            controls=[
                # image placeholder
                ft.Container(
                    width=220,
                    height=140,
                    bgcolor="#EBEBEB",
                    border_radius=15,
                    alignment=ft.alignment.center,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    content=ft.Image(src=thumb, fit=ft.ImageFit.COVER),
                    ink=True,
                    on_click=lambda e, pid=rid: page.go(
                        f"/donation_recipient_detail?idPenerima={pid}"
                    ),
                ),
                # recipient name
                ft.Text(
                    name,
                    size=14,
                    weight=ft.FontWeight.W_600,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                    color="#161616",
                ),
                # "Donate" buttons
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Container(
                            width=100,
                            height=32,
                            bgcolor="#000000",
                            border_radius=12,
                            alignment=ft.alignment.center,
                            ink=True,
                            content=ft.Text("Donate", size=11, color="white"),
                            on_click=lambda e, pid=rid: page.go(
                                f"/donation_recipient_detail?idPenerima={pid}"
                            ),
                        ),
                        ft.Container(
                            width=90,
                            height=32,
                            border_radius=12,
                            border=ft.border.all(1, "#000000"),
                            alignment=ft.alignment.center,
                            ink=True,
                            content=ft.Text("View", size=11, color="#161616"),
                            on_click=lambda e, pid=rid: page.go(
                                f"/donation_recipient_detail?idPenerima={pid}"
                            ),
                        ),
                    ],
                ),
            ],
        )

    def get_latest_recipients():
        try:
            all_recipients = GetAllPenerima() or []

            filtered = [
                r
                for r in all_recipients
                if getattr(r, "idPenerima", None) != idPenerima
            ]

            sorted_recipients = sorted(
                filtered, key=lambda x: getattr(x, "idPenerima", 0), reverse=True
            )

            return sorted_recipients[:4]
        except Exception as e:
            print(f"Error getting recipient recommendations: {e}")
            return []

    recommended = get_latest_recipients()
    recommended_grid = ft.Row(
        controls=[recipient_card(r) for r in recommended],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
    )

    footer = Footer_black()
    nav = NavigationBar(on_nav=lambda r: page.go(r), page=page, active="/donation")

    # WHITE CONTAINER CONTENT
    white_container = ft.Container(
        bgcolor="white",
        border_radius=ft.border_radius.only(top_left=30, top_right=30),
        padding=40,
        width=1400,
        content=ft.Column(
            spacing=40,
            controls=[
                ft.Row(
                    spacing=40,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[main_photo, title_section],
                ),
                sub_photos,
                section_description,
                section_deliverables,
                section_donations,  # NEW: Daftar Donatur section
                ft.Text(
                    "You might also want to see",
                    size=20,
                    weight=ft.FontWeight.W_700,
                    color="#161616",
                ),
                recommended_grid,
            ],
        ),
    )

    # SCROLLABLE PAGE
    scroll_area = ft.Column(
        controls=[
            top_bar,
            white_container,
            ft.Container(height=50),
            footer,
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.View(
        route="/donation_recipient_detail",
        appbar=nav,
        bgcolor="#FFFFFF",
        controls=[ft.SafeArea(scroll_area)],
        padding=0,
        scroll=ft.ScrollMode.AUTO,
    )
