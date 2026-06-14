from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import EscapeRoomGame

KONAMI_SEQUENCE = ["up", "up", "down", "down", "left", "right", "left", "right", "b", "a"]


def debug_enabled_from_env() -> bool:
    """Enable debug mode when ESCAPE_ROOM_DEBUG is one of: 1, true, on, yes."""
    return os.getenv("ESCAPE_ROOM_DEBUG", "").strip().lower() in {"1", "true", "on", "yes"}


def process_hidden_command(game: "EscapeRoomGame", command: str) -> bool:
    lowered = command.strip().lower()

    if lowered in {"xyzzy", "iddqd", "/escape-now"}:
        game.win("A hidden command echoed through the walls. Emergency shutters opened instantly.")
        return True

    if lowered == "sudo letmein":
        game.inventory.add("master key")
        game.logs.append("A master key drops from a hidden slot.")
        return True

    if lowered == "sudo debug-on":
        game.debug_mode = True
        game.logs.append("[DEBUG] Debug mode activated.")
        return True

    if lowered == "unlock --debug" and game.debug_mode:
        game.win("Debug override accepted. Test exit unlocked.")
        return True

    token = lowered
    if token in {"up", "down", "left", "right", "a", "b"}:
        game.konami_buffer.append(token)
        game.konami_buffer = game.konami_buffer[-len(KONAMI_SEQUENCE):]
        if game.konami_buffer == KONAMI_SEQUENCE:
            game.win("Legacy cheat sequence accepted. You found the developer backdoor.")
            return True
        return True

    return False
