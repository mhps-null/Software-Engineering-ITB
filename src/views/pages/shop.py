import flet as ft
import os
from ..components.navigation_bar import NavigationBar
from ..components.footer_black import Footer_black
from controllers.BarangManager import BarangManager

# constants
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
ASSETS_UI = os.path.join(ASSETS_DIR, "ui")
FONT_SFPRO_PATH = os.path.join(ASSETS_DIR, "fonts", "SF-Pro-Display-Regular.otf")
HERO_DONATION_PATH = os.path.join(ASSETS_UI, "hero_shop_1.jpg")


def ShopPage(page: ft.Page) -> ft.View:

    page.fonts = {"SFPro": FONT_SFPRO_PATH}

    # state management
    current_page = ft.Ref[int]()
    current_page.current = 1
    current_category = ft.Ref[str]()
    current_category.current = "All"
    search_query = ft.Ref[str]()
    search_query.current = ""
    products_per_page = 9

    all_products = BarangManager.list_products()

    def is_logged_in():
        return bool(str(page.client_storage.get("idPengguna") or "").strip())

    categories_set = set()
    for p in all_products:
        if p.kategori:
            categories_set.add(p.kategori)
    categories_list = ["All"] + sorted(categories_set)

    # HERO SECTION
    hero_section = ft.Container(
        width=1400,
        content=ft.Stack(
            controls=[
                # ft.Container(
                #     src=os.path.join(ASSETS_UI, "hero_donation.png"),
                #     width=1400,
                #     height=400,
                #     # bgcolor="#3A3A3A",
                # ),
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
                # overlay text
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Buy,",
                                size=48,
                                weight=ft.FontWeight.W_700,
                                font_family="SFPro",
                                color="#FFFFFF",
                            ),
                            ft.Text(
                                "Sell, and",
                                size=48,
                                weight=ft.FontWeight.W_700,
                                font_family="SFPro",
                                color="#FFFFFF",
                            ),
                            ft.Text(
                                "Trade Preloved Items",
                                size=48,
                                weight=ft.FontWeight.W_700,
                                font_family="SFPro",
                                color="#FFFFFF",
                            ),
                        ],
                        spacing=0,
                    ),
                    padding=ft.padding.only(left=60, top=40),
                    alignment=ft.alignment.center_left,
                ),
            ],
        ),
        margin=ft.margin.only(bottom=0),
    )

    # SELL ITEM SECTION
    sell_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Sell an Item",
                    size=32,
                    weight=ft.FontWeight.W_700,
                    font_family="SFPro",
                    color="#000000",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=8),
                ft.Text(
                    "List your item with photos and details - fast and easy.",
                    size=14,
                    weight=ft.FontWeight.W_400,
                    font_family="SFPro",
                    color="#666666",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=20),
                ft.ElevatedButton(
                    content=ft.Text(
                        "Sell Now",
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
                        page.go("/sell")
                        if is_logged_in()
                        else page.open(
                            ft.SnackBar(
                                ft.Text("Please log in before listing your product."),
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
        # border_radius=ft.border_radius.only(top_left=30, top_right=30, bottom_left=30, bottom_right=30),
        border_radius=ft.border_radius.all(54),
        padding=ft.padding.all(40),
        bgcolor="#F5F5F5",
        margin=ft.margin.only(bottom=40),
    )

    # FILTER & PRODUCT FUNCTIONS
    def get_filtered_products():
        filtered = all_products

        if current_category.current != "All":
            filtered = [
                p for p in filtered if (p.kategori or "") == current_category.current
            ]

        if search_query.current:
            filtered = [
                p
                for p in filtered
                if search_query.current.lower() in (p.namaBarang or "").lower()
            ]

        return filtered

    def get_total_pages():
        total_products = len(get_filtered_products())
        return max(1, (total_products + products_per_page - 1) // products_per_page)

    def get_current_products():
        filtered = get_filtered_products()
        start_idx = (current_page.current - 1) * products_per_page
        end_idx = start_idx + products_per_page
        return filtered[start_idx:end_idx]

    # PRODUCT CARD
    def create_product_card(product):
        return ft.Container(
            content=ft.Column(
                controls=[
                    # product image placeholder
                    ft.Container(
                        content=(
                            ft.Icon(
                                name=ft.Icons.IMAGE_OUTLINED,
                                size=60,
                                color="#CCCCCC",
                            )
                            if not getattr(product, "foto", None)
                            else ft.Image(
                                src_base64=product.foto,
                                fit=ft.ImageFit.COVER,
                            )
                        ),
                        width=250,
                        height=200,
                        bgcolor="#E8E8E8",
                        border_radius=15,
                        alignment=ft.alignment.center,
                        ink=True,
                        on_click=lambda e, p=product: page.go(
                            f"/product/{p.idBarang}?from_page={current_page.current}&from_category={current_category.current}"
                        ),
                    ),
                    ft.Container(height=12),
                    # product name
                    ft.Container(
                        content=ft.Text(
                            getattr(product, "namaBarang", "-"),
                            size=16,
                            weight=ft.FontWeight.W_600,
                            font_family="SFPro",
                            color="#000000",
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        ink=True,
                        on_click=lambda e, p=product: page.go(
                            f"/product/{p.idBarang}?from_page={current_page.current}&from_category={current_category.current}"
                        ),
                    ),
                    ft.Container(height=4),
                    # product price
                    ft.Text(
                        f"IDR{int(product.harga or 0):,}".replace(",", "."),
                        size=18,
                        weight=ft.FontWeight.W_700,
                        font_family="SFPro",
                        color="#0088ff",
                    ),
                    ft.Container(height=12),
                    # action buttons
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                content=ft.Text(
                                    "View details",
                                    size=12,
                                    weight=ft.FontWeight.W_600,
                                    color="#FFFFFF",
                                ),
                                width=115,
                                bgcolor="#000000",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=15),
                                    padding=ft.padding.symmetric(
                                        horizontal=8, vertical=10
                                    ),
                                ),
                                on_click=lambda e, p=product: page.go(
                                    f"/product/{p.idBarang}?from_page={current_page.current}&from_category={current_category.current}"
                                ),
                            ),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                ],
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=ft.padding.all(15),
            width=280,
        )

    # SIDEBAR (CATEGORIES)
    def create_category_button(category):
        is_active = current_category.current == category
        return ft.Container(
            content=ft.Text(
                category,
                size=14,
                weight=ft.FontWeight.W_600 if is_active else ft.FontWeight.W_400,
                font_family="SFPro",
                color="#0088ff" if is_active else "#666666",
            ),
            padding=ft.padding.symmetric(horizontal=0, vertical=5),
            ink=True,
            on_click=lambda e, cat=category: handle_category_change(cat),
        )

    sidebar = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Categories",
                    size=18,
                    weight=ft.FontWeight.W_700,
                    font_family="SFPro",
                    color="#000000",
                ),
                ft.Container(height=10),
                ft.Column(
                    controls=[create_category_button(cat) for cat in categories_list],
                    spacing=8,
                ),
                ft.Container(height=10),
                # ft.TextButton(
                #     content=ft.Row(
                #         controls=[
                #             ft.Text(
                #                 "See More",
                #                 size=14,
                #                 weight=ft.FontWeight.W_500,
                #                 color="#0088ff",
                #             ),
                #             ft.Icon(
                #                 name=ft.Icons.CHEVRON_RIGHT,
                #                 size=16,
                #                 color="#0088ff",
                #             ),
                #         ],
                #         spacing=4,
                #     ),
                #     on_click=lambda e: print("Show more categories"),
                # ),
            ],
            spacing=0,
        ),
        width=200,
        padding=ft.padding.all(20),
    )

    # SEARCH BAR
    search_field = ft.TextField(
        hint_text="Search in your favorite",
        hint_style=ft.TextStyle(
            size=14,
            weight=ft.FontWeight.W_400,
            color="#B3B3B3",
        ),
        text_style=ft.TextStyle(
            size=14,
            weight=ft.FontWeight.W_500,
            color="#161616",
        ),
        border_radius=99,
        filled=True,
        bgcolor="#FFFFFF",
        border_color="#161616",
        prefix_icon=ft.Icons.SEARCH,
        suffix=ft.Container(
            content=ft.Text(
                "Search",
                size=14,
                weight=ft.FontWeight.W_600,
                color="#FFFFFF",
            ),
            padding=ft.padding.symmetric(horizontal=14, vertical=5),
            bgcolor="#000000",
            border_radius=30,
            ink=True,
            on_click=lambda e: handle_search(),
        ),
        on_submit=lambda e: handle_search(),
    )

    # PAGINATION
    def create_pagination():
        total_pages = get_total_pages()
        pagination_buttons = []

        # previous button
        pagination_buttons.append(
            ft.TextButton(
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.CHEVRON_LEFT, size=16),
                        ft.Text("Previous", size=14, color="#161616"),
                    ],
                    spacing=4,
                ),
                disabled=current_page.current == 1,
                on_click=lambda e: handle_page_change(current_page.current - 1),
            )
        )

        # page numbers
        for i in range(1, min(total_pages + 1, 7)):
            is_current = i == current_page.current
            pagination_buttons.append(
                ft.Container(
                    content=ft.Text(
                        str(i),
                        size=14,
                        weight=(
                            ft.FontWeight.W_600 if is_current else ft.FontWeight.W_400
                        ),
                        color="#FFFFFF" if is_current else "#000000",
                    ),
                    width=36,
                    height=36,
                    bgcolor="#000000" if is_current else "transparent",
                    border_radius=18,
                    alignment=ft.alignment.center,
                    ink=True,
                    on_click=lambda e, page_num=i: handle_page_change(page_num),
                )
            )

        if total_pages > 6:
            pagination_buttons.append(ft.Text("...", size=14, color="#666666"))

        # next button
        pagination_buttons.append(
            ft.TextButton(
                content=ft.Row(
                    controls=[
                        ft.Text("Next", size=14, color="#161616"),
                        ft.Icon(name=ft.Icons.CHEVRON_RIGHT, size=16),
                    ],
                    spacing=4,
                ),
                disabled=current_page.current >= total_pages,
                on_click=lambda e: handle_page_change(current_page.current + 1),
            )
        )

        return ft.Row(
            controls=pagination_buttons,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        )

    # PRODUCT GRID
    product_grid = ft.Ref[ft.Column]()
    pagination_row = ft.Ref[ft.Row]()

    def update_product_display():
        products = get_current_products()

        # 3 products per row
        rows = []
        for i in range(0, len(products), 3):
            row_products = products[i : i + 3]
            rows.append(
                ft.Row(
                    controls=[create_product_card(p) for p in row_products],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.START,
                )
            )

        product_grid.current.controls = rows
        pagination_row.current.controls = [create_pagination()]
        page.update()

    # eVENT HANDLERS
    def handle_category_change(category):
        current_category.current = category
        current_page.current = 1
        update_product_display()

        # update sidebar buttons
        sidebar.content.controls[2] = ft.Column(
            controls=[create_category_button(cat) for cat in categories_list],
            spacing=8,
        )
        page.update()

    def handle_search():
        search_query.current = search_field.value or ""
        current_page.current = 1
        update_product_display()

    def handle_page_change(new_page):
        total_pages = get_total_pages()
        if 1 <= new_page <= total_pages:
            current_page.current = new_page
            update_product_display()

    # MAIN CONTENT
    main_content = ft.Column(
        controls=[
            # discover header + search
            ft.Row(
                controls=[
                    ft.Text(
                        "Discover",
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
                "Preloved products from trusted sellers across various collections.",
                size=14,
                weight=ft.FontWeight.W_400,
                font_family="SFPro",
                color="#666666",
            ),
            ft.Container(height=30),
            # product grid
            ft.Column(
                ref=product_grid,
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

    # CONTENT BODY
    # initial load
    update_product_display()

    # content body inside white rounded container
    content_body = ft.Row(
        controls=[
            sidebar,
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

    sell_container = ft.Container(
        content=sell_section,
        margin=ft.margin.only(bottom=40, top=40),
        width=1400,
    )

    # white rounded container that wraps everything below hero
    white_container = ft.Container(
        content=ft.Column(
            controls=[
                # sell_section,
                content_body,
            ],
            spacing=0,
        ),
        bgcolor="#FFFFFF",
        border_radius=ft.border_radius.only(top_left=30, top_right=30),
        padding=ft.padding.only(left=40, right=40, top=0, bottom=40),
        width=1400,
    )

    # nav_bar = NavigationBar(on_nav=lambda route: page.go(route))
    nav_bar = NavigationBar(
        on_nav=lambda route: page.go(route), active="/shop", page=page
    )

    footer = ft.Container(
        content=Footer_black(),
        margin=ft.margin.only(top=-150),
    )

    need_padding = ft.Container(
        content=ft.Column(
            controls=[
                hero_section,
                sell_container,
                white_container,
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
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

    return ft.View(
        route="/shop",
        appbar=nav_bar,
        controls=[ft.SafeArea(content=scrollable_content, expand=True)],
        bgcolor="#FFFFFF",
        padding=0,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )
