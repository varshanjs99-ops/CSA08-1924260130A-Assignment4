from pathlib import Path
from fest_package import process_departments

def main():
    root = Path(__file__).parent
    departments = ["CSE", "ECE", "EEE", "MECH", "CIVIL"]
    master, events, errors = process_departments(
        root / "department_files", departments, root / "outputs"
    )
    print("COLLEGE FEST REGISTRATION DESK")
    print("Unique students:", len(master))
    print("Events:", sorted(events))
    print("Event participant counts:", {event: len(rows) for event, rows in sorted(events.items())})
    print("Errors / audit records:")
    for err in errors:
        print(err)
    print("Output files are in:", root / "outputs")

if __name__ == "__main__":
    main()
