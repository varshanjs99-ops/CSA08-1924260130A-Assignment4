from pathlib import Path
import csv
from .reader import read_department_file
from .validator import parse_registration, InvalidRegistration

def process_departments(input_dir, department_names, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    master = {}
    errors = []

    for department in department_names:
        file_path = input_dir / f"{department.lower()}.txt"
        try:
            for line_number, raw_line in read_department_file(file_path):
                if not raw_line.strip():
                    continue
                try:
                    item = parse_registration(raw_line, department)
                except InvalidRegistration as exc:
                    errors.append((file_path.name, line_number, str(exc), raw_line))
                    continue

                if item.register in master:
                    # Same register number: keep first canonical identity details,
                    # merge any new events, and record a duplicate row for audit.
                    master[item.register]["events"].update(item.events)
                    errors.append((file_path.name, line_number,
                                   "duplicate registration merged by register number", raw_line))
                else:
                    master[item.register] = {
                        "register": item.register,
                        "name": item.name,
                        "department": item.department,
                        "email": item.email,
                        "events": set(item.events)
                    }
        except FileNotFoundError:
            errors.append((file_path.name, 0, "department file missing; skipped", "" ))
        except PermissionError as exc:
            errors.append((file_path.name, 0, f"permission denied: {exc}", "" ))
        except UnicodeDecodeError as exc:
            errors.append((file_path.name, 0, f"UTF-8 decoding failed: {exc}", "" ))

    # Write a clean master list using CSV quoting.
    with (output_dir / "master_registrations.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["register", "name", "department", "email", "events"])
        for reg in sorted(master):
            item = master[reg]
            writer.writerow([
                item["register"], item["name"], item["department"], item["email"],
                ";".join(sorted(item["events"]))
            ])

    # Build event-wise participant files.
    event_map = {}
    for item in master.values():
        for event in item["events"]:
            event_map.setdefault(event, []).append(item)
    for event, people in event_map.items():
        safe_name = "".join(ch.lower() if ch.isalnum() else "_" for ch in event).strip("_")
        with (output_dir / f"event_{safe_name}.csv").open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["register", "name", "department", "email"])
            for item in sorted(people, key=lambda person: person["register"]):
                writer.writerow([
                    item["register"], item["name"], item["department"], item["email"]
                ])

    with (output_dir / "summary_report.txt").open("w", encoding="utf-8") as f:
        f.write("COLLEGE FEST REGISTRATION SUMMARY\n")
        f.write(f"Unique students: {len(master)}\n")
        f.write(f"Unique events: {len(event_map)}\n")
        for event, people in sorted(event_map.items()):
            f.write(f"{event}: {len(people)} participant(s)\n")
    with (output_dir / "error.log").open("w", encoding="utf-8") as f:
        for filename, line_no, message, raw in errors:
            f.write(f"{filename}:{line_no}: {message}; raw={raw!r}\n")

    return master, event_map, errors
