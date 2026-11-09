from pathlib import Path

def read_department_file(path):
    """Yield (line_number, raw_line) from a UTF-8 department file."""
    with Path(path).open("r", encoding="utf-8-sig") as source:
        for line_number, line in enumerate(source, start=1):
            yield line_number, line.rstrip("\r\n")
