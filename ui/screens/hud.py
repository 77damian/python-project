"""HUD overlay builder for the tower defense game.

Displays live game information (HP, wave, gold) and provides a toggleable build panel
with a secondary tower selection window (5 buttons).
"""

from typing import Dict, Any

import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ui import Frame, Button, Label


def create_hud(ui_manager, game_state: Dict[str, Any]) -> Dict[str, Any]:
    """Build the HUD overlay and register it with *ui_manager*.

    Args:
        ui_manager: The active UIManager instance.
        game_state: Mutable dict holding live game data.

    Returns:
        The game_state dict.
    """

    # Root HUD frame spanning the full screen (free layout)
    hud_root = Frame(
        x=0,
        y=0,
        width=SCREEN_WIDTH,
        height=SCREEN_HEIGHT,
        layout="free",
        padding=0,
        gap=0,
        bg_color=None,
        border_color=None,
    )

    # =========================================================================
    # Top bar — spanning full width, free layout for precise section alignment
    # =========================================================================
    bar_height = 45
    top_bar = Frame(
        x=0,
        y=0,
        width=SCREEN_WIDTH,
        height=bar_height,
        layout="free",
        padding=0,
        gap=0,
        bg_color=(20, 20, 32),
        border_color=(45, 45, 70),
        border_width=1,
    )

    # 1. Left: HP indicator
    hp_label = Label(
        text=lambda: f"HP: {game_state['tower_hp']}/{game_state['tower_max_hp']}",
        font_size=26,
        color=(255, 90, 90),
    )
    top_bar.add(hp_label, x=30, y=12)

    # 2. Center: Wave indicator
    wave_frame = Frame(
        layout="horizontal",
        padding=0,
        gap=0,
    )
    wave_label = Label(
        text=lambda: f"WAVE {game_state['wave']}/{game_state['max_waves']}",
        font_size=28,
        color=(255, 230, 100),
    )
    wave_frame.add(wave_label)
    top_bar.add(wave_frame, x=(SCREEN_WIDTH // 2) - 75, y=10)

    # 3. Right: Gold indicator
    gold_label = Label(
        text=lambda: f"GOLD: {game_state['gold']}",
        font_size=26,
        color=(255, 215, 0),
    )
    top_bar.add(gold_label, x=SCREEN_WIDTH - 270, y=12)

    # 4. Far Right: Pause/Menu toggle button
    def toggle_pause():
        game_state["paused"] = not game_state.get("paused", False)
        if game_state["paused"]:
            pause_menu.show()
        else:
            pause_menu.hide()

    menu_btn = Button(
        text="Menu [Esc]",
        width=110,
        height=32,
        on_click=toggle_pause,
        bg_color=(45, 45, 75),
        hover_color=(70, 70, 115),
        press_color=(95, 95, 145),
        text_color=(255, 255, 255),
        font_size=16,
    )
    top_bar.add(menu_btn, x=SCREEN_WIDTH - 125, y=7)

    hud_root.add(top_bar, x=0, y=0)

    # =========================================================================
    # Pause menu popup — centered modal frame
    # =========================================================================
    pause_menu = Frame(
        width=340,
        height=None,
        layout="vertical",
        padding=28,
        gap=18,
        bg_color=(18, 18, 30),
        border_color=(80, 80, 130),
        border_width=2,
        anchor="center",
    )
    pause_menu.set_anchor_target(SCREEN_WIDTH, SCREEN_HEIGHT)

    pause_title = Label(
        text="GAME PAUSED",
        font_size=36,
        color=(255, 215, 60),
    )
    pause_menu.add(pause_title)

    def resume_game():
        game_state["paused"] = False
        pause_menu.hide()

    def go_to_main_menu():
        game_state["paused"] = False
        pause_menu.hide()
        ui_manager.set_screen("main_menu")

    resume_btn = Button(
        text="Resume",
        width=230,
        height=48,
        on_click=resume_game,
        bg_color=(50, 50, 80),
        hover_color=(75, 75, 120),
        press_color=(100, 100, 155),
        text_color=(255, 255, 255),
        font_size=22,
    )
    pause_menu.add(resume_btn)

    exit_to_menu_btn = Button(
        text="Main Menu",
        width=230,
        height=48,
        on_click=go_to_main_menu,
        bg_color=(110, 45, 45),
        hover_color=(145, 60, 60),
        press_color=(180, 80, 80),
        text_color=(255, 255, 255),
        font_size=22,
    )
    pause_menu.add(exit_to_menu_btn)

    pause_menu.hide()
    hud_root.add(pause_menu)
    hud_root.toggle_pause = toggle_pause

    # =========================================================================
    # Build panel — bottom center bar with "Wall" and "Tower" buttons
    # =========================================================================
    btn_w, btn_h = 95, 55
    padding = 12
    gap = 14
    panel_w = padding * 2 + 2 * btn_w + gap
    panel_h = btn_h + padding * 2

    build_panel = Frame(
        x=(SCREEN_WIDTH - panel_w) // 2,
        y=SCREEN_HEIGHT - panel_h - 20,
        width=panel_w,
        height=panel_h,
        layout="horizontal",
        padding=padding,
        gap=gap,
        bg_color=(22, 22, 36),
        border_color=(70, 70, 110),
        border_width=2,
    )

    btn_bg = (45, 45, 75)
    btn_hover = (70, 70, 115)
    btn_press = (95, 95, 145)

    # Wall button
    def select_wall():
        game_state["selected_building"] = 1
        tower_panel.hide()

    wall_btn = Button(
        text="Wall",
        width=btn_w,
        height=btn_h,
        on_click=select_wall,
        bg_color=btn_bg,
        hover_color=btn_hover,
        press_color=btn_press,
        text_color=(255, 255, 255),
        font_size=18,
    )
    build_panel.add(wall_btn)

    # Tower button (toggles the tower selection panel)
    def toggle_tower_panel():
        tower_panel.toggle()

    tower_btn = Button(
        text="Tower",
        width=btn_w,
        height=btn_h,
        on_click=toggle_tower_panel,
        bg_color=(55, 45, 80),
        hover_color=(80, 65, 115),
        press_color=(105, 85, 145),
        text_color=(255, 255, 255),
        font_size=18,
    )
    build_panel.add(tower_btn)

    build_panel.hide()
    hud_root.add(build_panel, x=build_panel.x, y=build_panel.y)

    # =========================================================================
    # Tower Selection Window — 5 buttons
    # =========================================================================
    t_btn_w, t_btn_h = 95, 55
    t_padding = 12
    t_gap = 10
    num_towers = 5
    t_panel_w = t_padding * 2 + num_towers * t_btn_w + (num_towers - 1) * t_gap
    t_panel_h = t_btn_h + t_padding * 2

    tower_panel = Frame(
        x=(SCREEN_WIDTH - t_panel_w) // 2,
        y=build_panel.y - t_panel_h - 10,
        width=t_panel_w,
        height=t_panel_h,
        layout="horizontal",
        padding=t_padding,
        gap=t_gap,
        bg_color=(22, 22, 36),
        border_color=(80, 80, 130),
        border_width=2,
    )

    for i in range(1, num_towers + 1):
        tower_idx = i

        def _make_tower_click(idx=tower_idx):
            def handler():
                game_state["selected_building"] = 2
                tower_panel.hide()
            return handler

        t_button = Button(
            text=f"Tower {i}",
            width=t_btn_w,
            height=t_btn_h,
            on_click=_make_tower_click(),
            bg_color=btn_bg,
            hover_color=btn_hover,
            press_color=btn_press,
            text_color=(255, 255, 255),
            font_size=18,
        )
        tower_panel.add(t_button)

    tower_panel.hide()
    hud_root.add(tower_panel, x=tower_panel.x, y=tower_panel.y)

    # =========================================================================
    # Toggle button — bottom right
    # =========================================================================
    def toggle_build():
        build_panel.toggle()
        if not build_panel.visible:
            tower_panel.hide()

    toggle_btn = Button(
        text="Build [B]",
        width=110,
        height=45,
        on_click=toggle_build,
        bg_color=(50, 45, 75),
        hover_color=(80, 70, 115),
        press_color=(110, 95, 145),
        text_color=(255, 255, 255),
        font_size=18,
    )
    hud_root.add(toggle_btn, x=SCREEN_WIDTH - 130, y=SCREEN_HEIGHT - 65)

    hud_root.toggle_build_panel = toggle_build

    # Register overlay
    ui_manager.add_overlay("hud", hud_root)

    return game_state
