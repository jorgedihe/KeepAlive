import ctypes
import threading
import time
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

# WinAPI flags
ES_CONTINUOUS       = 0x80000000
ES_SYSTEM_REQUIRED  = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

is_awake = True
icon = None

def set_awake(enable):
    global is_awake
    if enable:
        ctypes.windll.kernel32.SetThreadExecutionState(
            ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
        )
    else:
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)

    is_awake = enable
    update_icon()

def toggle_awake(icon=None, item=None):
    set_awake(not is_awake)

def quit_app(icon=None, item=None):
    set_awake(False)
    icon.stop()

def update_icon():
    icon.icon = draw_icon("green" if is_awake else "red")
    icon.title = f"KA: {'ON' if is_awake else 'OFF'}"
    icon.menu = build_menu()

def draw_icon(color):
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if color == "green":
        fill = (50, 205, 50)
        outline = (34, 139, 34)
    else:
        fill = (255, 99, 71)
        outline = (178, 34, 34)

    draw.ellipse((8, 8, 56, 56), fill=fill, outline=outline, width=4)
    return img

def build_menu():
    return Menu(
        MenuItem(
            "Desactivar KA" if is_awake else "Activar KA",
            toggle_awake
        ),
        MenuItem("Salir", quit_app)
    )

def keep_teams_active():
    while True:
        if is_awake:
            # Simula una pulsación de tecla SHIFT para evitar el estado "ausente"
            ctypes.windll.user32.keybd_event(0x10, 0, 0, 0)  # SHIFT down
            ctypes.windll.user32.keybd_event(0x10, 0, 2, 0)  # SHIFT up
        time.sleep(60)  # repetir cada 60 segundos

def main():
    global icon
    icon = Icon(
        "KA",
        draw_icon("green"),
        "KA: ON",
        menu=build_menu()
    )
    set_awake(True)  # Estado por defecto: ON

    # Inicia el hilo para mantener Teams activo
    threading.Thread(target=keep_teams_active, daemon=True).start()

    icon.run()

if __name__ == "__main__":
    main()
