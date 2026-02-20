from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
import csv


@dataclass(frozen=True)
class Expense:
    spent_on: date
    category: str
    amount: float
    note: str = ""


HEADER = ["spent_on", "category", "amount", "note"]


def ensure_csv(path: str) -> None:
    """Create the CSV file with header if it doesn't exist."""
    p = Path(path)
    if p.exists():
        return
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)


def append_expense(path: str, expense: Expense) -> None:
    """Append one expense row to CSV."""
    ensure_csv(path)
    with Path(path).open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                expense.spent_on.isoformat(),
                expense.category.strip(),
                f"{expense.amount:.2f}",
                expense.note.strip(),
            ]
        )


def read_expenses(path: str) -> list[Expense]:
    """Read all expenses from CSV. If file doesn't exist, return empty list."""
    p = Path(path)
    if not p.exists():
        return []

    out: list[Expense] = []
    with p.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            out.append(
                Expense(
                    spent_on=date.fromisoformat(row["spent_on"]),
                    category=row["category"],
                    amount=float(row["amount"]),
                    note=row.get("note", "") or "",
                )
            )
    return out


def filter_by_month(expenses: list[Expense], yyyy_mm: str) -> list[Expense]:
    """Filter expenses for a month string like '2026-02'."""
    if len(yyyy_mm) != 7 or yyyy_mm[4] != "-":
        raise ValueError("Month must be in YYYY-MM format, e.g., 2026-02")
    year = int(yyyy_mm[:4])
    month = int(yyyy_mm[5:7])
    return [e for e in expenses if e.spent_on.year == year and e.spent_on.month == month]


def summarize(expenses: list[Expense]) -> dict[str, float]:
    """
    Return totals:
      - total
      - per category totals
    Keys:
      'TOTAL' and 'CAT:<category>'
    """
    totals: dict[str, float] = {"TOTAL": 0.0}
    for e in expenses:
        totals["TOTAL"] += e.amount
        key = f"CAT:{e.category}"
        totals[key] = totals.get(key, 0.0) + e.amount
    return totals
