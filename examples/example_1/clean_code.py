"""
Refactored version of ``messy_code.py`` applying SOLID principles,
improving readability, structure, and adding comprehensive documentation.
The functionality remains unchanged.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import List, Any


class FileHandler:
    """
    Handles reading from and writing to files.

    Responsibilities:
        * Loading data from a file.
        * Saving processed data to a file.
    """

    @staticmethod
    def load(file_path: str) -> List[str]:
        """
        Load lines from ``file_path`` and return them stripped of trailing newlines.

        Args:
            file_path: Path to the file to read.

        Returns:
            A list of stripped strings. Returns an empty list if the file does not exist.
        """
        path = Path(file_path)
        if not path.exists():
            print("file not found")
            return []

        with path.open("r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]

    @staticmethod
    def save(data: List[Any], file_path: str) -> None:
        """
        Write ``data`` to ``file_path`` – one element per line.

        Args:
            data: Iterable of items to be written. Each item is converted to ``str``.
            file_path: Destination file.
        """
        path = Path(file_path)
        with path.open("w", encoding="utf-8") as f:
            for item in data:
                f.write(f"{item}\n")


class DataProcessor:
    """
    Processes a collection of heterogeneous items.

    The processing rules are:
        * ``int``  → even numbers are doubled, odd numbers are tripled.
        * ``str``  → stripped of surrounding whitespace and converted to upper‑case.
        * any other type → ``None``.
    """

    @staticmethod
    def process(items: List[Any]) -> List[Any]:
        """
        Apply the processing rules to ``items``.

        Args:
            items: List of values to process.

        Returns:
            A new list containing the processed values.
        """
        result: List[Any] = []
        for item in items:
            if isinstance(item, int):
                result.append(item * 2 if item % 2 == 0 else item * 3)
            elif isinstance(item, str):
                result.append(item.strip().upper())
            else:
                result.append(None)
        return result


class Stuff:
    """
    Simple utility class demonstrating stateful behaviour.

    Attributes:
        x (int): A numeric value supplied at construction time.
    """

    def __init__(self, x: int) -> None:
        """
        Initialise the instance with ``x``.

        Args:
            x: An integer used by ``do`` and ``calc``.
        """
        self.x = x

    def do(self) -> None:
        """Print a message that includes the stored ``x`` value."""
        print("doing stuff with", self.x)

    def calc(self) -> int:
        """
        Perform a deterministic calculation based on ``x``.

        Returns:
            The sum of ``i * x`` for ``i`` ranging from 0 to 9 inclusive.
        """
        return sum(i * self.x for i in range(10))


def run() -> None:
    """
    Entry point for the command‑line interface.

    Expected usage:
        ``python messy_code.py <input_file>``

    The function loads data from the supplied file, processes it,
    and writes the result to ``out.txt``.  It prints helpful messages
    for missing arguments or empty input.
    """
    if len(sys.argv) < 2:
        print("no file")
        return

    input_file = sys.argv[1]
    raw_data = FileHandler.load(input_file)

    if not raw_data:
        print("empty")
        return

    processed = DataProcessor.process(raw_data)
    FileHandler.save(processed, "out.txt")


def weird() -> None:
    """
    Demonstrates usage of the ``Stuff`` class.
    """
    obj = Stuff(5)
    obj.do()
    print(obj.calc())


if __name__ == "__main__":
    run()
    weird()