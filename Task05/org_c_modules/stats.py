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
