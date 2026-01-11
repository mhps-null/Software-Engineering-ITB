import flet as ft
import os
import time
from ..components.navigation_bar import NavigationBar
from ..components.footer_black import Footer_black
from controllers.BarangManager import BarangManager

# Constants
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
ASSETS_UI = os.path.join(ASSETS_DIR, "ui")
FONT_SFPRO_PATH = os.path.join(ASSETS_DIR, "fonts", "SF-Pro-Display-Regular.otf")


def ProductDetailPage(
    page: ft.Page, product_id: int, from_page: int = 1, from_category: str = "All"
) -> ft.View:
    page.fonts = {"SFPro": FONT_SFPRO_PATH}

    product = BarangManager.get_product(product_id)

    if not product:
        page.go("/shop")
        return

    seller = None
    if product.idPenjual:
        seller = BarangManager.get_seller(product.idPenjual)

    def get_id(value):
        if value in (None, "", "None"):
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            try:
                return int(str(value))
            except (TypeError, ValueError):
                return None

    is_sold_out = bool(getattr(product, "isSold", False))

    def handle_checkout_click(e, target_product=None):
        target = target_product or product
        if not target:
            return

        buyer_id = get_id(page.client_storage.get("idPembeli"))
        if not buyer_id:
            page.open(
                ft.SnackBar(
                    content=ft.Text("Please log in before checking out."),
                    bgcolor="#FFAA00",
                )
            )
            page.update()
            return

        seller_id = get_id(page.client_storage.get("idPenjual"))
        is_self = bool(
            target
            and getattr(target, "idPenjual", None)
            and seller_id
            and getattr(target, "idPenjual") == seller_id
        )

        if getattr(target, "isSold", False):
            page.open(
                ft.SnackBar(
                    content=ft.Text("This product has been sold out."),
                    bgcolor="#FFAA00",
                )
            )
            page.update()
            return

        if is_self:
            page.open(
                ft.SnackBar(
                    content=ft.Text("You cannot checkout your own product."),
                    bgcolor="#FFAA00",
                )
            )
            page.update()
            return

        page.go(f"/checkout?product_id={target.idBarang}")

    product_images = []
    if getattr(product, "foto", None):
        product_images.append(product.foto)

    # state management
    current_image_index = ft.Ref[int]()
    current_image_index.current = 0
    description_expanded = ft.Ref[bool]()
    description_expanded.current = False
    shipping_expanded = ft.Ref[bool]()
    shipping_expanded.current = False

    carousel_interval = 3.5

    def create_main_image():
        if product_images:
            return ft.Container(
                content=ft.Image(
                    src_base64=product_images[
                        current_image_index.current % len(product_images)
                    ],
                    fit=ft.ImageFit.CONTAIN,
                ),
                width=400,
                height=480,
                bgcolor="#E8E8E8",
                border_radius=54,
                alignment=ft.alignment.center,
            )
        return ft.Container(
            content=ft.Icon(
                name=ft.Icons.IMAGE_OUTLINED,
                size=120,
                color="#CCCCCC",
            ),
            width=400,
            height=480,
            bgcolor="#E8E8E8",
            border_radius=54,
            alignment=ft.alignment.center,
        )

    main_image = ft.Ref[ft.Container]()

    def create_thumbnail(index):
        is_active = current_image_index.current == index
        thumbnail = ft.Icon(
            name=ft.Icons.IMAGE_OUTLINED,
            size=30,
            color="#999999" if is_active else "#CCCCCC",
        )
        if index < len(product_images):
            thumbnail = ft.Image(
                src_base64=product_images[index],
                fit=ft.ImageFit.COVER,
            )
        return ft.Container(
            content=thumbnail,
            width=100,
            height=100,
            bgcolor="#F5F5F5" if is_active else "#E8E8E8",
            border_radius=30,
            border=ft.border.all(3, "#0088ff" if is_active else "transparent"),
            alignment=ft.alignment.center,
            ink=True,
            on_click=lambda e, idx=index: change_image(idx),
        )

    thumbnails_row = ft.Ref[ft.Row]()

    def change_image(index):
        current_image_index.current = index
        if main_image.current:
            main_image.current.content = create_main_image()
        update_thumbnails()
        page.update()

    def update_thumbnails():
        thumbnails_row.current.controls = [
            create_thumbnail(i) for i in range(len(product_images) or 1)
        ]

    def auto_carousel():
        if len(product_images) < 2:
            return
        while True:
            time.sleep(carousel_interval)
            if current_image_index.current < len(product_images) - 1:
                current_image_index.current += 1
            else:
                current_image_index.current = 0
            if main_image.current:
                main_image.current.content = create_main_image()
            update_thumbnails()
            page.update()

    # start auto-carousel in background
    import threading

    carousel_thread = threading.Thread(target=auto_carousel, daemon=True)
    carousel_thread.start()

    image_gallery = ft.Column(
        controls=[
            ft.Container(
                ref=main_image,
                content=create_main_image(),
            ),
            ft.Container(height=15),
            ft.Row(
                ref=thumbnails_row,
                controls=[create_thumbnail(i) for i in range(len(product_images) or 1)],
                spacing=10,
            ),
        ],
        spacing=0,
    )

    # PRODUCT INFO SECTION
    product_info = ft.Column(
        controls=[
            # category
            ft.Container(height=30),
            ft.Container(
                content=ft.Text(
                    product.kategori or "-",
                    size=14,
                    weight=ft.FontWeight.W_600,
                    color="#000000",
                ),
                padding=ft.padding.symmetric(horizontal=15, vertical=3),
                border=ft.border.all(1, "#000000"),
                border_radius=30,
                width=None,
            ),
            # product name
            ft.Text(
                getattr(product, "namaBarang", "-"),
                size=42,
                weight=ft.FontWeight.W_700,
                font_family="SFPro",
                color="#000000",
                max_lines=3,
            ),
            ft.Container(height=10),
            # seller info
            ft.Text(
                f"by {seller.nama}" if seller else "",
                size=14,
                weight=ft.FontWeight.W_400,
                font_family="SFPro",
                color="#666666",
            ),
            ft.Container(height=20),
            # price
            ft.Text(
                f"IDR{int(product.harga or 0):,}".replace(",", "."),
                size=32,
                weight=ft.FontWeight.W_700,
                font_family="SFPro",
                color="#0088ff",
            ),
            ft.Container(height=170),
            # action buttons
            ft.Row(
                controls=[
                    ft.OutlinedButton(
                        content=ft.Text(
                            "Trade In",
                            size=14,
                            weight=ft.FontWeight.W_500,
                            color="#161616",
                        ),
                        width=170,
                        height=40,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=54),
                            side=ft.BorderSide(1.5, "#000000"),
                        ),
                        on_click=lambda e: page.go(
                            f"/product_tradein?product_id={product.idBarang}"
                        ),
                    ),
                ],
                spacing=15,
            ),
            ft.Container(height=15),
            ft.ElevatedButton(
                content=ft.Text(
                    "Sold Out" if is_sold_out else "Checkout",
                    size=14,
                    weight=ft.FontWeight.W_600,
                    color="#FFFFFF",
                ),
                width=355,
                height=40,
                bgcolor="#555555" if is_sold_out else "#161616",
                disabled=is_sold_out,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=54),
                ),
                on_click=None if is_sold_out else handle_checkout_click,
            ),
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.START,
    )

    # COLLAPSIBLE SECTIONS
    description_content = ft.Ref[ft.Container]()
    shipping_content = ft.Ref[ft.Container]()
    description_icon = ft.Ref[ft.Icon]()
    shipping_icon = ft.Ref[ft.Icon]()

    def toggle_description(e):
        description_expanded.current = not description_expanded.current
        description_content.current.height = None if description_expanded.current else 0
        description_content.current.visible = description_expanded.current
        description_icon.current.name = (
            ft.Icons.KEYBOARD_ARROW_UP
            if description_expanded.current
            else ft.Icons.KEYBOARD_ARROW_DOWN
        )
        page.update()

    def toggle_shipping(e):
        shipping_expanded.current = not shipping_expanded.current
        shipping_content.current.height = None if shipping_expanded.current else 0
        shipping_content.current.visible = shipping_expanded.current
        shipping_icon.current.name = (
            ft.Icons.KEYBOARD_ARROW_UP
            if shipping_expanded.current
            else ft.Icons.KEYBOARD_ARROW_DOWN
        )
        page.update()

    description_section = ft.Container(
        content=ft.Column(
            controls=[
                # header
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(
                                "Description",
                                size=18,
                                weight=ft.FontWeight.W_700,
                                font_family="SFPro",
                                color="#000000",
                            ),
                            ft.Container(expand=True),
                            ft.Icon(
                                ref=description_icon,
                                name=ft.Icons.KEYBOARD_ARROW_DOWN,
                                size=24,
                                color="#000000",
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=ft.padding.all(20),
                    ink=True,
                    on_click=toggle_description,
                ),
                # content
                ft.Container(
                    ref=description_content,
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                getattr(product, "deskripsi", "-"),
                                size=14,
                                weight=ft.FontWeight.W_400,
                                font_family="SFPro",
                                color="#666666",
                            ),
                        ],
                        spacing=0,
                    ),
                    padding=ft.padding.only(left=20, right=20, bottom=20),
                    height=0,
                    visible=False,
                ),
            ],
            spacing=0,
        ),
        border=ft.border.all(1, "#E0E0E0"),
        border_radius=30,
    )

    shipping_section = ft.Container(
        content=ft.Column(
            controls=[
                # header
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(
                                "Shipping & Delivery",
                                size=18,
                                weight=ft.FontWeight.W_700,
                                font_family="SFPro",
                                color="#000000",
                            ),
                            ft.Container(expand=True),
                            ft.Icon(
                                ref=shipping_icon,
                                name=ft.Icons.KEYBOARD_ARROW_DOWN,
                                size=24,
                                color="#000000",
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=ft.padding.all(20),
                    ink=True,
                    on_click=toggle_shipping,
                ),
                # content
                ft.Container(
                    ref=shipping_content,
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Shipping address (seller):",
                                size=14,
                                weight=ft.FontWeight.W_600,
                                font_family="SFPro",
                                color="#161616",
                            ),
                            ft.Text(
                                getattr(seller, "alamat", "") or "Not provided",
                                size=14,
                                weight=ft.FontWeight.W_400,
                                font_family="SFPro",
                                color="#666666",
                            ),
                            ft.Container(height=8),
                            ft.Text(
                                "Contact:",
                                size=14,
                                weight=ft.FontWeight.W_600,
                                font_family="SFPro",
                                color="#161616",
                            ),
                            ft.Text(
                                f"Phone: {getattr(seller, 'nomorTelepon', '') or '-'}",
                                size=14,
                                weight=ft.FontWeight.W_400,
                                font_family="SFPro",
                                color="#666666",
                                selectable=True,
                            ),
                            ft.Text(
                                f"Email: {getattr(seller, 'email', '') or '-'}",
                                size=14,
                                weight=ft.FontWeight.W_400,
                                font_family="SFPro",
                                color="#666666",
                                selectable=True,
                            ),
                        ],
                        spacing=4,
                    ),
                    padding=ft.padding.only(left=20, right=20, bottom=20),
                    height=0,
                    visible=False,
                ),
            ],
            spacing=0,
        ),
        border=ft.border.all(1, "#E0E0E0"),
        border_radius=30,
    )

    def get_recommendations():
        try:
            all_products = BarangManager.get_all_products() or []

            filtered = [
                p
                for p in all_products
                if getattr(p, "idBarang", None) != product_id
                and not bool(getattr(p, "isSold", False))
            ]

            sorted_products = sorted(
                filtered, key=lambda x: getattr(x, "idBarang", 0), reverse=True
            )
            return sorted_products[:4]
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return []

    def create_recommendation_card(rec_product):
        return ft.Container(
            content=ft.Column(
                controls=[
                    # product image
                    ft.Container(
                        content=(
                            ft.Icon(
                                name=ft.Icons.IMAGE_OUTLINED,
                                size=60,
                                color="#CCCCCC",
                            )
                            if not getattr(rec_product, "foto", None)
                            else ft.Image(
                                src_base64=rec_product.foto,
                                fit=ft.ImageFit.COVER,
                            )
                        ),
                        width=250,
                        height=200,
                        bgcolor="#E8E8E8",
                        border_radius=15,
                        alignment=ft.alignment.center,
                        ink=True,
                        on_click=lambda e, p=rec_product: page.go(
                            f"/product/{p.idBarang}"
                        ),
                    ),
                    ft.Container(height=12),
                    # product name
                    ft.Container(
                        content=ft.Text(
                            getattr(rec_product, "namaBarang", "-"),
                            size=16,
                            weight=ft.FontWeight.W_600,
                            font_family="SFPro",
                            color="#000000",
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        ink=True,
                        on_click=lambda e, p=rec_product: page.go(
                            f"/product/{p.idBarang}"
                        ),
                    ),
                    ft.Container(height=4),
                    # price
                    ft.Text(
                        f"IDR{int(rec_product.harga or 0):,}".replace(",", "."),
                        size=18,
                        weight=ft.FontWeight.W_700,
                        font_family="SFPro",
                        color="#0088ff",
                    ),
                    ft.Container(height=12),
                    # buttons
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                content=ft.Text(
                                    "Checkout",
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
                                on_click=lambda e, p=rec_product: handle_checkout_click(
                                    e, p
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

    recommendations = get_recommendations()
    recommendations_section = ft.Column(
        controls=[
            ft.Text(
                "You might also like",
                size=32,
                weight=ft.FontWeight.W_700,
                font_family="SFPro",
                color="#000000",
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=30),
            ft.Row(
                controls=[create_recommendation_card(p) for p in recommendations],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    back_button = ft.Container(
        content=ft.Icon(
            name=ft.Icons.CHEVRON_LEFT,
            size=60,
            color="#161616",
        ),
        alignment=ft.alignment.center,
        ink=True,
        on_click=lambda e: page.go("/shop"),
    )

    footer = Footer_black()
    nav_bar = NavigationBar(
        on_nav=lambda route: page.go(route), active="/shop", page=page
    )

    product_detail_section = ft.Container(
        content=ft.Row(
            controls=[
                image_gallery,
                ft.Container(width=50),
                product_info,
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=0,
        ),
        width=1150,
    )

    info_sections = ft.Container(
        content=ft.Column(
            controls=[
                description_section,
                ft.Container(height=20),
                shipping_section,
            ],
            spacing=0,
        ),
        width=1150,
    )

    recommendations_container = ft.Container(
        content=recommendations_section,
        width=1400,
        padding=ft.padding.symmetric(vertical=60),
    )

    scrollable_content = ft.Column(
        controls=[
            ft.Container(height=30),
            product_detail_section,
            ft.Container(height=40),
            info_sections,
            ft.Container(height=20),
            recommendations_container,
            ft.Container(height=40),
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    main_content = ft.Stack(
        controls=[
            ft.Column(
                controls=[
                    ft.Container(
                        content=scrollable_content,
                        expand=True,
                    ),
                    footer,
                ],
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            ft.Container(
                content=back_button,
                left=40,
                top=40,
            ),
        ],
        expand=True,
    )

    return ft.View(
        route=f"/product/{product_id}",
        appbar=nav_bar,
        controls=[ft.SafeArea(content=main_content, expand=True)],
        bgcolor="#FFFFFF",
        padding=0,
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
