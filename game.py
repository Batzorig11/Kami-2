"""
ШОРОНГООС ЗУГТААХ
Терминал дээр тоглодог адал явдалт тоглоом -- Kami-2 жишээ төсөл.

ЗӨВХӨН Kami-2 хичээлд заасан ойлголтуудыг ашиглаж бүтээсэн:
  хувьсагч, тэмдэгт мөр, f-string, if/elif/else, логик утга,
  while/for давталт, жагсаалт (list), толь бичиг (dict), функц,
  random модуль, болон текст файл унших/бичих.
Класс / OOP огт ашиглаагүй -- энд байгаа бүх зүйлийг оюутан
хичээлийн төгсгөлд биеэрээ бүтээж чадна.

ВИЗУАЛ: терминалын өнгө (ANSI), ASCII зураг, эрүүл мэндийн зураас,
аялах тусам нээгдэх жижиг газрын зураг -- бүгд зүгээр л тэмдэгт мөр.

ХЭРХЭН ЯЛАХ ВЭ:
  Шоронгоос зугт. Өрөөнүүдийг нэгжиж эд зүйл ол, өөрийгөө зэвсэглэ,
  мангасуудаас амьд гар, шатаар авирч эрх чөлөөнд хүр.

Оноо нь энэ файлын хажууд 'dungeon_scores.txt'-д хадгалагдана.
"""

import random
import os

SCORES_FILE = "dungeon_scores.txt"

# ANSI өнгө/дэлгэц цэвэрлэхийг асаах/унтраах ганц тохиргоо.
# Хэрэв таны терминал муухай тэмдэгт харуулбал үүнийг False болго.
USE_COLOR = True
os.system("")   # Windows 10+ дээр ANSI өнгийг асаадаг жижиг заль (бусад дээр хор хөнөөлгүй)

# Функцууд үндсэн давталтыг зогсоох боломжтой жижиг хуваалцсан төлөв.
state = {"running": True}

# Тоглогч очиж үзсэн өрөөнүүд (газрын зураг дээр нээгдэнэ).
visited = []

# ----------------------------------------------------------------------
# ТОГЛООМЫН ӨГӨГДӨЛ
# ----------------------------------------------------------------------

# Тоглогч бол зүгээр л шинж чанаруудын толь бичиг (dict).
player = {
    "name": "",
    "hp": 30,
    "max_hp": 30,
    "attack": 5,
    "gold": 0,
    "inventory": [],
    "location": "cell",
    "last_location": "cell",
}

# Өрөө бүр толь бичиг. Бүх газрын зураг нь өрөөнүүдийн толь бичиг.
rooms = {
    "cell": {
        "name": "Хүйтэн Шорон",
        "desc": "Чийгтэй чулуун шорон. Харанхуйд хаа нэгтээ ус дусална.\n"
                "ХОЙД талын төмөр хаалга бага зэрэг онгорхой байна.\n"
                "Шалны сул чулуунууд доор нь юм нуусан мэт харагдана.",
        "exits": {"хойд": "corridor"},
        "items": [],
        "hidden": ["зэвэрсэн түлхүүр"],   # зөвхөн нэгжиж олно
        "monster": None,
        "locked": False,
        "dark": False,
    },
    "corridor": {
        "name": "Бамбартай Коридор",
        "desc": "Урт коридор. Ханан дээр ганц бамбар анивчина.\n"
                "Замууд УРД, ЗҮҮН, болон ХОЙД зүг рүү (хүнд цоожтой хаалга) хөтөлнө.",
        "exits": {"урд": "cell", "зүүн": "guard_room", "хойд": "treasury"},
        "items": ["бамбар"],
        "hidden": [],
        "monster": None,
        "locked": False,
        "dark": False,
    },
    "guard_room": {
        "name": "Харуулын Өрөө",
        "desc": "Хагарсан ширээ, зэвэрсэн зэвсгийн тавиуртай эмх замбараагүй өрөө.\n"
                "Гарцууд БАРУУН болон ХОЙД зүг рүү хөтөлнө.",
        "exits": {"баруун": "corridor", "хойд": "armory"},
        "items": [],
        "hidden": [],
        "monster": {
            "name": "Гоблин",
            "hp": 16,
            "max_hp": 16,
            "attack": 4,
            "alive": True,
            "gold": 15,
            "drop": "төмөр сэлэм",
            "intro": "Ширүүлсэн ГОБЛИН харайн босч, бороохой даллана!",
        },
        "locked": False,
        "dark": False,
    },
    "armory": {
        "name": "Зэвсгийн Агуулах",
        "desc": "Нарийхан агуулах. Хана бүр тавиураар хучигдсан.",
        "exits": {"урд": "guard_room"},
        "items": ["эдгээх эм"],
        "hidden": [],
        "monster": None,
        "locked": False,
        "dark": True,   # бамбаргүйгээр харж чадахгүй
    },
    "treasury": {
        "name": "Эрдэнэсийн Сан",
        "desc": "Хаа сайгүй алт гялалзана! Шат ДЭЭШ нар руу хөтөлнө.",
        "exits": {"урд": "corridor", "дээш": "freedom"},
        "items": [],
        "hidden": [],
        "monster": {
            "name": "Агуйн Тролл",
            "hp": 38,
            "max_hp": 38,
            "attack": 6,
            "alive": True,
            "gold": 100,
            "drop": None,
            "intro": "Асар том АГУЙН ТРОЛЛ архиран шатыг хамгаална!",
        },
        "locked": True,   # зэвэрсэн түлхүүр хэрэгтэй
        "dark": False,
    },
}

