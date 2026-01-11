import os
import sys
from pathlib import Path
import flet as ft

# fix untuk import diluar pages
current_path = Path(__file__).resolve()
search_paths = [current_path.parent] + list(current_path.parents)
for candidate in search_paths:
    direct_db = candidate / "database"
    src_db = candidate / "src" / "database"
    target_path = None
    if direct_db.exists():
        target_path = candidate
    elif src_db.exists():
        target_path = candidate / "src"

    if target_path:
        target_str = str(target_path)
        if target_str not in sys.path:
            sys.path.insert(0, target_str)
        break

from database.connection import create_db_and_tables

from .pages.home import HomePage
from .pages.donate_funds import DonateFundsPage
from .pages.donate_goods import DonateGoodsPage
from .pages.shop import ShopPage
from .pages.product_detail import ProductDetailPage
from .pages.product_tradein import ProductTradeInPage
from .pages.sell import SellPage
from .pages.checkout import CheckoutPage
from .pages.login import LoginPage
from .pages.register import RegisterPage
from .pages.profile import ProfilePage
from .pages.donation import DonationPage
from .pages.donation_request import DonationRequestPage
from .pages.donation_recipient_detail import DonationRecipientDetailPage

icon_path = os.path.join(os.path.dirname(__file__), "assets", "ui", "app_icon.png")


