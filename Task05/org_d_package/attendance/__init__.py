"""Reusable attendance-processing package."""
from .reader import read_records
from .stats import percentages, absent_three_days
from .report import write_reports

__all__ = ["read_records", "percentages", "absent_three_days", "write_reports"]
