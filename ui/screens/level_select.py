"""Level-select screen builder for the tower defense game."""

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ui import Frame, Button, Label


def create_level_select(ui_manager) -> None:
    """Build the level-select screen and register it with *ui_manager*.

    Displays a title, a horizontal row of five level buttons, and a back
    button that returns to the main menu.

    Args:
        ui_manager: The active :class:`UIManager` instance.
    """

    # --- Root frame (vertical, centred) -----------------------------------
    root = Frame(
        width=680,
        height=None,  # auto-fit height
        layout="vertical",
        padding=30,
        gap=24,
        bg_color=(18, 18, 30),
        border_color=(70, 70, 110),
        border_width=2,
        anchor="center",
    )
    root.set_anchor_target(SCREEN_WIDTH, SCREEN_HEIGHT)

    # --- Title label ------------------------------------------------------
    title_label = Label(
        text="SELECT LEVEL",
        font_size=42,
        color=(255, 215, 60),
    )
    root.add(title_label)

    # --- Horizontal row of level buttons ----------------------------------
    level_row = Frame(
        layout="horizontal",
        padding=12,
        gap=16,
        bg_color=(25, 25, 40),
        border_color=(60, 60, 90),
    )

    btn_bg = (50, 50, 80)
    btn_hover = (70, 70, 110)
    btn_press = (90, 90, 140)
    btn_text = (255, 255, 255)

    for level_num in range(1, 6):
        level_btn = Button(
            text=f"Level {level_num}",
            width=100,
            height=80,
            on_click=lambda _n=level_num: ui_manager.set_screen("game"),
            bg_color=btn_bg,
            hover_color=btn_hover,
            press_color=btn_press,
            text_color=btn_text,
            font_size=20,
        )
        level_row.add(level_btn)

    root.add(level_row)

    # --- Back button ------------------------------------------------------
    back_btn = Button(
        text="< Back",
        width=160,
        height=45,
        on_click=lambda: ui_manager.set_screen("main_menu"),
        bg_color=(80, 60, 60),
        hover_color=(110, 80, 80),
        press_color=(140, 100, 100),
        text_color=btn_text,
        font_size=22,
    )
    root.add(back_btn)

    # --- Register with UIManager ------------------------------------------
    ui_manager.add_screen("levels", root)
