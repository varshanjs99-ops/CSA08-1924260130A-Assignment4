# SIMATS Python Programming - Assignment 4
## Robust Data Processing with Files, Exceptions, Modules and Packages (CO4)

**Student:** Varshan J S  
**Register number:** 1924260130A  
**Institution:** SIMATS Engineering  
**Python reported in the student's VS Code:** Python 3.14.2  
**Dependencies:** Python standard library only.

## Project structure

- `Task01/` - Diagnose and repair the poor mess-bill script; sample input, Decimal-based processor and report.
- `Task02/` - Monthly biometric attendance processor, daily sample files, combined attendance report and damaged-line CSV.
- `Task03/` - `InvalidRecord` and `AttendanceFileError`, specific exception handling, exception chaining and broad-except misuse experiment.
- `Task04/` - Reproduce the library log defects, append-mode repair, newline handling and error log.
- `Task05/` - Four versions of the same utility: one script, one imported module, three modules and an `attendance` package.
- `Task06/` - College fest package with `reader.py`, `validator.py`, `processor.py`, five department input files and generated event reports.
- `evidence/` - Console run outputs, attendance reports, event participant CSVs and error logs.

## Run commands

Run from the project root in PowerShell:

```powershell
py Task01/task01_mess_bills.py
py Task02/task02_attendance.py
py Task03/task03_exceptions.py
py Task04/task04_file_forensics.py
py Task05/org_a_script/all_in_one.py
py Task05/org_b_module/main.py
py Task05/org_c_modules/main.py
py Task05/org_d_package/main.py
py Task06/main.py
py Task06/test_missing_department.py
```

No `pip install` is required.

## Input formats

- Task 1: `register_number,student_name,amount` (CSV-style; decimal amounts supported).
- Task 2: one daily `.txt` file per date, each line `register_number,YYYY-MM-DD,P_or_A`.
- Task 4: one returned book title per line in each daily input file.
- Task 5: `attendance.csv` with `register,name,date,status` columns.
- Task 6: `register|name|department|email|event1;event2`; department file names are `cse.txt`, `ece.txt`, `eee.txt`, `mech.txt`, `civil.txt`.

## Outputs

- Task 1: `Task01/mess_report.txt`.
- Task 2: `Task02/outputs/attendance_report.txt` and `Task02/outputs/damaged_lines.csv`.
- Task 4: cumulative return log and error log from its temporary demonstration.
- Task 5: each architecture writes attendance percentages and three-day absence reports in its own `output/` folder.
- Task 6: master CSV, one event CSV per event, summary report and `error.log` in `Task06/outputs/`.

## Notes on measurements

The report's Task 1 benchmark was generated with Python 3.13.5 on Linux x86_64. The student's VS Code terminal previously reported Python 3.14.2 on Windows. Timings are machine-dependent; rerun the programs locally and use local measurements for the viva.

## GitHub submission

Create a separate public repository named `CSA08-1924260130A-Assignment4` (or private with faculty added as collaborator). Commit `Task01` through `Task06` progressively, then commit the report, README, sample inputs and evidence. Add the repository URL to the report cover and README after creating the repository.

## Viva preparation

Be ready to explain context managers, line-by-line iteration, Decimal currency parsing, file modes `r/w/a`, specific and custom exceptions, exception chaining, dictionary aggregation, package imports, `__name__ == "__main__"`, duplicate detection and safe handling of damaged records.