# Зэвсэг бүр хэдэн нэгж довтлох хүч нэмэх вэ.
WEAPONS = {"төмөр сэлэм": 9}

# Мангас бүрийн ASCII зураг (зүгээр л мөрүүдийн жагсаалт).
MONSTER_ART = {
    "Гоблин": [
        "      .-\"\"\"-.",
        "     /  o o  \\",
        "    |    ^    |",
        "     \\  \\_/  /",
        "     /`-----'\\",
        "    / /     \\ \\",
    ],
    "Агуйн Тролл": [
        "       _______",
        "    __/  o  o  \\__",
        "   /   \\  ___  /   \\",
        "   |    \\_____/    |",
        "    \\    |   |    /",
        "    /|   |   |   |\\",
        "   d_|   |___|   |_b",
    ],
}

# Газрын зураг дээрх өрөөний богино нэр.
MAP_ABBR = {
    "cell": "ШОРОН", "corridor": "КОРИД", "guard_room": "ХАРУУ",
    "armory": "АГУУЛ", "treasury": "ЭРДЭН",
}


# ----------------------------------------------------------------------
# ӨНГӨ + ДЭЛГЭЦИЙН ҮНДСЭН ТУСЛАХ ФУНКЦУУД
# ----------------------------------------------------------------------

COLORS = {
    "red": "31", "green": "32", "yellow": "33", "blue": "34",
    "magenta": "35", "cyan": "36", "white": "37", "grey": "90",
}


def color(text, c, bold=False):
    """Тэмдэгт мөрийг өнгөтэй болгож буцаана (өнгө унтраалттай бол хэвээр)."""
    if not USE_COLOR:
        return text
    code = COLORS.get(c, "37")
    start = "1;" if bold else ""
    return f"\033[{start}{code}m{text}\033[0m"


def clear():
    """Дэлгэцийг цэвэрлэнэ."""
    if USE_COLOR:
        print("\033[2J\033[H", end="")


def visible_len(s):
    """Өнгөний нууц кодыг тооцохгүйгээр харагдах урт. (re ашиглахгүй!)"""
    count = 0
    i = 0
    while i < len(s):
        if s[i] == "\033":            # өнгөний код эхэллээ
            while i < len(s) and s[i] != "m":
                i += 1
            i += 1                    # 'm' үсгийг алгасна
        else:
            count += 1
            i += 1
    return count


def pad(s, width, center=False):
    """Тэмдэгт мөрийг харагдах уртаар нь width хүртэл хоосон зайгаар дүүргэнэ."""
    extra = width - visible_len(s)
    if extra < 0:
        extra = 0
    if center:
        left = extra // 2
        return " " * left + s + " " * (extra - left)
    return s + " " * extra


def box(lines, width=52, c="cyan", center=False):
    """Текстийн мөрүүдийг гоё хүрээгээр хүрээлж хэвлэнэ."""
    inner = width - 4
    print(color("╔" + "═" * (width - 2) + "╗", c))
    for ln in lines:
        print(color("║", c) + " " + pad(ln, inner, center) + " " + color("║", c))
    print(color("╚" + "═" * (width - 2) + "╝", c))


def line():
    print(color("─" * 52, "grey"))


