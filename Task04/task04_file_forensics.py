"""Task 4 - Demonstrate and repair a library return-log program."""
from pathlib import Path
import tempfile
import os

def save_returns_buggy(books, log_path):
    log = open(log_path, "w", encoding="utf-8")
    for book in books:
        log.write(book)  # no newline; 'w' truncates prior days
    log.close()

def process_buggy(day_file, log_path):
    try:
        books = open(day_file, "r", encoding="utf-8").read().split("\n")
        save_returns_buggy(books, log_path)
    except FileNotFoundError:
        print("missing")

def save_returns_fixed(books, log_path):
    with open(log_path, "a", encoding="utf-8") as log:
        for book in books:
            if book.strip():
                log.write(book.rstrip("\r\n") + "\n")

def process_fixed(day_file, log_path, error_log):
    try:
        with open(day_file, "r", encoding="utf-8") as source:
            books = source.read().splitlines()
        save_returns_fixed(books, log_path)
        return True
    except FileNotFoundError as exc:
        with open(error_log, "a", encoding="utf-8") as errors:
            errors.write(f"{day_file}: {exc}\n")
        return False
    except PermissionError as exc:
        with open(error_log, "a", encoding="utf-8") as errors:
            errors.write(f"{day_file}: permission denied: {exc}\n")
        return False

if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        days = []
        for index, books in enumerate([
            ["Book A", "Book B"],
            ["Book C"],
            ["Book D", "Book E"]
        ], start=1):
            path = root / f"day{index}.txt"
            path.write_text("\n".join(books) + "\n", encoding="utf-8")
            days.append(path)

        bad_log = root / "buggy_returns.log"
        for day in days:
            process_buggy(day, bad_log)
        print("Buggy log after three days:", repr(bad_log.read_text(encoding="utf-8")))

        fixed_log = root / "returns.log"
        errors = root / "errors.log"
        for day in days:
            process_fixed(day, fixed_log, errors)
        print("Fixed log after three days:")
        print(fixed_log.read_text(encoding="utf-8"), end="")
        print("Error log exists:", errors.exists())
        print("Missing day handled:", process_fixed(root / "missing_day.txt", fixed_log, errors))
        print("Final error log:", errors.read_text(encoding="utf-8"))
