"""
ПАКМАН (PAC-MAN)
Терминал дээр тоглодог сонгодог тоглоомын энгийн хувилбар -- Kami-2 жишээ.

ЗӨВХӨН Kami-2 хичээлд заасан ойлголтуудыг ашиглав:
  хувьсагч, тэмдэгт мөр, f-string, if/elif/else, логик утга,
  while/for давталт, жагсаалт (list), толь бичиг (dict), функц,
  random / time / os / sys модуль. Класс / OOP огт ашиглаагүй.

ХЭРХЭН ТОГЛОХ ВЭ:
  W A S D эсвэл сумны товчоор Пакманыг (ᗧ) хөдөлгө.
  Бүх цэгийг (·) идвэл ялна. Хийсвэр сүнснүүд (ᗣ) чамайг барьвал
  нэг амь хорогдоно. Гурван амиа бүрэн алдвал тоглоом дуусна.
  Гарахдаа Q дар.

ТЭМДЭГЛЭЛ: энэ нь Линукс/Мак терминал дээр ажиллана (termios ашигладаг).
"""

import os
import sys
import time
import random
import select
import termios
import tty

# ----------------------------------------------------------------------
# ТОХИРГОО
# ----------------------------------------------------------------------

USE_COLOR = True
TICK = 0.12          # нэг алхам хоорондын хугацаа (секунд) -- жижиг = хурдан
GHOST_EVERY = 2      # сүнснүүд хэдэн алхам тутамд нэг хөдлөх вэ
START_LIVES = 3

# Талбайн зураг. # = хана, . = цэг, ' ' = хоосон зам,
# P = Пакманы эхлэл, G = сүнсний эхлэл.
LEVEL = [
    "####################",
    "#P...#........#....#",
    "#.##.#.######.#.##.#",
    "#.#..............#.#",
    "#.#.##.######.##.#.#",
    "#......#.G..#......#",
    "####.#.#.##.#.#.####",
    "   #.#......G.#.#   ",
    "####.#.##..##.#.####",
    "#......#.GG.#......#",
    "#.####.######.####.#",
    "#..................#",
    "#.##.##.#..#.##.##.#",
    "#....#...##...#....#",
    "####################",
]

# ----------------------------------------------------------------------
# ӨНГӨ + ДЭЛГЭЦ
# ----------------------------------------------------------------------

COLORS = {
    "red": "31", "green": "32", "yellow": "33", "blue": "34",
    "magenta": "35", "cyan": "36", "white": "37", "grey": "90",
}


def color(text, c, bold=False):
    if not USE_COLOR:
        return text
    code = COLORS.get(c, "37")
    start = "1;" if bold else ""
    return f"\033[{start}{code}m{text}\033[0m"


def clear():
    print("\033[2J\033[H", end="")


def home():
    """Курсорыг зүүн дээд буланд аваачна (дэлгэцийг бүхэлд нь цэвэрлэхгүй
    -- ингэснээр анивчихгүй жигд шинэчлэгдэнэ)."""
    print("\033[H", end="")


def hide_cursor():
    print("\033[?25l", end="")


def show_cursor():
    print("\033[?25h", end="")


# ----------------------------------------------------------------------
# ТОВЧ УНШИХ (блоклохгүй) -- termios ашиглана
# ----------------------------------------------------------------------

def read_key():
    """Дарагдсан товчийг буцаана, юу ч дараагүй бол '' буцаана (хүлээхгүй).
    Сумны товчийг 'W/A/S/D' болгож хувиргана."""
    dr, _, _ = select.select([sys.stdin], [], [], 0)
    if not dr:
        return ""
    ch = sys.stdin.read(1)
    if ch == "\033":                 # сумны товч нь 3 тэмдэгтээр ирдэг
        seq = sys.stdin.read(2) if select.select([sys.stdin], [], [], 0)[0] else ""
        arrows = {"[A": "w", "[B": "s", "[C": "d", "[D": "a"}
        return arrows.get(seq, "")
    return ch.lower()


# ----------------------------------------------------------------------
# ТАЛБАЙ БЭЛДЭХ
# ----------------------------------------------------------------------