def hp_bar(cur, mx, width=16):
    """HP-г өнгөт нүдэн зураас болгож харуулна."""
    if cur < 0:
        cur = 0
    if mx <= 0:
        mx = 1
    filled = int(round(width * cur / mx))
    if filled > width:
        filled = width
    ratio = cur / mx
    if ratio > 0.5:
        c = "green"
    elif ratio > 0.25:
        c = "yellow"
    else:
        c = "red"
    return color("█" * filled + "░" * (width - filled), c)


# ----------------------------------------------------------------------
# ГАЗРЫН ЗУРАГ
# ----------------------------------------------------------------------

def room_cell(key):
    """Газрын зураг дээрх нэг өрөөний нүд (одоогийнх ногоон, нээгдээгүй нь ???)."""
    label = MAP_ABBR[key]
    if key == player["location"]:
        return color("[" + label + "]", "green", bold=True)
    if key in visited:
        return "[" + label + "]"
    return "[ ??? ]"


def draw_map():
    t = room_cell("treasury")
    a = room_cell("armory")
    cr = room_cell("corridor")
    g = room_cell("guard_room")
    s = room_cell("cell")
    grey = "grey"
    return [
        "   " + t + "   " + a,
        color(" " * 6 + "│" + " " * 9 + "│", grey),
        "   " + cr + color("───", grey) + g,
        color(" " * 6 + "│", grey),
        "   " + s,
    ]


def hud():
    """Доод талын мэдээллийн зураас: нэр, HP зураас, алт, довтлох хүч."""
    p = player
    return (f"{color(p['name'], 'white', bold=True)}   "
            f"HP {hp_bar(p['hp'], p['max_hp'])} {p['hp']}/{p['max_hp']}   "
            f"{color('Алт', 'yellow')} {p['gold']}   "
            f"{color('Довтлох', 'cyan')} {p['attack']}")


# ----------------------------------------------------------------------
# ДЭЛГЭЦҮҮД
# ----------------------------------------------------------------------

def show_title():
    clear()
    skull = [
        "        _______",
        "      .'       '.",
        "     /  .-. .-.  \\",
        "     |  'o' 'o'  |",
        "     |     ^     |",
        "      \\  '---'  /",
        "       '._____.'",
    ]
    for ln in skull:
        print(color(ln, "grey"))
    box([
        "",
        color("Ш О Р О Н Г О О С   З У Г Т А А Х", "yellow", bold=True),
        color("терминал адал явдал", "grey"),
        "",
    ], c="magenta", center=True)


def show_help():
    print(color("\nКОМАНДУУД:", "cyan", bold=True))
    print("  яв <чиглэл>      (эсвэл зүгээр: хойд / урд / зүүн / баруун / дээш)")
    print("  хар             - өрөөгөө дахин ажиглах")
    print("  хай             - өрөөг нуугдсан зүйл хайж нэгжих")
    print("  ав <зүйл>        - юм авах")
    print("  хэрэглэ <зүйл>   - зүйл хэрэглэх (ж: 'хэрэглэ эм')")
    print("  тулаан          - өрөөн дэх мангастай тулалдах")
    print("  цүнх (ц)         - юу авч яваагаа харах")
    print("  төлөв           - эрүүл мэнд, чадвараа харах")
    print("  тусламж         - энэ жагсаалтыг харуулах")
    print("  гарах           - бууж өгч тоглоомоос гарах\n")


def show_status():
    print()
    print(hud())


def show_inventory():
    if len(player["inventory"]) == 0:
        print("Таны үүргэвч хоосон байна.")
    else:
        print(color("Таны үүргэвчинд:", "yellow"))
        for item in player["inventory"]:
            print("  •", item)


def describe_room():
    room = rooms[player["location"]]
    if player["location"] not in visited:
        visited.append(player["location"])

    clear()
    box([color(room["name"].upper(), "yellow", bold=True)], center=True)

    for ln in draw_map():
        print(ln)
    print()
    print(room["desc"])

    # Харанхуй өрөөнд бамбар авч яваагүй бол эд зүйлийг харж чадахгүй.
    can_see = (not room["dark"]) or ("бамбар" in player["inventory"])
    if not can_see:
        print(color("\nЭнд ХАР ХАРАНХУЙ байна. Харахын тулд гэрлийн эх үүсвэр хэрэгтэй.",
                    "blue", bold=True))
    elif len(room["items"]) > 0:
        print(color("\nЭнд та харж байна:", "green"))
        for item in room["items"]:
            print("  •", color(item, "green"))

    monster = room["monster"]
    if monster is not None and monster["alive"]:
        print()
        for ln in MONSTER_ART.get(monster["name"], []):
            print(color(ln, "red"))
        print(color(monster["intro"], "red", bold=True))
        print(f"{monster['name']}  HP {hp_bar(monster['hp'], monster['max_hp'])} "
              f"{monster['hp']}/{monster['max_hp']}")

    print(color("\nГарцууд: ", "cyan") + ", ".join(room["exits"].keys()))
    line()
    print(hud())
    line()


