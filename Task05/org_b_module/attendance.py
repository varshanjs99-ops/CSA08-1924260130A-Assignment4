import csv
from pathlib import Path

def read_records(path):
    records = []
    with open(path, "r", encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        for row in reader:
            if row["status"] not in {"P", "A"}:
                continue
            records.append({
                "register": row["register"].strip(),
                "name": row["name"].strip(),
                "date": row["date"].strip(),
                "status": row["status"].strip()
            })
    return records

from collections import defaultdict
from datetime import date, timedelta

def percentages(records):
    totals = defaultdict(lambda: [0, 0])
    for row in records:
        totals[row["register"]][0 if row["status"] == "P" else 1] += 1
    return {
        reg: round(present / (present + absent) * 100, 2)
        for reg, (present, absent) in totals.items() if present + absent
    }

def absent_three_days(records):
    dates_by_student = defaultdict(list)
    for row in records:
        if row["status"] == "A":
            dates_by_student[row["register"]].append(date.fromisoformat(row["date"]))
    result = []
    for reg, days in dates_by_student.items():
        days = sorted(set(days))
        streak = 1
        for i in range(1, len(days)):
            streak = streak + 1 if days[i] - days[i-1] == timedelta(days=1) else 1
            if streak >= 3:
                result.append(reg)
                break
    return sorted(result)

from pathlib import Path

def write_reports(percentages, streaks, out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "attendance_percentage.txt").write_text(
        "".join(f"{reg}: {pct:.2f}%\n" for reg, pct in sorted(percentages.items())),
        encoding="utf-8"
    )
    (out / "absent_three_days.txt").write_text(
        "\n".join(streaks) + ("\n" if streaks else ""), encoding="utf-8"
    )

def run(data_file, out_dir):
    rows = read_records(data_file)
    pct = percentages(rows)
    streaks = absent_three_days(rows)
    write_reports(pct, streaks, out_dir)
    return pct, streaks
