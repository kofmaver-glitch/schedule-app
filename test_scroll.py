"""
Тест скролла в Flet 1.0.
"""

import flet as ft


def main(page: ft.Page):
    page.title = "Тест скролла"
    page.window.width = 400
    page.window.height = 400

    cards = []
    for i in range(30):
        cards.append(
            ft.Container(
                content=ft.Text(f"Карточка #{i + 1}", size=18),
                padding=15,
                bgcolor=ft.Colors.GREY_200,
                border_radius=10,
            )
        )

    page.add(
        ft.Column(
            controls=cards,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.run(main)