# ----------------------------------------------------------------------
# ЭД ЗҮЙЛ + ҮЙЛДЛИЙН ТУСЛАХ ФУНКЦУУД
# ----------------------------------------------------------------------

def find_item(query, item_list):
    """query-тэй тохирох item_list дэх бүтэн нэрийг буцаана, эсвэл None."""
    query = query.strip()
    if query == "":
        return None
    for item in item_list:
        if query == item or query in item or item in query:
            return item
    return None


def do_search():
    room = rooms[player["location"]]
    if room["dark"] and "бамбар" not in player["inventory"]:
        print("Та харанхуйд тэмтэрч үзлээ ч хэрэгтэй юм олсонгүй.")
        return
    if len(room["hidden"]) == 0:
        print("Та анхааралтай нэгжлээ ч нуугдсан юм олсонгүй.")
        return
    print(color("Та өрөөг нэгжээд нэг зүйл оллоо!", "green", bold=True))
    for item in room["hidden"]:
        room["items"].append(item)
        print("  ✦ Илэрсэн:", color(item, "green"))
    room["hidden"] = []


def do_take(target):
    room = rooms[player["location"]]
    can_see = (not room["dark"]) or ("бамбар" in player["inventory"])
    if not can_see:
        print("Харанхуйд авах юмаа харж чадахгүй байна.")
        return
    item = find_item(target, room["items"])
    if item is None:
        print("Энд авах '" + target + "' гэж байхгүй байна.")
        return
    room["items"].remove(item)
    player["inventory"].append(item)
    print("Та " + color(item, "green") + "-г авлаа.")
    # Хэрэв одоогийнхоос сайн зэвсэг бол автоматаар зүүнэ.
    if item in WEAPONS and WEAPONS[item] > player["attack"]:
        player["attack"] = WEAPONS[item]
        print(color(f"Та {item}-г зүүлээ! Таны довтлох хүч одоо {player['attack']}.",
                    "yellow", bold=True))


def do_use(target):
    item = find_item(target, player["inventory"])
    if item is None:
        print("Танд '" + target + "' байхгүй байна.")
        return
    if item == "эдгээх эм":
        if player["hp"] >= player["max_hp"]:
            print("Та аль хэдийн бүрэн эрүүл байна.")
            return
        player["hp"] = min(player["max_hp"], player["hp"] + 18)
        player["inventory"].remove(item)
        print(color(f"Та эмийг уугаад эрч хүчээ сэргээлээ. HP одоо {player['hp']}.",
                    "green"))
    elif item == "бамбар":
        print(color("Та бамбараа өндөрт өргөв. Гэрэл нь харанхуйг ухраав.", "yellow"))
    else:
        print("Та " + item + "-г одоо хэрэглэж чадахгүй.")


def do_move(direction):
    room = rooms[player["location"]]
    if direction not in room["exits"]:
        print("Эндээс " + direction + " зүг рүү явж чадахгүй.")
        return

    target_key = room["exits"][direction]

    # Тусгай зугтаах гарц.
    if target_key == "freedom":
        monster = room["monster"]
        if monster is not None and monster["alive"]:
            print(monster["name"] + " шатыг хааж байна! Эхлээд түүнийг ялаарай.")
            return
        win_game()
        return

    target = rooms[target_key]

    # Цоожтой хаалганд зэвэрсэн түлхүүр хэрэгтэй.
    if target["locked"]:
        if "зэвэрсэн түлхүүр" in player["inventory"]:
            target["locked"] = False
            player["inventory"].remove("зэвэрсэн түлхүүр")
            print(color("Та зэвэрсэн түлхүүрээ эргүүлэв. КЛИК! "
                        "Хаалга онгойж, түлхүүр тоос болон бутрав.", "yellow", bold=True))
        else:
            print("Тэр хаалга чанга цоожтой байна. Танд түлхүүр хэрэгтэй.")
            return

    player["last_location"] = player["location"]
    player["location"] = target_key
    describe_room()


# ----------------------------------------------------------------------
# ТУЛААН
# ----------------------------------------------------------------------

def combat_frame(monster, log):
    """Тулааны нэг хүрээг (зураг + хоёр HP зураас + сүүлийн мэдээ) дахин зурна."""
    clear()
    box([color("⚔   Т У Л А А Н   ⚔", "red", bold=True)], c="red", center=True)
    for ln in MONSTER_ART.get(monster["name"], []):
        print(color(ln, "red"))
    print()
    mhp = monster["hp"] if monster["hp"] > 0 else 0
    print(f"  {pad(color(monster['name'], 'red', bold=True), 16)} "
          f"HP {hp_bar(mhp, monster['max_hp'])} {mhp}/{monster['max_hp']}")
    print(f"  {pad(color(player['name'], 'white', bold=True), 16)} "
          f"HP {hp_bar(player['hp'], player['max_hp'])} {player['hp']}/{player['max_hp']}")
    line()
    for m in log[-5:]:
        print("  " + m)


def do_fight():
    room = rooms[player["location"]]
    monster = room["monster"]
    if monster is None or not monster["alive"]:
        print("Энд тулалдах юм байхгүй.")
        return

    log = [color("Та " + monster["name"] + "-тай тулалдахаар зэхлээ!", "yellow")]

    while monster["alive"] and player["hp"] > 0:
        combat_frame(monster, log)
        choice = input("\n  (довтлох) / (эм) уух / (зугтах)? ").lower().strip()

        if choice.startswith(("д", "a")):                # довтлох / attack
            dmg = random.randint(player["attack"] - 2, player["attack"] + 3)
            monster["hp"] -= dmg
            log.append(color(f"Та {monster['name']}-г {dmg} хохирол учруулан цохив!",
                             "green"))

        elif choice.startswith(("э", "у", "p", "h")):    # эм / уух / эдгээх
            if "эдгээх эм" in player["inventory"]:
                player["hp"] = min(player["max_hp"], player["hp"] + 18)
                player["inventory"].remove("эдгээх эм")
                log.append(color(f"Та эм залгиж {player['hp']} HP хүртэл эдгэрлээ.",
                                 "green"))
            else:
                log.append("Танд эм алга! Та сандарч ээлжээ алдлаа.")

        elif choice.startswith(("з", "r", "f")):         # зугтах / run
            if random.randint(1, 100) <= 60:
                print(color("\n  Та салж яваад ирсэн замаараа зугтлаа!", "yellow"))
                player["location"] = player["last_location"]
                describe_room()
                return
            log.append("Та бүдрэв -- зугтах гарц алга!")

        else:
            log.append("Та юу хийхээ мэдэхгүй эргэлзэв.")
            continue   # бичгийн алдаа ээлж тань идэхгүй

        # Мангас унав уу?
        if monster["hp"] <= 0:
            monster["alive"] = False
            combat_frame(monster, log)
            print()
            print(color(f"  Та {monster['name']}-г яллаа!", "green", bold=True))
            if monster["gold"] > 0:
                player["gold"] += monster["gold"]
                print(color(f"  Та {monster['gold']} алт шүүрэн авлаа.", "yellow"))
            if monster["drop"] is not None:
                drop = monster["drop"]
                player["inventory"].append(drop)
                print(color(f"  {monster['name']} {drop} унагав!", "yellow"))
                if drop in WEAPONS and WEAPONS[drop] > player["attack"]:
                    player["attack"] = WEAPONS[drop]
                    print(color(f"  Та {drop}-г зүүлээ! Довтлох хүч одоо {player['attack']}.",
                                "yellow", bold=True))
            return

        # Мангас хариу цохив.
        mdmg = random.randint(monster["attack"] - 1, monster["attack"] + 2)
        player["hp"] -= mdmg
        log.append(color(f"{monster['name']} танд {mdmg} хохирол учруулав!", "red"))

    if player["hp"] <= 0:
        lose_game()


# ----------------------------------------------------------------------
# ЯЛАХ / ЯЛАГДАХ + ОНООНЫ ЖАГСААЛТ (файл унших, бичих)
# ----------------------------------------------------------------------

def save_score(won):
    result = "зугтсан" if won else "унасан"
    try:
        with open(SCORES_FILE, "a") as f:
            f.write(f"{player['name']}|{player['gold']}|{result}\n")
    except OSError:
        print("(Энэ удаад таны оноог хадгалж чадсангүй.)")