def build_world():
    """LEVEL зургаас тоглоомын төлвийг (dict) үүсгэж буцаана."""
    walls = []        # ханын (мөр, багана) хосуудын жагсаалт
    dots = []         # үлдсэн цэгүүдийн (мөр, багана) жагсаалт
    ghosts = []       # сүнс бүр {"r":.., "c":.., "dr":.., "dc":..} dict
    pac = {"r": 0, "c": 0, "dr": 0, "dc": 0}

    for r in range(len(LEVEL)):
        row = LEVEL[r]
        for c in range(len(row)):
            ch = row[c]
            if ch == "#":
                walls.append((r, c))
            elif ch == ".":
                dots.append((r, c))
            elif ch == "P":
                pac["r"] = r
                pac["c"] = c
            elif ch == "G":
                ghosts.append({"r": r, "c": c, "dr": 0, "dc": 0})

    return {
        "walls": walls,
        "dots": dots,
        "ghosts": ghosts,
        "pac": pac,
        "score": 0,
        "lives": START_LIVES,
        "pac_start": (pac["r"], pac["c"]),
        "ghost_start": [(g["r"], g["c"]) for g in ghosts],
        "tick": 0,
    }


def is_wall(world, r, c):
    return (r, c) in world["walls"]


# ----------------------------------------------------------------------
# ХӨДӨЛГӨӨН
# ----------------------------------------------------------------------

def move_pac(world):
    """Пакманыг одоогийн чиглэлийн дагуу нэг алхам хөдөлгөнө."""
    pac = world["pac"]
    nr = pac["r"] + pac["dr"]
    nc = pac["c"] + pac["dc"]
    cols = len(LEVEL[0])
    # Хажуу талаар гарвал нөгөө талаас гарч ирэх (туннель).
    nc = nc % cols
    if not is_wall(world, nr, nc):
        pac["r"] = nr
        pac["c"] = nc
        # Цэг идэх.
        if (nr, nc) in world["dots"]:
            world["dots"].remove((nr, nc))
            world["score"] += 10


def move_ghosts(world):
    """Сүнс бүрийг хөдөлгөнө. Энгийн дүрэм: одоогийн чиглэлээ үргэлжлүүлэх,
    хана таарвал санамсаргүй чөлөөтэй чиглэл сонгох."""
    for g in world["ghosts"]:
        choices = []
        # Боломжтой бүх чиглэлийг цуглуулна (буцаж эргэхээс зайлсхийнэ).
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr = g["r"] + dr
            nc = (g["c"] + dc) % len(LEVEL[0])
            if not is_wall(world, nr, nc):
                # Шууд эргэж буцахаас аль болох зайлсхийнэ.
                if (dr, dc) != (-g["dr"], -g["dc"]):
                    choices.append((dr, dc))
        # Хэрэв тэр чигтээ үргэлжлэх боломжтой бол ихэвчлэн тэгнэ.
        forward = (g["dr"], g["dc"])
        if forward in choices and random.random() < 0.7:
            dr, dc = forward
        elif choices:
            dr, dc = random.choice(choices)
        else:
            dr, dc = -g["dr"], -g["dc"]    # цорын ганц гарц нь буцах бол

        g["dr"] = dr
        g["dc"] = dc
        g["r"] = g["r"] + dr
        g["c"] = (g["c"] + dc) % len(LEVEL[0])


def caught(world):
    """Пакман сүнстэй мөргөлдсөн бол True буцаана."""
    pac = world["pac"]
    for g in world["ghosts"]:
        if g["r"] == pac["r"] and g["c"] == pac["c"]:
            return True
    return False


def reset_positions(world):
    """Амь алдсаны дараа Пакман, сүнснүүдийг эхний байрлалд нь буцаана."""
    world["pac"]["r"], world["pac"]["c"] = world["pac_start"]
    world["pac"]["dr"] = 0
    world["pac"]["dc"] = 0
    for i in range(len(world["ghosts"])):
        world["ghosts"][i]["r"], world["ghosts"][i]["c"] = world["ghost_start"][i]
        world["ghosts"][i]["dr"] = 0
        world["ghosts"][i]["dc"] = 0


# ----------------------------------------------------------------------
# ЗУРАХ
# ----------------------------------------------------------------------

