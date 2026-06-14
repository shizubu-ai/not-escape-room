from __future__ import annotations

from dataclasses import dataclass, field

from cheats import debug_enabled_from_env, process_hidden_command
from puzzles import PatternPuzzle, build_puzzles
from rooms import ITEM_DESCRIPTIONS, ROOMS


@dataclass
class EscapeRoomGame:
    current_room: str = "cell"
    inventory: set[str] = field(default_factory=set)
    hints_used: int = 0
    running: bool = True
    escaped: bool = False
    puzzles: dict = field(default_factory=build_puzzles)
    logs: list[str] = field(default_factory=list)
    debug_mode: bool = field(default_factory=debug_enabled_from_env)
    konami_buffer: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.room_items = {name: set(data["items"]) for name, data in ROOMS.items()}
        if self.debug_mode:
            self.logs.append("[DEBUG] Environment override detected.")

    def run(self) -> None:
        print("=== NOT ESCAPE ROOM ===")
        print("You wake up in a place designed to waste your life. Type 'help' for commands.")
        self.look()

        while self.running:
            while self.logs:
                print(self.logs.pop(0))

            command = input("\n> ").strip()
            if not command:
                continue
            if process_hidden_command(self, command):
                continue
            self.handle_command(command)

        if self.escaped:
            print("\n🎉 You escaped. Somehow.")
        else:
            print("\nGame over.")

    def handle_command(self, command: str) -> None:
        parts = command.lower().split()
        verb = parts[0]

        if verb == "help":
            self.show_help()
        elif verb == "look":
            self.look()
        elif verb == "go" and len(parts) > 1:
            self.move(parts[1])
        elif verb == "take" and len(parts) > 1:
            self.take(" ".join(parts[1:]))
        elif verb == "inventory":
            self.show_inventory()
        elif verb == "use" and len(parts) > 1:
            target = " ".join(parts[2:]) if len(parts) > 2 else ""
            self.use_item(parts[1], target)
        elif verb == "solve" and len(parts) > 2:
            self.solve(parts[1], " ".join(parts[2:]))
        elif verb == "hint":
            self.hint()
        elif verb in {"quit", "exit"}:
            self.running = False
        else:
            self.logs.append("Unknown command.")

    def show_help(self) -> None:
        self.logs.append(
            "Commands: look, go <direction>, take <item>, use <item> [target], "
            "solve <puzzle> <answer>, inventory, hint, help, quit"
        )

    def look(self) -> None:
        room = ROOMS[self.current_room]
        self.logs.append(f"[{room['name']}] {room['description']}")

        items = sorted(self.room_items[self.current_room])
        if items:
            self.logs.append("You see: " + ", ".join(items))

        exits = ", ".join(sorted(room["exits"].keys())) or "none"
        self.logs.append(f"Exits: {exits}")

        if self.current_room == "pattern":
            pattern = self.puzzles["pattern_lock"]
            if isinstance(pattern, PatternPuzzle) and not pattern.solved:
                self.logs.append("Tiles now show: " + " | ".join(pattern.shuffled_symbols()))

    def move(self, direction: str) -> None:
        room = ROOMS[self.current_room]
        if direction not in room["exits"]:
            self.logs.append("You can't go that way.")
            return

        lock_id = room.get("locked_exits", {}).get(direction)
        if lock_id and not self.puzzles[lock_id].solved:
            if lock_id == "vault_lock":
                self.logs.append("The door keypad flashes: ACCESS DENIED.")
            elif lock_id == "archive_lock":
                self.logs.append("The southern blast door won't budge. Another system controls it.")
            else:
                self.logs.append("That path is locked.")
            return

        if self.current_room == "vault" and direction == "east":
            if not (
                self.puzzles["archive_lock"].solved
                and self.puzzles["pattern_lock"].solved
                and self.puzzles["vault_lock"].solved
            ):
                self.logs.append("The final door remains sealed. Additional authorization required.")
                return

        self.current_room = room["exits"][direction]
        if self.current_room == "exit":
            self.win("You opened the final door and stepped outside.")
            return
        self.look()

    def take(self, item: str) -> None:
        items = self.room_items[self.current_room]
        if item not in items:
            self.logs.append("That item isn't here.")
            return

        items.remove(item)
        self.inventory.add(item)
        description = ITEM_DESCRIPTIONS.get(item, "")
        if description:
            self.logs.append(f"Taken: {item}. {description}")
        else:
            self.logs.append(f"Taken: {item}")

    def show_inventory(self) -> None:
        if not self.inventory:
            self.logs.append("Inventory is empty.")
            return
        self.logs.append("Inventory: " + ", ".join(sorted(self.inventory)))

    def use_item(self, item: str, target: str) -> None:
        if item not in self.inventory:
            self.logs.append("You don't have that item.")
            return

        if item == "master key" and self.current_room == "vault":
            self.puzzles["vault_lock"].solved = True
            self.win("The master key turns once, every lock disengages, and the exit opens.")
            return

        if item == "note" and self.current_room == "archive":
            self.logs.append("The terminal prompt highlights 3.14159265358...")
            return

        if item == "strange coin" and self.current_room == "pattern":
            self.logs.append("The symbols glow in a meaningful order: sun moon star eye")
            return

        self.logs.append(f"You use {item}{' on ' + target if target else ''}, but nothing happens.")

    def solve(self, puzzle_name: str, answer: str) -> None:
        room_to_puzzle = {
            "archive": "archive_lock",
            "pattern": "pattern_lock",
            "vault": "vault_lock",
        }
        expected = room_to_puzzle.get(self.current_room)

        if not expected or expected != puzzle_name:
            self.logs.append("No such puzzle to solve here.")
            return

        puzzle = self.puzzles[expected]
        if puzzle.solved:
            self.logs.append("That puzzle is already solved.")
            return

        if puzzle.try_solve(answer):
            self.logs.append(f"{puzzle_name} solved.")
            if puzzle_name == "archive_lock":
                self.logs.append("A side panel opens; the hall's southern door is now responding.")
            if self.puzzles["archive_lock"].solved and self.puzzles["pattern_lock"].solved and self.puzzles["vault_lock"].solved:
                self.logs.append("All authorization layers disabled. The eastern exit is open.")
        else:
            self.logs.append("Incorrect answer.")

    def hint(self) -> None:
        self.hints_used += 1

        if self.hints_used == 1:
            self.logs.append("Hint: 'look' closely in each room. Some wording is not random.")
        elif self.hints_used == 2:
            self.logs.append("Hint: Long numeric constants can be guessed smarter than brute force.")
        elif self.hints_used == 3:
            self.logs.append("Hint: Some players test old game cheat words.")
        else:
            self.logs.append("Hint: Try commands nobody asked for. Also inspect environment settings.")

    def win(self, message: str) -> None:
        self.logs.append(message)
        self.escaped = True
        self.running = False
