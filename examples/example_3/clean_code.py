"""
Refactored implementation of the original ``messy_code_3.py`` using SOLID principles.

Key improvements:
- **Single Responsibility**: Separate classes for user representation, user management,
  persistence, and logging.
- **Open/Closed**: New storage mechanisms can be added by extending ``UserRepository``.
- **Liskov Substitution**: ``FileUserRepository`` can replace any ``UserRepository``.
- **Interface Segregation**: Small, focused interfaces (methods) for each class.
- **Dependency Inversion**: High‑level ``Manager`` depends on abstractions
  (``UserService``, ``UserRepository``, ``Logger``) rather than concrete implementations.

The public behaviour (adding/removing users, printing, saving/loading, logging) is
identical to the original script.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Protocol


# --------------------------------------------------------------------------- #
# Domain model
# --------------------------------------------------------------------------- #
@dataclass
class User:
    """Simple data holder for a user."""
    name: str
    age: int


# --------------------------------------------------------------------------- #
# Repository abstraction (Persistence)
# --------------------------------------------------------------------------- #
class UserRepository(Protocol):
    """Abstract repository for persisting ``User`` objects."""

    def save(self, users: List[User], file_path: Path) -> None:
        """Persist a collection of users to *file_path*."""
        ...

    def load(self, file_path: Path) -> List[User]:
        """Load users from *file_path* and return them."""
        ...


class FileUserRepository:
    """
    Concrete ``UserRepository`` that stores users in a plain‑text CSV file.

    Each line in the file has the format: ``name,age``.
    """

    def save(self, users: List[User], file_path: Path) -> None:
        """Write ``users`` to *file_path*."""
        with file_path.open("w", encoding="utf-8") as f:
            for user in users:
                f.write(f"{user.name},{user.age}\n")

    def load(self, file_path: Path) -> List[User]:
        """Read users from *file_path*; malformed lines are ignored."""
        loaded: List[User] = []
        try:
            with file_path.open("r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) != 2:
                        continue  # skip malformed line
                    name, age_str = parts
                    try:
                        age = int(age_str)
                        loaded.append(User(name=name, age=age))
                    except ValueError:
                        continue  # skip lines with non‑numeric age
        except FileNotFoundError:
            print("error loading file")
        return loaded


# --------------------------------------------------------------------------- #
# Logging abstraction
# --------------------------------------------------------------------------- #
class Logger:
    """Collects log messages in memory and can display them."""

    def __init__(self) -> None:
        self._messages: List[str] = []

    def log(self, message: str) -> None:
        """Add *message* to the internal log."""
        self._messages.append(message)

    def show(self) -> None:
        """Print all stored log messages to stdout."""
        for msg in self._messages:
            print(msg)


# --------------------------------------------------------------------------- #
# Service layer (User management)
# --------------------------------------------------------------------------- #
class UserService:
    """
    Handles business rules around ``User`` objects.

    It does **not** know anything about persistence or logging – those concerns
    are delegated to ``UserRepository`` and ``Logger`` respectively.
    """

    def __init__(self, repository: UserRepository, logger: Logger) -> None:
        self._users: List[User] = []
        self._repo = repository
        self._logger = logger

    # ------------------------------------------------------------------- #
    # CRUD operations
    # ------------------------------------------------------------------- #
    def add_user(self, name: str, age: int) -> None:
        """
        Add a new user if *age* is positive.

        Invalid ages are reported via ``print`` to keep behaviour identical to
        the original script.
        """
        if age > 0:
            self._users.append(User(name=name, age=age))
        else:
            print("invalid age")

    def remove_user(self, name: str) -> None:
        """Remove the first user whose ``name`` matches the supplied value."""
        for user in self._users:
            if user.name == name:
                self._users.remove(user)
                break

    def list_users(self) -> None:
        """Print each user's name and age."""
        for user in self._users:
            print(user.name, user.age)

    # ------------------------------------------------------------------- #
    # Persistence helpers
    # ------------------------------------------------------------------- #
    def save(self, file_path: str | Path) -> None:
        """Delegate saving to the configured ``UserRepository``."""
        self._repo.save(self._users, Path(file_path))

    def load(self, file_path: str | Path) -> None:
        """
        Load users from *file_path* and append them to the current collection.

        This mirrors the original behaviour where loaded users are added on top
        of any existing ones.
        """
        loaded = self._repo.load(Path(file_path))
        self._users.extend(loaded)

    # ------------------------------------------------------------------- #
    # Logging helpers
    # ------------------------------------------------------------------- #
    def log(self, message: str) -> None:
        """Forward a log message to the injected ``Logger``."""
        self._logger.log(message)

    def show_logs(self) -> None:
        """Display all stored log messages."""
        self._logger.show()


# --------------------------------------------------------------------------- #
# High‑level façade (original Manager responsibilities)
# --------------------------------------------------------------------------- #
class Manager:
    """
    Orchestrates user management, persistence and logging.

    The public API matches the original script's ``doEverything`` method.
    """

    def __init__(self) -> None:
        self._logger = Logger()
        self._repository = FileUserRepository()
        self._service = UserService(repository=self._repository, logger=self._logger)

    def do_everything(self) -> None:
        """Execute the same sequence of actions as the original ``doEverything``."""
        self._service.add_user("Alice", 25)
        self._service.add_user("Bob", -1)          # triggers "invalid age"
        self._service.list_users()
        self._service.save("users.txt")
        self._service.load("users.txt")
        self._service.show_logs()


# --------------------------------------------------------------------------- #
# Entry point (mirrors original script)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    manager = Manager()
    manager.do_everything()