def draw(world, message=""):
    """Талбайг бүхэлд нь дахин зурна."""
    home()
    pac = world["pac"]
    ghosts = world["ghosts"]

    print(color(" П А К М А Н ", "yellow", bold=True) +
          color("   (W A S D — хөдлөх,  Q — гарах)", "grey"))

    for r in range(len(LEVEL)):
        out = ""
        for c in range(len(LEVEL[r])):
            # Юу зурахаа дээрээс нь доош нь шалгана.
            if pac["r"] == r and pac["c"] == c:
                out += color("ᗧ", "yellow", bold=True)
            elif any(g["r"] == r and g["c"] == c for g in ghosts):
                out += color("ᗣ", "red", bold=True)
            elif (r, c) in world["walls"]:
                out += color("█", "blue")
            elif (r, c) in world["dots"]:
                out += color("·", "white")
            else:
                out += " "
        print(out)

    print(color(f" Оноо: {world['score']}", "green") +
          color(f"    Амь: {'♥ ' * world['lives']}", "red") +
          color(f"   Үлдсэн цэг: {len(world['dots'])}", "cyan"))
    if message:
        print(" " + message + "          ")
    else:
        print(" " * 40)


# ----------------------------------------------------------------------
# ДЭЛГЭЦҮҮД
# ----------------------------------------------------------------------

def show_intro():
    clear()
    print(color("""
        ██████   ██████   ██████
        ██   ██ ██    ██ ██
        ██████  ██████   ██
        ██      ██   ██  ██
        ██      ██   ██   ██████   П А К М А Н
    """, "yellow", bold=True))
    print(color("  Бүх цэгийг (·) цуглуул. Улаан сүнснүүдээс (ᗣ) зугт!", "white"))
    print(color("  Хөдлөх: W A S D эсвэл сумны товч.   Гарах: Q\n", "grey"))
    input(color("  Эхлэхийн тулд Enter дар... ", "cyan"))


def show_end(world, won):
    clear()
    if won:
        print(color("\n   🏆  ЧИ ЯЛЛАА!  Бүх цэгийг цуглууллаа!\n", "green", bold=True))
    else:
        print(color("\n   💀  ТОГЛООМ ДУУСЛАА.  Сүнснүүд чамайг барьлаа.\n", "red", bold=True))
    print(color(f"   Эцсийн оноо: {world['score']}\n", "yellow", bold=True))


# ----------------------------------------------------------------------
# ҮНДСЭН ДАВТАЛТ
# ----------------------------------------------------------------------

def game_loop(world):
    """Тоглоомын гол давталт. Ялвал True, хожигдвол False буцаана."""
    message = "Хөдөлж эхлэхийн тулд товч дар!"
    while True:
        # 1) Оролт уншина (хамгийн сүүлд дарсан чиглэлийг л авна).
        key = read_key()
        while key != "":
            if key == "q":
                return None                 # тоглогч гарлаа
            elif key == "w":
                world["pac"]["dr"], world["pac"]["dc"] = -1, 0
            elif key == "s":
                world["pac"]["dr"], world["pac"]["dc"] = 1, 0
            elif key == "a":
                world["pac"]["dr"], world["pac"]["dc"] = 0, -1
            elif key == "d":
                world["pac"]["dr"], world["pac"]["dc"] = 0, 1
            key = read_key()

        # 2) Пакман хөдөлнө.
        move_pac(world)

        # 3) Сүнснүүд хааяа хөдөлнө.
        world["tick"] += 1
        if world["tick"] % GHOST_EVERY == 0:
            move_ghosts(world)

        # 4) Мөргөлдөөн шалгана (Пакман хөдөлсний дараа ба сүнс хөдөлсний дараа).
        if caught(world):
            world["lives"] -= 1
            if world["lives"] <= 0:
                draw(world, color("Амь дууслаа...", "red"))
                return False
            draw(world, color("Барьдлаа! Дахин эхэл...", "red"))
            time.sleep(1.0)
            reset_positions(world)
            message = ""

        # 5) Бүх цэгийг идсэн эсэхийг шалгана.
        if len(world["dots"]) == 0:
            draw(world, color("Бүх цэгийг идлээ!", "green"))
            return True

        # 6) Дэлгэцийг шинэчилнэ.
        draw(world, message)
        message = ""
        time.sleep(TICK)


def main():
    show_intro()
    world = build_world()

    # Терминалыг "raw" горимд оруулж, нэг товчийг шууд уншина.
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        hide_cursor()
        clear()
        result = game_loop(world)
    finally:
        # Юу ч болсон терминалаа хэвийн болгож сэргээнэ.
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
        show_cursor()

    if result is None:
        clear()
        print(color("\n  Тоглоомоос гарлаа. Баяртай!\n", "grey"))
    else:
        time.sleep(1.0)
        show_end(world, result)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Гэнэт тасалбал курсорыг сэргээнэ.
        print("\033[?25h", end="")
        print(color("\n\n  Тоглоомоос гарлаа. Баяртай!\n", "grey"))
