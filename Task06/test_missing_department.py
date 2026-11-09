"""Isolated test: a missing department file is logged but does not stop processing."""
from pathlib import Path
import tempfile
import shutil
from fest_package import process_departments

if __name__ == "__main__":
    source = Path(__file__).parent / "department_files"
    with tempfile.TemporaryDirectory() as temp:
        temp = Path(temp)
        inp = temp / "input"
        out = temp / "output"
        inp.mkdir()
        for name in ["cse.txt", "ece.txt", "eee.txt", "mech.txt"]:
            shutil.copy2(source / name, inp / name)
        # civil.txt deliberately omitted
        master, events, errors = process_departments(
            inp, ["CSE", "ECE", "EEE", "MECH", "CIVIL"], out
        )
        missing = [e for e in errors if e[0] == "civil.txt"]
        print("Missing CIVIL file detected:", bool(missing))
        print("Other departments still processed:", len(master) > 0)
        print("Missing-file error:", missing)
