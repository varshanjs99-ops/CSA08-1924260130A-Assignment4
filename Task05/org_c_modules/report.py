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
