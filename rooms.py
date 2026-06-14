from __future__ import annotations

ROOMS = {
    "cell": {
        "name": "Rust Cell",
        "description": (
            "A damp concrete cell with a bolted cot and scratched walls. "
            "A tiny vent whispers air from somewhere deeper in the complex."
        ),
        "exits": {"east": "hall"},
        "items": ["note"],
        "locked_exits": {},
    },
    "hall": {
        "name": "Hall of Delays",
        "description": (
            "Long fluorescent lights buzz overhead. Three heavy doors stand out: "
            "north to the archive, east to the pattern chamber, and south to the vault antechamber."
        ),
        "exits": {"west": "cell", "north": "archive", "east": "pattern", "south": "vault"},
        "items": ["metal shard"],
        "locked_exits": {"south": "archive_lock"},
    },
    "archive": {
        "name": "Archive Terminal Room",
        "description": (
            "Dusty binders and a blinking terminal cover the room. "
            "A painted message on a pillar reads: 'Xylophones Yield Zealous Zigs Yearly.'"
        ),
        "exits": {"south": "hall"},
        "items": ["cipher page"],
        "locked_exits": {},
    },
    "pattern": {
        "name": "Permutation Chamber",
        "description": (
            "A circular chamber with rotating tiles. Each attempt shuffles symbol positions, "
            "as if mocking brute force."
        ),
        "exits": {"west": "hall"},
        "items": ["strange coin"],
        "locked_exits": {},
    },
    "vault": {
        "name": "Vault Antechamber",
        "description": (
            "A final reinforced door blocks the way out. An engraved keypad demands a 10+ digit code."
        ),
        "exits": {"north": "hall", "east": "exit"},
        "items": [],
        "locked_exits": {"east": "vault_lock"},
    },
    "exit": {
        "name": "Outside",
        "description": "Cold night air hits your face. You made it out.",
        "exits": {},
        "items": [],
        "locked_exits": {},
    },
}

ITEM_DESCRIPTIONS = {
    "note": "A crumpled note: 'Digits of circles calm machines.'",
    "metal shard": "A sharp shard with tiny arrows etched in sequence.",
    "cipher page": "A page says: 'Long numbers are easier when constants are loved.'",
    "strange coin": "A coin with symbols: SUN, MOON, STAR, EYE.",
    "master key": "A universal key stamped 'SERVICE OVERRIDE'.",
}