def main(page: ft.Page):

    # PAGE CONFIGURATION
    page.title = "YAREU - Your Action to Reuse & Unite"
    page.bgcolor = "#161616"
    page.padding = 0
    page.spacing = 0
    page.scroll = ft.ScrollMode.AUTO

    page.window.width = 1440
    page.window.height = 900
    page.window.min_width = 1440
    page.window.min_height = 900
    page.window.resizable = True

    # page.window.icon = APP_ICON_PATH
    print("DEBUG ICON PATH:", icon_path)
    print("FILE EXISTS:", os.path.exists(icon_path))
    page.window.icon = icon_path

    page.window.center()

    # Between page transition + font-family
    FONT_SFPRO_PATH = "assets/fonts/SF-Pro-Display-Regular.otf"
    page.fonts = {"SFPro": FONT_SFPRO_PATH}
    page.theme = ft.Theme(
        font_family="SFPro",
        page_transitions=ft.PageTransitionsTheme(
            android=ft.PageTransitionTheme.OPEN_UPWARDS,
            ios=ft.PageTransitionTheme.CUPERTINO,
            macos=ft.PageTransitionTheme.FADE_UPWARDS,
            linux=ft.PageTransitionTheme.ZOOM,
            windows=ft.PageTransitionTheme.NONE,
        ),
    )

    # Init DB and session
    create_db_and_tables()
    session = ["idPengguna", "idPembeli", "idPenjual", "idDonatur"]
    for i in session:
        if page.client_storage.get(i) is None:
            page.client_storage.set(i, "")

    # ROUTING
    def route_change(e):
        def parse_query(route: str):
            qs = ""
            if "?" in route:
                qs = route.split("?")[1]
            elif getattr(page, "query", None):
                qs = page.query.lstrip("?")
            if not qs:
                return {}
            return {
                param.split("=")[0]: param.split("=")[1]
                for param in qs.split("&")
                if "=" in param
            }

        try:
            page.views.clear()

            # I-01 - Home
            if page.route == "/":
                page.views.append(HomePage(page))

            # I-02 - Shop
            elif page.route == "/shop":
                page.views.append(ShopPage(page))

            # I-02A - Product Detail
            elif page.route.startswith("/product/"):
                try:
                    product_id = int(page.route.split("/")[-1].split("?")[0])
                    from_page = 1
                    from_category = "All"

                    if "?" in page.route:
                        query_string = page.route.split("?")[1]
                        params = dict(
                            param.split("=")
                            for param in query_string.split("&")
                            if "=" in param
                        )
                        from_page = int(params.get("from_page", 1))
                        from_category = params.get("from_category", "All")

                    page.views.append(
                        ProductDetailPage(page, product_id, from_page, from_category)
                    )
                except (ValueError, IndexError) as e:
                    print(f"Invalid product ID: {e}")
                    page.go("/shop")
            elif page.route.startswith("/product_tradein"):
                product_id = None
                try:
                    if "?" in page.route:
                        params = dict(
                            param.split("=")
                            for param in page.route.split("?")[1].split("&")
                            if "=" in param
                        )
                        product_id = int(params.get("product_id", 0))
                    elif "/" in page.route[16:]:
                        product_id = int(page.route.split("/")[-1])
                except (ValueError, IndexError) as e:
                    print(f"Invalid product ID for trade in: {e}")
                    product_id = None
                page.views.append(ProductTradeInPage(page, product_id))

            # I-02B - Sell
            elif page.route == "/sell":
                page.views.append(SellPage(page))

            # I-02C - Checkout
            elif page.route.startswith("/checkout"):
                product_id = None
                try:
                    if "?" in page.route:
                        params = dict(
                            param.split("=")
                            for param in page.route.split("?")[1].split("&")
                            if "=" in param
                        )
                        if "product_id" in params:
                            product_id = int(params.get("product_id", 0))
                    elif "/" in page.route[10:]:  # /checkout/xxx
                        product_id = int(page.route.split("/")[-1])
                except (ValueError, IndexError) as e:
                    print(f"Invalid product ID: {e}")
                    product_id = None

                page.views.append(CheckoutPage(page, product_id=product_id))

            # I-03 - Donation
            elif page.route == "/donation":
                page.views.append(DonationPage(page))

            elif page.route == "/donation/funds" or page.route.startswith(
                "/donation/funds"
            ):
                penerima_id = None
                try:
                    params = parse_query(page.route)
                    if params:
                        penerima_id = int(params.get("idPenerima", 0))
                except (ValueError, IndexError):
                    penerima_id = None
                page.views.append(DonateFundsPage(page, penerima_id))

            elif page.route == "/donation/goods" or page.route.startswith(
                "/donation/goods"
            ):
                penerima_id = None
                try:
                    params = parse_query(page.route)
                    if params:
                        penerima_id = int(params.get("idPenerima", 0))
                except (ValueError, IndexError):
                    penerima_id = None
                page.views.append(DonateGoodsPage(page, penerima_id))

            elif page.route == "/donation_request":
                page.views.append(DonationRequestPage(page))

            elif page.route.startswith("/donation_recipient_detail"):
                penerima_id = None
                try:
                    params = parse_query(page.route)
                    if params and "idPenerima" in params:
                        penerima_id = int(params.get("idPenerima", 0))
                    else:
                        parts = [p for p in page.route.split("/") if p]
                        if len(parts) >= 2 and parts[-2] == "donation_recipient_detail":
                            penerima_id = int(parts[-1])
                except (ValueError, IndexError) as e:
                    print(f"Invalid penerima ID: {e}")
                    penerima_id = None

                page.views.append(DonationRecipientDetailPage(page, penerima_id))

            elif page.route == "/profile/general-info":
                page.views.append(ProfilePage(page, active_tab="general-info"))

            elif page.route == "/profile/orders-activity":
                page.views.append(ProfilePage(page, active_tab="orders-activity"))

            elif page.route == "/profile/security":
                page.views.append(ProfilePage(page, active_tab="security"))

            elif page.route == "/login":
                page.views.append(LoginPage(page))

            elif page.route == "/register":
                page.views.append(RegisterPage(page))

            else:
                # 404 - Route not found
                page.views.append(
                    ft.View(
                        route="/404",
                        controls=[
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            "404",
                                            size=72,
                                            weight=ft.FontWeight.W_700,
                                            color="#0088ff",
                                        ),
                                        ft.Text(
                                            "Page Not Found",
                                            size=24,
                                            color="#B3B3B3",
                                        ),
                                        ft.Container(height=20),
                                        ft.ElevatedButton(
                                            "Go Home",
                                            bgcolor="#0088ff",
                                            color="#FFFFFF",
                                            on_click=lambda e: page.go("/"),
                                        ),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=10,
                                ),
                                alignment=ft.alignment.center,
                                expand=True,
                            )
                        ],
                        bgcolor="#161616",
                    )
                )

            page.update()

        except Exception as e:
            print(f"Error in route_change: {e}")
            import traceback

            traceback.print_exc()

            # show error page
            page.views.clear()
            page.views.append(
                ft.View(
                    route="/error",
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "Error Loading Page",
                                        size=32,
                                        color="#FF0000",
                                    ),
                                    ft.Text(
                                        str(e),
                                        size=14,
                                        color="#B3B3B3",
                                    ),
                                    ft.Container(height=20),
                                    ft.ElevatedButton(
                                        "Go Home",
                                        bgcolor="#0088ff",
                                        color="#FFFFFF",
                                        on_click=lambda e: page.go("/"),
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10,
                            ),
                            alignment=ft.alignment.center,
                            expand=True,
                        )
                    ],
                    bgcolor="#161616",
                )
            )
            page.update()

    def view_pop(e):
        if len(page.views) <= 1:
            page.go("/")
            return

        page.views.pop()
        page.go(page.views[-1].route)

    # EVENT HANDLERS
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # INITIAL ROUTE
    try:
        page.go("/")  # nav ke home page
    except Exception as e:
        print(f"Error in initial navigation: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    ft.app(target=main)
