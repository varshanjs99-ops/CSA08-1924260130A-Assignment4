"""Task 1 - Diagnose and repair a poor mess-bill file processor."""
from decimal import Decimal, InvalidOperation
from pathlib import Path
import csv
import io
import time
import tracemalloc
import tempfile

def process_mess_file(file_name):
    """Stream a CSV file and return (total, report_rows, rejected_rows)."""
    total = Decimal("0.00")
    report_rows = []
    rejected_rows = []

    with open(file_name, "r", encoding="utf-8-sig", newline="") as source:
        for line_number, raw_line in enumerate(source, start=1):
            if not raw_line.strip():
                continue
            try:
                row = next(csv.reader([raw_line], strict=True))
                if len(row) != 3:
                    raise ValueError(f"expected 3 fields, found {len(row)}")
                register, name, amount_text = (field.strip() for field in row)
                if not register or not name:
                    raise ValueError("register number and name are required")
                amount = Decimal(amount_text)
                if not amount.is_finite() or amount < 0:
                    raise ValueError("amount must be a finite non-negative value")
            except InvalidOperation:
                rejected_rows.append((line_number, raw_line.rstrip("\r\n"),
                                      "amount must be a valid decimal such as 1250.50"))
                continue
            except (csv.Error, ValueError) as exc:
                rejected_rows.append((line_number, raw_line.rstrip("\r\n"), str(exc)))
                continue

            total += amount
            report_rows.append((register, name, amount))

    return total, report_rows, rejected_rows

def write_report(rows, destination):
    """Write report lines in one joined operation."""
    lines = ["Register Number | Student Name | Amount (INR)\n"]
    lines.extend(
        f"{register} | {name} | {amount:.2f}\n"
        for register, name, amount in rows
    )
    Path(destination).write_text("".join(lines), encoding="utf-8")

def benchmark_reading(n=50_000):
    """Compare equivalent counting work and peak memory for iteration/readlines."""
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, newline="") as temp:
        temp_path = temp.name
        for i in range(n):
            temp.write(f"1924{i:06d},Student{i},1250.50\n")
    file_bytes = Path(temp_path).stat().st_size
    samples = {}
    for method in ("iteration", "readlines"):
        tracemalloc.start()
        start = time.perf_counter()
        with open(temp_path, "r", encoding="utf-8") as source:
            count = sum(1 for _ in source) if method == "iteration" else len(source.readlines())
        elapsed = time.perf_counter() - start
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        samples[method] = (elapsed, peak, count)
    Path(temp_path).unlink()
    assert samples["iteration"][2] == samples["readlines"][2] == n
    return samples["iteration"], samples["readlines"], file_bytes

if __name__ == "__main__":
    input_file = Path(__file__).with_name("mess_oct.txt")
    output_file = Path(__file__).with_name("mess_report.txt")
    total, accepted, rejected = process_mess_file(input_file)
    write_report(accepted, output_file)
    print("TASK 1 - MESS BILL PROCESSOR")
    print("Accepted records:", len(accepted))
    print("Rejected records:")
    for line_no, raw, reason in rejected:
        print(f"  line {line_no}: {raw!r} -> {reason}")
    print(f"Total mess bill: INR {total:.2f}")
    print("Report:", output_file.name)
    iteration, readlines, bytes_size = benchmark_reading()
    print(f"50,000-line reading test: iteration={iteration[0]:.6f}s, "
          f"peak={iteration[1]:,} B; readlines={readlines[0]:.6f}s, "
          f"peak={readlines[1]:,} B; file-size={bytes_size:,} bytes")
