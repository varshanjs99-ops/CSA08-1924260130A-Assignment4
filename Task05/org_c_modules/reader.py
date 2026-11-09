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
