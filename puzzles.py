from __future__ import annotations

import random


class Puzzle:
    def __init__(self, puzzle_id: str, prompt: str, answer: str, brute_force_space: int) -> None:
        self.puzzle_id = puzzle_id
        self.prompt = prompt
        self.answer = answer
        self.brute_force_space = brute_force_space
        self.solved = False

    def try_solve(self, attempt: str) -> bool:
        if attempt.strip() == self.answer:
            self.solved = True
            return True
        return False


class PatternPuzzle(Puzzle):
    def __init__(self) -> None:
        symbols = ["sun", "moon", "star", "eye", "key", "wave", "flame", "crown"]
        super().__init__(
            puzzle_id="pattern_lock",
            prompt="Arrange symbols in the correct sequence.",
            answer=" ".join(symbols),
            brute_force_space=40_320,
        )
        self.symbols = symbols

    def shuffled_symbols(self) -> list[str]:
        pool = self.symbols[:]
        random.shuffle(pool)
        return pool


def build_puzzles() -> dict[str, Puzzle]:
    return {
        "archive_lock": Puzzle(
            puzzle_id="archive_lock",
            prompt="Enter 12-digit terminal unlock code",
            # First 12 digits of pi, including the leading "3" before the decimal point.
            answer="314159265358",
            brute_force_space=10**12,
        ),
        "pattern_lock": PatternPuzzle(),
        "vault_lock": Puzzle(
            puzzle_id="vault_lock",
            prompt="Enter 10-digit vault authentication code",
            # First 10 digits of Euler's number (e).
            answer="2718281828",
            brute_force_space=10**10,
        ),
    }
