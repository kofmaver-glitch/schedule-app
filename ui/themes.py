"""
Определения тем оформления для приложения.
"""

import flet as ft


# ============================================================
# ПАСТЕЛЬНЫЕ ТЕМЫ
# ============================================================

# ☕ Кофе с молоком — фон кофейный, карточки белые
COFFEE_THEME = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary="#C8A98B",
        on_primary="#1A1A1A",
        secondary="#E8D5C0",
        surface="#2E2218",
        on_surface="#F5E8D8",
    ),
)

# 🌿 Мятная — тёмный фон, светлые карточки
MINT_THEME = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary="#A8D5BA",
        on_primary="#1A1A1A",
        secondary="#C8E6D0",
        surface="#1E2E24",
        on_surface="#E0F0E8",
    ),
)

# 🌸 Нежно-розовая — светлый фон, насыщенные розовые карточки
PINK_THEME = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary="#F4B6C2",
        on_primary="#1A1A1A",
        secondary="#F8D0D8",
        surface="#FFF0F3",
        on_surface="#3A2028",
    ),
)

# ☁️ Небесно-голубая — светлый фон, белые карточки
SKY_THEME = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary="#A8D0E6",
        on_primary="#1A1A1A",
        secondary="#C8E0F0",
        surface="#F0F6FA",
        on_surface="#1A2A3A",
    ),
)

# 🦊 Рыжеватая — тёмный фон, рыжие карточки
FOX_THEME = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary="#E8A87C",
        on_primary="#1A1A1A",
        secondary="#F0C8A0",
        surface="#2A1F18",
        on_surface="#F8E8D8",
    ),
)


# ============================================================
# СЛОВАРЬ ВСЕХ ТЕМ
# ============================================================

THEMES = {
    "system": {
        "name": "Системная",
        "icon": "🖥",
        "mode": ft.ThemeMode.SYSTEM,
        "theme": None,
        "card_color": None,
        "card_text_color": None,
    },
    "dark": {
        "name": "Тёмная",
        "icon": "🌙",
        "mode": ft.ThemeMode.DARK,
        "theme": None,
        "card_color": None,
        "card_text_color": None,
    },
    "light": {
        "name": "Светлая",
        "icon": "☀️",
        "mode": ft.ThemeMode.LIGHT,
        "theme": None,
        "card_color": None,
        "card_text_color": None,
    },
    "coffee": {
        "name": "Кофе с молоком",
        "icon": "☕",
        "mode": ft.ThemeMode.DARK,
        "theme": COFFEE_THEME,
        "card_color": "#F0E6D8",            # кремовые (почти белые)
        "card_text_color": "#3A2E24",       # тёмно-коричневый текст
    },
    "mint": {
        "name": "Мятная",
        "icon": "🌿",
        "mode": ft.ThemeMode.DARK,
        "theme": MINT_THEME,
        "card_color": "#C8E6D0",            # светло-мятный
        "card_text_color": "#1A2E24",       # тёмно-зелёный текст
    },
    "pink": {
        "name": "Нежно-розовая",
        "icon": "🌸",
        "mode": ft.ThemeMode.LIGHT,
        "theme": PINK_THEME,
        "card_color": "#F4B6C2",            # насыщенный розовый
        "card_text_color": "#3A1A24",       # тёмно-бордовый текст
    },
    "sky": {
        "name": "Небесно-голубая",
        "icon": "☁️",
        "mode": ft.ThemeMode.LIGHT,
        "theme": SKY_THEME,
        "card_color": "#FFFFFF",            # белые
        "card_text_color": "#1A2A3A",       # тёмно-синий текст
    },
    "fox": {
        "name": "Рыжеватая",
        "icon": "🦊",
        "mode": ft.ThemeMode.DARK,
        "theme": FOX_THEME,
        "card_color": "#E8A87C",            # рыжий
        "card_text_color": "#2A1A0E",       # тёмно-коричневый текст
    },
}


DEFAULT_THEME = "dark"


def apply_theme(page: ft.Page, theme_key: str):
    """Применяет тему к странице."""
    if theme_key not in THEMES:
        theme_key = DEFAULT_THEME
    
    theme_data = THEMES[theme_key]
    
    page.theme_mode = theme_data["mode"]
    page.theme = theme_data["theme"]
    
    page.update()