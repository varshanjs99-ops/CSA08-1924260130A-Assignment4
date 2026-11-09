"""Task 2 - Monthly biometric attendance file processor."""
from pathlib import Path
import csv
import argparse

def process_month(input_dir, report_file, error_file, threshold=75.0):
    input_path = Path(input_dir)
    counts = {}  # register -> [present_count, absent_count]
    errors = []

    files = sorted(input_path.glob("*.txt"))
    for file_path in files:
        with file_path.open("r", encoding="utf-8-sig") as source:
            for line_number, raw_line in enumerate(source, start=1):
                if not raw_line.strip():
                    continue
                try:
                    parts = [field.strip() for field in raw_line.rstrip("\r\n").split(",")]
                    if len(parts) != 3:
                        raise ValueError(f"expected 3 fields, found {len(parts)}")
                    register, date_text, status = parts
                    if not register or not date_text:
                        raise ValueError("register and date are required")
                    if status not in {"P", "A"}:
                        raise ValueError(f"invalid status {status!r}; expected P or A")
                except ValueError as exc:
                    errors.append((file_path.name, line_number, str(exc), raw_line.rstrip()))
                    continue

                counts.setdefault(register, [0, 0])
                counts[register][0 if status == "P" else 1] += 1

    percentage_rows = []
    below_rows = []
    for register in sorted(counts):
        present, absent = counts[register]
        total = present + absent
        percentage = (present / total * 100) if total else 0.0
        row = (register, present, absent, total, percentage)
        percentage_rows.append(row)
        if percentage < threshold:
            below_rows.append(row)

    with open(report_file, "w", encoding="utf-8") as target:
        target.write("MONTHLY ATTENDANCE PERCENTAGE\\n")
        target.write("register,present,absent,working_days,percentage\\n")
        for r, p, a, t, pc in percentage_rows:
            target.write(f"{r},{p},{a},{t},{pc:.2f}\\n")
        target.write("\\nSTUDENTS BELOW 75 PERCENT\\n")
        for r, p, a, t, pc in below_rows:
            target.write(f"{r},{pc:.2f}%\\n")

    with open(error_file, "w", encoding="utf-8", newline="") as target:
        writer = csv.writer(target)
        writer.writerow(["file", "line", "reason", "raw_line"])
        writer.writerows(errors)

    return percentage_rows, below_rows, errors

if __name__ == "__main__":
    root = Path(__file__).parent
    output = root / "outputs"
    output.mkdir(exist_ok=True)
    all_rows, low_rows, errors = process_month(
        root / "attendance_input",
        output / "attendance_report.txt",
        output / "damaged_lines.csv"
    )
    print("TASK 2 - MONTHLY ATTENDANCE")
    print("Attendance percentages:")
    for row in all_rows:
        print(f"{row[0]}: P={row[1]}, A={row[2]}, {row[4]:.2f}%")
    print("Below 75%:", [row[0] for row in low_rows])
    print("Damaged lines:", errors)
    print("Output files: attendance_report.txt, damaged_lines.csv")
