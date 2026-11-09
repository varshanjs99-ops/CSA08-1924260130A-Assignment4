from pathlib import Path
from reader import read_records
from stats import percentages, absent_three_days
from report import write_reports

def run(data_file, out_dir):
    rows = read_records(data_file)
    pct = percentages(rows)
    streaks = absent_three_days(rows)
    write_reports(pct, streaks, out_dir)
    return pct, streaks

if __name__ == "__main__":
    root = Path(__file__).parent
    print(run(root/"../data/attendance.csv", root/"output"))
