"""
TOOLBOX — Багшаас бэлэн өгсөн туслах хэрэгслүүд.

Эдгээр функцийг та зүгээр л ДУУДАЖ хэрэглэнэ. Дотор нь яаж ажилладгийг
одоохондоо мэдэх шаардлагагүй — яг л print() гэдгийг хэрэглэдэг шиг.

Хэрэглэх жишээ:
    from toolbox import color, clear, slow, box, line, pause, ask

    clear()
    box(["Сайн уу!"])
    slow(color("Аажуухан гарч ирэх текст", "green"))
    name = ask("Нэрээ бичнэ үү: ")
"""

import time
import os

# Хэрэв терминал муухай тэмдэгт харуулбал доорхыг False болго.
USE_COLOR = True
SLOW_TEXT = True
os.system("")   # Windows 10+ дээр ANSI өнгийг асаадаг жижиг заль


COLORS = {
    "red": "31", "green": "32", "yellow": "33", "blue": "34",
    "magenta": "35", "cyan": "36", "white": "37", "grey": "90",
}


def color(text, c, bold=False):
    """Тэмдэгт мөрийг өнгөтэй болгож буцаана."""
    if not USE_COLOR:
        return text
    code = COLORS.get(c, "37")
    start = "1;" if bold else ""
    return f"\033[{start}{code}m{text}\033[0m"


def clear():
    """Дэлгэцийг цэвэрлэнэ."""
    if USE_COLOR:
        print("\033[2J\033[H", end="")


def slow(text="", c=None, bold=False, delay=0.012):
    """Текстийг бичгийн машин шиг аажуухан хэвлэнэ."""
    if c is not None:
        text = color(text, c, bold)
    if not SLOW_TEXT:
        print(text)
        return
    for ch in text:
        print(ch, end="", flush=True)
        if ch not in "\033[0123456789;m":   # өнгөний нууц кодыг алгасна
            time.sleep(delay)
    print()


def pause(msg="( Үргэлжлүүлэхийн тулд Enter дар )"):
    """Тоглогч Enter дартал хүлээнэ."""
    input("\n" + color(msg, "grey"))


def ask(prompt):
    """Тоглогчоос мөр асууж, цэвэрлэж, жижиг үсгээр буцаана."""
    return input(color(prompt, "yellow", bold=True)).strip().lower()


def line():
    """Заагч зураас хэвлэнэ."""
    print(color("─" * 64, "grey"))


# --- Доорх хоёр функц нь зөвхөн box()-д хэрэгтэй дотоод туслахууд ---

def _visible_len(s):
    """Өнгөний нууц кодыг тооцохгүйгээр харагдах урт."""
    count = 0
    i = 0
    while i < len(s):
        if s[i] == "\033":
            while i < len(s) and s[i] != "m":
                i += 1
            i += 1
        else:
            count += 1
            i += 1
    return count


def _pad(s, width, center):
    """Тэмдэгт мөрийг width хүртэл хоосон зайгаар дүүргэнэ."""
    extra = width - _visible_len(s)
    if extra < 0:
        extra = 0
    if center:
        left = extra // 2
        return " " * left + s + " " * (extra - left)
    return s + " " * extra


def box(lines, c="cyan", center=False, width=64):
    """Текстийн мөрүүдийг гоё хүрээгээр хүрээлж хэвлэнэ.
    lines — тэмдэгт мөрүүдийн жагсаалт."""
    inner = width - 4
    print(color("╔" + "═" * (width - 2) + "╗", c))
    for ln in lines:
        print(color("║", c) + " " + _pad(ln, inner, center) + " " + color("║", c))
    print(color("╚" + "═" * (width - 2) + "╝", c))
