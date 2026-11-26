"""Level end screen (victory / game over) with Restart and Main Menu buttons."""

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ui import Frame, Button, Label


def create_level_end(ui_manager, game_state):
    """Build the level end screen and register it with *ui_manager*."""
    panel_w, panel_h = 340, 230
    root = Frame(
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

    panel = Frame(
        x=(SCREEN_WIDTH - panel_w) // 2,
        y=(SCREEN_HEIGHT - panel_h) // 2,
        width=panel_w,
        height=panel_h,
        layout="vertical",
        padding=24,
        gap=18,
        bg_color=(24, 24, 38),
        border_color=(90, 90, 140),
        border_width=2,
    )

    title = Label(
        text=lambda: "LEVEL COMPLETE" if game_state.get("level_won") else "GAME OVER",
        font_size=36,
        color=(255, 220, 100),
    )
    panel.add(title)

    def on_restart():
        game_state["restart_requested"] = True
        ui_manager.set_screen("game")

    def on_menu():
        game_state["restart_requested"] = True
        ui_manager.set_screen("main_menu")

    restart_btn = Button(
        text="Restart Level",
        width=panel_w - 48,
        height=46,
        on_click=on_restart,
        bg_color=(50, 80, 55),
        hover_color=(70, 115, 78),
        press_color=(90, 145, 100),
        text_color=(255, 255, 255),
        font_size=22,
    )
    panel.add(restart_btn)

    menu_btn = Button(
        text="Main Menu",
        width=panel_w - 48,
        height=46,
        on_click=on_menu,
        bg_color=(60, 45, 75),
        hover_color=(90, 68, 115),
        press_color=(120, 90, 150),
        text_color=(255, 255, 255),
        font_size=22,
    )
    panel.add(menu_btn)

    root.add(panel, x=panel.x, y=panel.y)
    ui_manager.add_screen("level_end", root)
