import flet as ft
import os
from pathlib import Path

from ..components.navigation_bar import NavigationBar
from ..components.footer_black import Footer_black
from controllers.DonasiBarangManager import DonasiBarangManager

# constants
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
ASSETS_UI = os.path.join(ASSETS_DIR, "ui")
FONT_SFPRO_PATH = os.path.join(ASSETS_DIR, "fonts", "SF-Pro-Display-Regular.otf")
HERO_DONATION_PATH = os.path.join(ASSETS_UI, "hero_donation.jpg")
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


def DonationPage(page: ft.Page) -> ft.View:

    # Register fonts
    page.fonts = {"SFPro": FONT_SFPRO_PATH}

    # STATE
    current_page = ft.Ref[int]()
    current_page.current = 1
    items_per_page = 12
    is_logged_in = bool(str(page.client_storage.get("idPengguna") or "").strip())
    search_query = ft.Ref[str]()
    search_query.current = ""

    # DATA
    recipients = []
    barang_manager = DonasiBarangManager()
    try:
        recipients = barang_manager.listPenerima() or []
        for r in recipients:
            try:
                resolved = resolve(getattr(r, "foto", None))
                print(
                    f"[Donation] Recipient id={getattr(r, 'idPenerima', None)} "
                    f"name={getattr(r, 'nama', '')} "
                    f"foto_raw={getattr(r, 'foto', None)} "
                    f"foto_resolved={resolved}"
                )
            except Exception as ex:
                print(f"[Donation] Failed to log recipient thumb: {ex}")
    except Exception as e:
        print(f"Donation page error: {e}")

    # FILTERING FUNCTIONS
    def get_filtered():
        data = recipients or []
        if not search_query.current:
            return data
        q = search_query.current.lower()
        return [d for d in data if q in (getattr(d, "nama", "") or "").lower()]

    def get_page_count():
        total = len(get_filtered())
        return max(1, (total + items_per_page - 1) // items_per_page)

    def get_current_items():
        f = get_filtered()
        start = (current_page.current - 1) * items_per_page
        end = start + items_per_page
        return f[start:end]

    # HERO SECTION
    hero_section = ft.Container(
        width=1400,
        content=ft.Stack(
            controls=[
                ft.Container(
                    expand=True,
                    border_radius=ft.border_radius.all(30),
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    content=ft.Image(
                        src=HERO_DONATION_PATH,
                        expand=True,
                        width=1400,
                        height=500,
                        fit=ft.ImageFit.COVER,
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Give",
                                size=52,
                                weight=ft.FontWeight.W_700,
                                font_family="SFPro",
                                color="white",
                            ),
                            ft.Text(
                                "With",
                                size=52,
                                weight=ft.FontWeight.W_700,
                                font_family="SFPro",
                                color="white",
                            ),
                            ft.Text(
                                "Purpose",
                                size=52,
                                weight=ft.FontWeight.W_700,
                                font_family="SFPro",
                                color="white",
                            ),
                        ],
                        spacing=0,
                    ),
                    padding=ft.padding.only(left=60, top=40),
                    alignment=ft.alignment.center_left,
                ),
            ]
        ),
        margin=ft.margin.only(bottom=0),
    )

    request_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Request Donation",
                    size=32,
                    weight=ft.FontWeight.W_700,
                    font_family="SFPro",
                    color="#000000",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=8),
                ft.Text(
                    "Share what you need and let donors support your cause",
                    size=14,
                    weight=ft.FontWeight.W_400,
                    font_family="SFPro",
                    color="#666666",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=20),
                ft.ElevatedButton(
                    content=ft.Text(
                        "Request",
                        size=16,
                        weight=ft.FontWeight.W_600,
                        color="#FFFFFF",
                    ),
                    bgcolor="#0088ff",
                    color="#FFFFFF",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=20),
                        padding=ft.padding.symmetric(horizontal=40, vertical=15),
                    ),
                    on_click=lambda e: (
                        page.go("/donation_request")
                        if is_logged_in
                        else page.open(
                            ft.SnackBar(
                                ft.Text("Please log in before opening a donation."),
                                bgcolor="#FFAA00",
                            )
                        )
                    ),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
        width=1400,
        border_radius=ft.border_radius.all(54),
        padding=ft.padding.all(40),
        bgcolor="#F5F5F5",
        margin=ft.margin.only(top=40, bottom=40),
    )

    # SEARCH BAR
    search_field = ft.TextField(
        hint_text="Search your recipients",
        bgcolor="#FFFFFF",
        border_radius=99,
        filled=True,
        border_color="#161616",
        prefix_icon=ft.Icons.SEARCH,
        on_submit=lambda e: handle_search(),
        suffix=ft.Container(
            content=ft.Text("Search", color="white", size=14),
            bgcolor="#000000",
            padding=ft.padding.symmetric(horizontal=14, vertical=6),
            border_radius=20,
            ink=True,
            on_click=lambda e: handle_search(),
        ),
    )

    # GRID ITEM (recipient card)
    def recipient_card(item):
        name = getattr(item, "nama", "-")
        idPenerima = getattr(item, "idPenerima", 0)
        thumb = resolve(
            getattr(item, "foto", None)
            or getattr(item, "image", None)
            or getattr(item, "thumbnail", None)
        )
        return ft.Container(
            width=300,
            content=ft.Column(
                controls=[
                    ft.Container(
                        width=250,
                        height=160,
                        bgcolor="#EEEEEE",
                        border_radius=20,
                        alignment=ft.alignment.center,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        content=ft.Image(
                            src=thumb,
                            fit=ft.ImageFit.COVER,
                            width=250,
                            height=160,
                        ),
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        name,
                        size=14,
                        max_lines=2,
                        color="#161616",
                        overflow=ft.TextOverflow.ELLIPSIS,
                        weight=ft.FontWeight.W_600,
                        font_family="SFPro",
                    ),
                    ft.Container(height=10),
                    ft.Container(
                        content=ft.Text("Find out more", size=12, color="white"),
                        bgcolor="black",
                        width=120,
                        height=36,
                        alignment=ft.alignment.center,
                        border_radius=20,
                        ink=True,
                        on_click=lambda e, pid=idPenerima: page.go(
                            f"/donation_recipient_detail?idPenerima={pid}"
                        ),
                    ),
                ],
                spacing=0,
            ),
        )

    # PAGINATION
    pagination_row = ft.Ref[ft.Row]()

    def create_pagination():
        total = get_page_count()
        items = []

        # prev
        items.append(
            ft.TextButton(
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.CHEVRON_LEFT, size=16),
                        ft.Text("Previous", size=14, color="#161616"),
                    ],
                    spacing=4,
                ),
                disabled=current_page.current == 1,
                on_click=lambda e: change_page(current_page.current - 1),
            )
        )

        # numbers
        for i in range(1, min(total, 6) + 1):
            items.append(
                ft.Container(
                    content=ft.Text(
                        str(i),
                        color="white" if i == current_page.current else "black",
                        weight=ft.FontWeight.W_600,
                    ),
                    width=34,
                    height=34,
                    bgcolor="black" if i == current_page.current else None,
                    alignment=ft.alignment.center,
                    border_radius=17,
                    ink=True,
                    on_click=lambda e, p=i: change_page(p),
                )
            )

        # next
        items.append(
            ft.TextButton(
                content=ft.Row(
                    controls=[
                        ft.Text("Next", size=14, color="#161616"),
                        ft.Icon(name=ft.Icons.CHEVRON_RIGHT, size=16),
                    ],
                    spacing=4,
                ),
                disabled=current_page.current >= total,
                on_click=lambda e: change_page(current_page.current + 1),
            )
        )

        return ft.Row(items, alignment=ft.MainAxisAlignment.CENTER)

    # GRID DISPLAY + UPDATE SYSTEM
    recipients_grid = ft.Ref[ft.Column]()

    def update_display():
        if recipients_grid.current is None or pagination_row.current is None:
            return

        items = get_current_items()
        rows = []

        if items:
            # 4 per row
            for i in range(0, len(items), 4):
                chunk = items[i : i + 4]
                rows.append(
                    ft.Row(
                        controls=[recipient_card(x) for x in chunk],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.START,
                    )
                )
        else:
            rows.append(
                ft.Text(
                    "No recipients found.",
                    size=16,
                    weight=ft.FontWeight.W_500,
                    color="#666666",
                )
            )
        recipients_grid.current.controls = rows
        pagination_row.current.controls = [create_pagination()]
        page.update()

    # SEARCH HANDLER
    def handle_search():
        search_query.current = search_field.value or ""
        current_page.current = 1
        update_display()

    # PAGE CHANGE
    def change_page(num):
        total = get_page_count()
        if 1 <= num <= total:
            current_page.current = num
            update_display()

    # Main Content
    main_content = ft.Column(
        controls=[
            # discover header + search
            ft.Row(
                controls=[
                    ft.Text(
                        "Donation",
                        size=64,
                        weight=ft.FontWeight.W_700,
                        font_family="SFPro",
                        color="#161616",
                    ),
                    ft.Container(expand=True),
                    ft.Container(
                        content=search_field,
                        width=500,
                        height=44,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Container(height=10),
            ft.Text(
                "Browse verified recipients and select where your donation will go.",
                size=14,
                weight=ft.FontWeight.W_400,
                font_family="SFPro",
                color="#161616",
            ),
            ft.Container(height=30),
            # recipients grid
            ft.Column(
                ref=recipients_grid,
                controls=[],
                spacing=20,
            ),
            ft.Container(height=40),
            # pagination
            ft.Row(
                ref=pagination_row,
                controls=[],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        spacing=0,
        expand=True,
    )

    content_body = ft.Row(
        controls=[
            ft.Container(width=30),
            ft.Container(
                content=main_content,
                expand=True,
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START,
        spacing=0,
    )
    # MAIN BODY (white container)
    white_container = ft.Container(
        content=ft.Column(
            controls=[
                content_body,
            ],
            spacing=0,
        ),
        bgcolor="#FFFFFF",
        border_radius=ft.border_radius.only(top_left=30, top_right=30),
        padding=ft.padding.only(left=40, right=40, top=0, bottom=40),
        width=1400,
    )

    # footer = Footer_black()
    footer = ft.Container(
        content=Footer_black(),
        margin=ft.margin.only(top=-150),
    )
    nav_bar = NavigationBar(
        on_nav=lambda route: page.go(route), active="/donation", page=page
    )

    need_padding = ft.Container(
        content=ft.Column(
            controls=[
                hero_section,
                request_card,
                white_container,
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.top_center,
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        expand=True,
    )

    scrollable_content = ft.Column(
        controls=[
            need_padding,
            ft.Container(height=200, bgcolor="#FFFFFF"),
            footer,
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # # SCROLL AREA
    # content = ft.Column(
    #     controls=[
    #         hero_section,
    #         request_card,
    #         white_container,
    #         ft.Container()
    #         footer,
    #     ],
    #     spacing=0,
    #     scroll=ft.ScrollMode.AUTO,
    #     horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    # )

    # page_body = ft.Container(
    #     content=content,
    #     alignment=ft.alignment.top_center,
    #     padding=ft.padding.symmetric(horizontal=20, vertical=10),
    #     expand=True,
    # )

    page.update()
    update_display()
    return ft.View(
        route="/donation",
        appbar=nav_bar,
        controls=[ft.SafeArea(content=scrollable_content, expand=True)],
        bgcolor="#FFFFFF",
        padding=0,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )
