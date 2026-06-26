# Kami-2 Curriculum: "Dungeon Escape"
### Real Python in VS Code — building one terminal game across 12 lessons (Ages 10–13)

---

## Course Overview

In Kami-1, students learned core programming concepts (variables, conditionals, loops, functions) inside a guided, game-based platform. They have never written code from a blank file or structured a program on their own.

**Kami-2 makes three jumps:**
1. From a guided platform → a real editor (VS Code) running real `.py` files.
2. From isolated exercises → one continuous project that grows every lesson.
3. From "make this snippet work" → "design, debug, and finish a real program."

By the end, every student graduates with a **playable terminal dungeon game they built themselves**, line by line, over 12 lessons.

### Big-picture learning outcomes
By graduation, students can:
- Set up and run Python in VS Code, and **read and fix error messages** (this is huge).
- Use variables, numbers, strings, and f-strings confidently.
- Control program flow with `if/elif/else`, boolean logic, `while` and `for` loops.
- Store data in **lists** and **dictionaries**.
- Write and call their own **functions** with parameters and return values.
- Use the **random** module and basic **file reading/writing**.
- Break a problem into steps, trace through their own code, and debug independently.

### How the project grows
Each lesson adds ONE feature to the same game file. Students never start over — they open last week's file and extend it. The motto: *"Today we make the game do something it couldn't do before."*

---

## Before Lesson 1: Setup (do this in the first 30 min of L1, or a short orientation session)
- Install Python (check "Add to PATH" on Windows) + VS Code + the Python extension.
- Create one folder per student: `dungeon_escape/` with a file `game.py`.
- Teach the loop they'll repeat all course: **write code → press Run → read what happens.**
- Run a one-line `print("It works!")` so everyone sees green before lesson content begins.

> **Teacher tip:** Expect chaos here — wrong Python version, file not saved, "it says error." Budget time. Once setup works, the rest of the course is smooth.

---

## The 12 Lessons

Each lesson lists: **New Python concept**, **Logic/algorithm focus**, **Project milestone** (what they add to the game), a **Warm-up**, a **Sample snippet**, **Common pitfalls**, and **Homework**.

---

### Lesson 1 — Hello, Dungeon (Output, Input, Variables, Strings)
- **New Python:** `print()`, `input()`, variables, strings, `#` comments.
- **Logic focus:** A program runs top to bottom, one line at a time.
- **Project milestone:** Title screen + story intro + ask the player's name and greet them.
- **Warm-up:** Everyone prints their name and favorite food on two lines.
- **Sample snippet:**
  ```python
  print("=== DUNGEON ESCAPE ===")
  name = input("What is your name, adventurer? ")
  print("Welcome, " + name + ". You wake up in a cold, dark cell...")
  ```
- **Common pitfalls:** Missing quotes; missing parentheses; forgetting to save before running.
- **Homework:** Write a 3-line intro story for your dungeon in your own words.

---

### Lesson 2 — The Hero's Stats (Numbers, Math, f-strings)
- **New Python:** integers, basic arithmetic (`+ - * /`), f-strings (`f"..."`), `int()`.
- **Logic focus:** Data has *types*; numbers and text behave differently.
- **Project milestone:** Give the hero `health`, `gold`, and `attack` and print a clean character sheet.
- **Warm-up:** Calculate and print "I will be ___ years old in 10 years."
- **Sample snippet:**
  ```python
  health = 100
  gold = 0
  attack = 10
  print(f"{name} | HP: {health} | Gold: {gold} | Attack: {attack}")
  ```
- **Common pitfalls:** Mixing text and numbers (`"5" + 5` errors); forgetting the `f` before the string.
- **Homework:** Add a 4th stat of your choice and show it on the character sheet.

---

### Lesson 3 — Which Way? (if / elif / else)
- **New Python:** `if`, `elif`, `else`, comparison operators (`==`, `<`, `>`).
- **Logic focus:** **Decision trees** — the program chooses a path based on a condition.
- **Project milestone:** First room with a real choice: "Go left or right?" Each path prints a different result.
- **Warm-up (unplugged):** Draw a flowchart on the board: "If it's raining, take umbrella, else wear sunglasses."
- **Sample snippet:**
  ```python
  choice = input("Two corridors. Go (left) or (right)? ")
  if choice == "left":
      print("You find a rusty key on the floor.")
  elif choice == "right":
      print("A bat screeches past your head!")
  else:
      print("You hesitate in the dark.")
  ```
- **Common pitfalls:** Using `=` instead of `==`; indentation errors (the #1 VS Code beginner error — teach it deliberately here).
- **Homework:** Add a third corridor option with its own outcome.

---

### Lesson 4 — The Locked Door (Booleans & Logic: and / or / not)
- **New Python:** `True`/`False`, `and`, `or`, `not`, nested `if`.
- **Logic focus:** **Combining conditions** — "you may pass ONLY if you have the key AND the door is unlocked."
- **Project milestone:** A locked door that opens only if the player picked up the key. A trap room that triggers under a condition.
- **Warm-up:** "True or False?" rapid-fire: `5 > 3 and 2 > 8`, `not (1 == 1)`, etc.
- **Sample snippet:**
  ```python
  has_key = True
  if choice == "left" and has_key:
      print("The key fits! The door creaks open.")
  else:
      print("The door is locked. You need a key.")
  ```
- **Common pitfalls:** Confusing `and`/`or`; over-nesting `if`s. Show how a single boolean variable keeps it clean.
- **Homework:** Add a second locked area that needs a different item.

---

### Lesson 5 — The Game Loop (while loops & input validation)
- **New Python:** `while`, `break`, loop conditions.
- **Logic focus:** **Repetition until a condition changes** — the heart of every game.
- **Project milestone:** Wrap the game in a main loop: keep asking "What do you do?" until the player types `quit` or wins.
- **Warm-up (unplugged):** "Keep clapping WHILE I have my hand up." Visceral intro to loops.
- **Sample snippet:**
  ```python
  playing = True
  while playing:
      action = input("\nWhat do you do? (explore / quit) ")
      if action == "quit":
          print("You give up and sit in the dark...")
          playing = False
      elif action == "explore":
          print("You shuffle deeper into the dungeon.")
      else:
          print("You can't do that here.")
  ```
- **Common pitfalls:** **Infinite loops** (forgetting to ever change the condition) — teach Ctrl+C to stop a runaway program, and treat the first infinite loop as a fun rite of passage.
- **Homework:** Add one more valid action to the loop.

---

### Lesson 6 — The Backpack (Lists & for loops)
- **New Python:** lists `[]`, `.append()`, `for item in list`, `len()`.
- **Logic focus:** **Iteration** — doing the same thing to every item in a collection.
- **Project milestone:** An inventory. Picking up an item adds it to the list; an "inventory" command loops through and displays everything.
- **Warm-up:** Build a class list out loud and "loop" through it: each kid says the next name.
- **Sample snippet:**
  ```python
  inventory = []
  inventory.append("rusty key")
  inventory.append("torch")

  print("Your backpack:")
  for item in inventory:
      print(" -", item)
  ```
- **Common pitfalls:** Index confusion (lists start at 0); printing the whole list vs. looping through it nicely.
- **Homework:** Add a "drop item" idea on paper (we'll code removal next lesson).

---

### Lesson 7 — A Bigger Map (List operations & moving between rooms)
- **New Python:** `in` keyword, `.remove()`, list of rooms / room names.
- **Logic focus:** **State tracking** — the program must "remember" which room you're in.
- **Project milestone:** Several connected rooms; player moves between them; "use key" removes it from inventory.
- **Warm-up:** "Is `apple` in this list?" — predict `in` results before running them.
- **Sample snippet:**
  ```python
  current_room = "entrance"
  if action == "go north" and current_room == "entrance":
      current_room = "hallway"
      print("You enter a long hallway.")

  if "rusty key" in inventory:
      print("You use the key, and it crumbles to dust.")
      inventory.remove("rusty key")
  ```
- **Common pitfalls:** Forgetting to update `current_room`; checking membership on the wrong list.
- **Homework:** Sketch your dungeon map (rooms + which connects to which) on paper.

---

### Lesson 8 — Cleaning Up the Mess (Functions)
- **New Python:** `def`, parameters, `return`, calling functions.
- **Logic focus:** **Decomposition & DRY** ("Don't Repeat Yourself") — turn repeated code into reusable tools.
- **Project milestone:** Refactor. Pull repeated code into functions: `show_status()`, `show_inventory()`, `enter_room(room)`. The game does the same thing but the code is far cleaner.
- **Warm-up:** Compare two whiteboards: 20 messy lines vs. the same logic as 3 named functions. Which would you rather fix?
- **Sample snippet:**
  ```python
  def show_status(name, health, gold):
      print(f"{name} | HP: {health} | Gold: {gold}")

  def show_inventory(inventory):
      print("Backpack:")
      for item in inventory:
          print(" -", item)

  show_status(name, health, gold)
  show_inventory(inventory)
  ```
- **Common pitfalls:** Forgetting to *call* a function; confusing "print inside the function" vs. "return a value." Keep it simple — mostly print-functions at this age.
- **Homework:** Turn one more repeated chunk of your code into a function.

---

### Lesson 9 — Data-Driven Rooms & Monsters (Dictionaries)
- **New Python:** dictionaries `{}`, key lookup, dicts inside lists/dicts.
- **Logic focus:** **Modeling real things as data** — a monster *is* a bundle of properties.
- **Project milestone:** Rooms and monsters become dictionaries with properties (name, description, hp, attack). Adding a new room/monster is now just adding data, not code.
- **Warm-up:** Describe a class pet as a dictionary out loud: `{"name": ..., "legs": ..., "loud": ...}`.
- **Sample snippet:**
  ```python
  goblin = {"name": "Goblin", "hp": 20, "attack": 5}
  print(f"A {goblin['name']} appears! (HP: {goblin['hp']})")

  rooms = {
      "entrance": {"desc": "A damp stone cell.", "exits": ["hallway"]},
      "hallway":  {"desc": "A torchlit corridor.", "exits": ["entrance", "lair"]},
  }
  print(rooms["hallway"]["desc"])
  ```
- **Common pitfalls:** `[]` vs `{}`; KeyError from a typo'd key. Show how to print the whole dict to debug.
- **Homework:** Design 2 monsters and 2 rooms as dictionaries.

---

### Lesson 10 — Roll the Dice (the random module & combat)
- **New Python:** `import random`, `random.randint()`, `random.choice()`.
- **Logic focus:** **Chance & a combat algorithm** — a turn-based loop where both sides take damage until one's HP hits 0.
- **Project milestone:** A working battle: player and monster trade attacks with random damage; loser dies; survivor may get loot.
- **Warm-up:** Roll a real die / `random.randint(1,6)` ten times. Is it predictable? Discuss randomness.
- **Sample snippet:**
  ```python
  import random

  def fight(monster):
      while monster["hp"] > 0 and health > 0:
          dmg = random.randint(3, 8)
          monster["hp"] -= dmg
          print(f"You hit the {monster['name']} for {dmg}! (HP: {monster['hp']})")
          # ...monster attacks back...
  ```
- **Common pitfalls:** Loop that never ends because HP never drops; forgetting `import random`. Combat is the most logic-dense lesson — go slow, trace it on the board.
- **Homework:** Balance your game: tweak damage/HP numbers so fights feel fair.

---

### Lesson 11 — Winning, Losing & Saving (conditions + file read/write)
- **New Python:** clear win/lose conditions; reading & writing a text file (`open`, `with`).
- **Logic focus:** **Terminal states** and **persistence** — knowing when the game is over, and remembering something between runs.
- **Project milestone:** Real win condition (reach the exit / defeat the boss) and lose condition (HP = 0). Save the player's name + a "you won/lost" record or simple high score to a file.
- **Warm-up:** "What three things must be true for YOUR game to be 'won'?" Everyone writes their win condition.
- **Sample snippet:**
  ```python
  if current_room == "exit":
      print("Sunlight! You escaped the dungeon. YOU WIN!")
      with open("scores.txt", "a") as f:
          f.write(f"{name} escaped with {gold} gold\n")
      playing = False
  ```
- **Common pitfalls:** File path confusion (file saves next to `game.py`); win/lose checks placed where the loop never reaches them.
- **Homework:** Make sure your game can actually be won AND lost. Play-test it.

---

### Lesson 12 — Polish & Graduation (testing, debugging, creativity, presenting)
- **New Python:** no new syntax — consolidation, testing, and debugging as a skill.
- **Logic focus:** **Quality** — finding edge cases, fixing crashes, making it your own.
- **Project milestone:** Final polish: personal story, custom rooms/monsters, nicer text, a help menu. Each student **demos their game** to the class.
- **Activities:**
  - Bug hunt: swap games with a partner and try to crash each other's (a fun, structured QA round).
  - Add one "signature feature" that's uniquely yours.
  - Demo day + graduation.
- **Graduation criteria (a student passes Kami-2 if their game):**
  1. Runs from a blank terminal without crashing.
  2. Has at least 3 rooms the player can move between.
  3. Uses a list (inventory) and a dictionary (room or monster data).
  4. Has at least one function they wrote.
  5. Has a win condition and a lose condition.
  6. Contains at least one personal/original touch.

---

## Teaching Notes Across the Whole Course

- **Errors are the curriculum, not the enemy.** Coming off a guided platform, the biggest new skill is reading a traceback. From Lesson 1, when something breaks, read the error *with* the class: "What does the last line say? What line number?" Make debugging normal and unscary.
- **Indentation will be the #1 pain.** VS Code helps, but expect `IndentationError` constantly through Lessons 3–5. Address it head-on.
- **Live-code, then they code.** Demo each new feature live (with at least one deliberate mistake you fix in front of them), then they add it to their own file. Avoid copy-paste — typing builds fluency.
- **Differentiate with the "and then" pattern.** Core task for everyone; "and then, if you finish early..." extensions for fast kids (extra rooms, a shop, a boss). Same project, scalable ambition.
- **Pair weaker + stronger students** during build time, but everyone keeps their own file.
- **Keep a running checklist** on the wall of features the games now have. Visible progress is huge motivation for this age.
- **Save religiously.** Lost work is the fastest way to kill momentum. Build a "save and run" habit from day one; consider a shared backup folder.

---

## Optional: if you'd rather use a different game
The lesson *structure* (concept → feature → milestone) stays identical; only the theme changes:
- **Monster Battler:** rooms → creatures you catch; movement → choosing battles; combat lesson becomes the centerpiece (type advantages via dictionaries).
- **Escape Room / Mystery:** monsters → puzzles; combat lesson → a logic/clue-solving lesson; inventory → collected clues.
