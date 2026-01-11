import flet as ft

from views.main import main as views_main


def main(page: ft.Page):
    views_main(page)


if __name__ == "__main__":
    ft.app(target=main)
