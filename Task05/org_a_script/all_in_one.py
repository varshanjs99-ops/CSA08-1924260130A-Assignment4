import csv
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

def main(data_file, out_dir):
    records = []
    with open(data_file, "r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row["status"] in {"P", "A"}:
                records.append(row)
    counts = defaultdict(lambda: [0, 0])
    absences = defaultdict(list)
    for row in records:
        counts[row["register"]][0 if row["status"] == "P" else 1] += 1
        if row["status"] == "A":
            absences[row["register"]].append(date.fromisoformat(row["date"]))
    percentages = {r: round(p/(p+a)*100, 2) for r,(p,a) in counts.items() if p+a}
    streaks = []
    for reg, days in absences.items():
        days = sorted(set(days))
        run = 1
        for i in range(1, len(days)):
            run = run + 1 if days[i]-days[i-1] == timedelta(days=1) else 1
            if run >= 3:
                streaks.append(reg); break
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    (out/"attendance_percentage.txt").write_text(
        "".join(f"{r}: {v:.2f}%\n" for r,v in sorted(percentages.items())), encoding="utf-8")
    (out/"absent_three_days.txt").write_text("\n".join(sorted(streaks))+"\n", encoding="utf-8")
    return percentages, sorted(streaks)

if __name__ == "__main__":
    root = Path(__file__).parent
    print(main(root/"../data/attendance.csv", root/"output"))
