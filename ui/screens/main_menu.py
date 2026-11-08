"""Main-menu screen builder for the tower defense game."""

import pygame
import sys

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ui import Frame, Button, Label


def create_main_menu(ui_manager) -> None:
    """Build the main-menu screen and register it with *ui_manager*.

    The menu contains a centred title ("TOWER DEFENSE") and three vertically
    stacked buttons: PLAY, LEVELS, and EXIT.

    Args:
        ui_manager: The active :class:`UIManager` instance.
    """

    # --- Root frame (vertical, centred on screen) -------------------------
    root = Frame(
        width=440,
        height=None,  # auto-fit height
        layout="vertical",
        padding=30,
        gap=20,
        bg_color=(18, 18, 30),
        border_color=(70, 70, 110),
        border_width=2,
        anchor="center",
    )
    root.set_anchor_target(SCREEN_WIDTH, SCREEN_HEIGHT)

    # --- Title label ------------------------------------------------------
    title_label = Label(
        text="TOWER DEFENSE",
        font_size=52,
        color=(255, 215, 60),
    )
    root.add(title_label)

    # --- Button colours ---------------------------------------------------
    btn_bg = (50, 50, 80)
    btn_hover = (70, 70, 110)
    btn_press = (90, 90, 140)
    btn_text = (255, 255, 255)

    # --- PLAY button ------------------------------------------------------
    play_btn = Button(
        text="PLAY",
        width=250,
        height=50,
        on_click=lambda: ui_manager.set_screen("game"),
        bg_color=btn_bg,
        hover_color=btn_hover,
        press_color=btn_press,
        text_color=btn_text,
        font_size=24,
    )
    root.add(play_btn)

    # --- LEVELS button ----------------------------------------------------
    levels_btn = Button(
        text="LEVELS",
        width=250,
        height=50,
        on_click=lambda: ui_manager.set_screen("levels"),
        bg_color=btn_bg,
        hover_color=btn_hover,
        press_color=btn_press,
        text_color=btn_text,
        font_size=24,
    )
    root.add(levels_btn)

    # --- EXIT button ------------------------------------------------------
    def _exit_game() -> None:
        pygame.quit()
        sys.exit()

    exit_btn = Button(
        text="EXIT",
        width=250,
        height=50,
        on_click=_exit_game,
        bg_color=(120, 40, 40),
        hover_color=(160, 60, 60),
        press_color=(200, 80, 80),
        text_color=btn_text,
        font_size=24,
    )
    root.add(exit_btn)

    # --- Register with UIManager ------------------------------------------
    ui_manager.add_screen("main_menu", root)
