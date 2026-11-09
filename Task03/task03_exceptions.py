"""Task 3 - Custom exception and complete try/except/else/finally."""
from pathlib import Path
import tempfile
import os
from datetime import date

class InvalidRecord(Exception):
    """Raised when an attendance line is not in the expected format."""

class AttendanceFileError(Exception):
    """Raised when an attendance source file cannot be opened."""

def parse_line(line):
    parts = line.strip().split(",")
    if len(parts) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    register, date_text, status = (part.strip() for part in parts)
    if status not in {"P", "A"}:
        raise InvalidRecord(f"invalid status {status!r}")
    if not register or not date_text:
        raise InvalidRecord("register and date must not be empty")
    try:
        date.fromisoformat(date_text)
    except ValueError as exc:
        raise InvalidRecord(f"invalid ISO date {date_text!r}") from exc
    return register, date_text, status

def summarise(path):
    present = absent = 0
    errors = []
    source = None
    try:
        try:
            source = open(path, "r", encoding="utf-8-sig")
        except OSError as exc:
            raise AttendanceFileError(f"cannot open attendance file: {path}") from exc
    except AttendanceFileError as exc:
        cause_name = type(exc.__cause__).__name__ if exc.__cause__ else "unknown"
        errors.append((0, f"{exc} (original cause: {cause_name})"))
    else:
        try:
            for line_number, line in enumerate(source, start=1):
                if not line.strip():
                    continue
                try:
                    _, _, status = parse_line(line)
                except InvalidRecord as exc:
                    errors.append((line_number, str(exc)))
                else:
                    if status == "P":
                        present += 1
                    else:
                        absent += 1
        except UnicodeDecodeError as exc:
            errors.append((0, f"decoding error: {exc}"))
        finally:
            # Explicitly close even if iteration/decoding raises an exception.
            source.close()
    return present, absent, errors

if __name__ == "__main__":
    data = (
        "192311001,2026-10-08,P\n"
        "192311002,2026-10-08,A\n"
        "192311003,2026-10-08\n"
        "192311004,2026-10-08,L\n"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as temp:
        temp.write(data)
        sample = temp.name
    try:
        print("Valid and invalid sample:", summarise(sample))
    finally:
        os.remove(sample)
    print("Missing-file handling:", summarise(sample + ".missing"))

    # Misuse experiment: broad except hides a programming typo (NameError).
    try:
        print(unknown_variable_typo)
    except Exception:
        pass
    print("Program continued, but the NameError was hidden by except Exception: pass")