def show_high_scores():
    rows = []   # мөр бүр жагсаалт: [алт, нэр, үр дүн]
    try:
        with open(SCORES_FILE, "r") as f:
            for raw in f:
                raw = raw.strip()
                if raw == "":
                    continue
                parts = raw.split("|")
                if len(parts) == 3:
                    rows.append([int(parts[1]), parts[0], parts[2]])
    except FileNotFoundError:
        return   # хараахан оноо хадгалаагүй
    except ValueError:
        return   # онооны файлын мөр гэмтсэн

    if len(rows) == 0:
        return

    rows.sort(reverse=True)   # жагсаалтын жагсаалт эхний зүйлээрээ эрэмбэлэгдэнэ: алт
    print(color("\nАЛДРЫН ТАНХИМ (шилдэг тоглолтууд):", "yellow", bold=True))
    rank = 1
    for row in rows[:5]:
        gold = row[0]
        name = row[1]
        result = row[2]
        print(f"  {rank}. {name} -- {color(str(gold) + ' алт', 'yellow')} ({result})")
        rank += 1
    print()


def win_game():
    clear()
    box([
        "",
        color("*** ТА ЯЛЛАА ***", "green", bold=True),
        "",
    ], c="green", center=True)
    print(color("Та шатаар авирч, нүд гэрэлтэм нарны гэрэлд гарч ирлээ.", "yellow"))
    print("ТА ШОРОНГООС ЗУГТЛАА!")
    print(f"Эцсийн алт: {color(str(player['gold']), 'yellow', bold=True)}")
    line()
    save_score(True)
    show_high_scores()
    state["running"] = False


def lose_game():
    clear()
    box([
        "",
        color("*** ТОГЛООМ ДУУСЛАА ***", "red", bold=True),
        "",
    ], c="red", center=True)
    print(color("Таны хараа харанхуй болж бүдгэрэв...", "grey"))
    print("ТА ШОРОНД УНАЛАА.")
    print(f"Цуглуулсан алт: {color(str(player['gold']), 'yellow')}")
    line()
    save_score(False)
    show_high_scores()
    state["running"] = False


# ----------------------------------------------------------------------
# ҮНДСЭН ТОГЛООМЫН ДАВТАЛТ
# ----------------------------------------------------------------------

def main():
    show_title()
    print("Та харанхуйд, толгой нь хагарам өвдөж, хэрхэн энд ирснээ санахгүй сэрлээ.")
    print("Таны зорилго энгийн: " + color("ЗУГТ.", "green", bold=True) + "\n")

    name = input("Хоригдол минь, таны нэр хэн бэ? ").strip()
    if name == "":
        name = "Нэргүй Нэгэн"
    player["name"] = name
    print(f"\nАмжилт хүсье, {name}. Командуудыг харахын тулд хэзээ ч "
          + color("'тусламж'", "cyan") + " гэж бич.")
    input(color("\n(үргэлжлүүлэхийн тулд Enter дар...)", "grey"))
    describe_room()

    directions = ["хойд", "урд", "зүүн", "баруун", "дээш", "доош"]
    short = {"х": "хойд", "у": "урд", "з": "зүүн",
             "б": "баруун", "д": "дээш"}

    while state["running"]:
        command = input(color("\n> ", "cyan", bold=True)).lower().strip()
        if command == "":
            continue

        words = command.split()
        verb = words[0]
        rest = " ".join(words[1:]) if len(words) > 1 else ""

        if verb in directions:
            do_move(verb)
        elif verb in ("яв", "явах", "оч", "очих", "go", "move"):
            do_move(short[rest] if rest in short else rest)
        elif verb in ("хар", "харах", "ажигла", "look", "l"):
            describe_room()
        elif verb in ("хай", "хайх", "нэгж", "нэгжих", "search"):
            do_search()
        elif verb in ("ав", "авах", "ол", "take", "get"):
            do_take(rest)
        elif verb in ("хэрэглэ", "хэрэглэх", "уу", "уух", "зүү", "use", "drink"):
            do_use(rest)
        elif verb in ("тулаан", "тулалд", "довтол", "зод", "fight", "attack"):
            do_fight()
        elif verb in ("цүнх", "эд", "ц", "inventory", "inv", "i"):
            show_inventory()
        elif verb in ("төлөв", "статус", "status", "me"):
            show_status()
        elif verb in ("тусламж", "команд", "?", "help"):
            show_help()
        elif verb in ("гарах", "гар", "зогс", "quit", "exit"):
            print("Та ханаар налан бууж өгөв. Баяртай.")
            state["running"] = False
        else:
            print("Та '" + command + "'-г хэрхэх вэ гэдгийг мэдэхгүй байна. "
                  + color("'тусламж'", "cyan") + " гэж бич.")


if __name__ == "__main__":
    main()
