from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

from mini_apps.expense_tracker.storage import (
    Expense,
    append_expense,
    read_expenses,
    filter_by_month,
    summarize,
)

DEFAULT_DATA_PATH = str(Path("mini_apps") / "expense_tracker" / "data" / "expenses.csv")


def usage() -> None:
    print(
        "Expense Tracker (CSV)\n"
        "Commands:\n"
        "  add YYYY-MM-DD category amount [note]\n"
        "  list [N]\n"
        "  summary YYYY-MM\n\n"
        "Examples:\n"
        '  py mini_apps/expense_tracker/tracker.py add 2026-02-12 groceries 45.20 "milk eggs"\n'
        "  py mini_apps/expense_tracker/tracker.py list 5\n"
        "  py mini_apps/expense_tracker/tracker.py summary 2026-02\n"
    )


def parse_amount(raw: str) -> float:
    amt = float(raw)
    if amt <= 0:
        raise ValueError("amount must be > 0")
    return amt


def cmd_add(args: list[str]) -> None:
    if len(args) < 3:
        raise ValueError("add requires: YYYY-MM-DD category amount [note]")

    spent_on = date.fromisoformat(args[0])
    category = args[1].strip()
    amount = parse_amount(args[2])
    note = " ".join(args[3:]).strip() if len(args) > 3 else ""

    if not category:
        raise ValueError("category cannot be empty")

    append_expense(DEFAULT_DATA_PATH, Expense(spent_on, category, amount, note))
    print("Added.")


def cmd_list(args: list[str]) -> None:
    n = int(args[0]) if args else 10
    if n <= 0:
        raise ValueError("N must be > 0")

    expenses = read_expenses(DEFAULT_DATA_PATH)
    if not expenses:
        print("(no expenses yet)")
        return

    # show newest first
    for e in expenses[-n:][::-1]:
        note_part = f" | {e.note}" if e.note else ""
        print(f"{e.spent_on.isoformat()} | {e.category:<12} | ${e.amount:>7.2f}{note_part}")


def cmd_summary(args: list[str]) -> None:
    if len(args) != 1:
        raise ValueError("summary requires: YYYY-MM")

    month = args[0]
    expenses = read_expenses(DEFAULT_DATA_PATH)
    month_expenses = filter_by_month(expenses, month)

    if not month_expenses:
        print(f"(no expenses for {month})")
        return

    totals = summarize(month_expenses)
    print(f"Summary for {month}")
    print(f"TOTAL: ${totals['TOTAL']:.2f}")

    # category totals
    cat_items = [(k[4:], v) for k, v in totals.items() if k.startswith("CAT:")]
    cat_items.sort(key=lambda x: (-x[1], x[0].lower()))
    for cat, total in cat_items:
        print(f"{cat:<12}: ${total:.2f}")


def main(argv: list[str]) -> int:
    if not argv:
        usage()
        return 1

    cmd = argv[0].lower()
    args = argv[1:]

    try:
        if cmd == "add":
            cmd_add(args)
        elif cmd == "list":
            cmd_list(args)
        elif cmd == "summary":
            cmd_summary(args)
        else:
            usage()
            return 1
    except Exception as e:
        print("ERROR:", e)
        usage()
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
