from datetime import date

from mini_apps.expense_tracker.storage import (
    Expense,
    append_expense,
    read_expenses,
    filter_by_month,
    summarize,
    filter_by_category,
    export_summary_csv,
    export_month_summary_csv,
)


def test_append_and_read_roundtrip(tmp_path):
    path = tmp_path / "expenses.csv"
    e1 = Expense(date(2026, 2, 12), "groceries", 45.2, "milk eggs")
    e2 = Expense(date(2026, 2, 13), "fuel", 30.0, "")

    append_expense(str(path), e1)
    append_expense(str(path), e2)

    loaded = read_expenses(str(path))
    assert loaded == [e1, e2]


def test_filter_by_month(tmp_path):
    path = tmp_path / "expenses.csv"
    append_expense(str(path), Expense(date(2026, 2, 1), "a", 10.0, ""))
    append_expense(str(path), Expense(date(2026, 3, 1), "b", 20.0, ""))

    all_exp = read_expenses(str(path))
    feb = filter_by_month(all_exp, "2026-02")
    assert len(feb) == 1
    assert feb[0].amount == 10.0


def test_summarize():
    exp = [
        Expense(date(2026, 2, 1), "groceries", 10.0, ""),
        Expense(date(2026, 2, 2), "groceries", 5.0, ""),
        Expense(date(2026, 2, 3), "fuel", 20.0, ""),
    ]
    totals = summarize(exp)
    assert totals["TOTAL"] == 35.0
    assert totals["CAT:groceries"] == 15.0
    assert totals["CAT:fuel"] == 20.0
    
    
def test_filter_by_category_case_insensitive():
    exp = [
        Expense(date(2026, 2, 1), "Groceries", 10.0, ""),
        Expense(date(2026, 2, 2), "fuel", 20.0, ""),
        Expense(date(2026, 2, 3), "GROCERIES", 5.0, ""),
    ]
    out = filter_by_category(exp, "  groceries  ")
    assert out == [exp[0], exp[2]]


def test_export_summary_csv(tmp_path):
    exp = [
        Expense(date(2026, 2, 1), "groceries", 10.0, ""),
        Expense(date(2026, 2, 2), "groceries", 5.5, ""),
        Expense(date(2026, 2, 3), "fuel", 20.0, ""),
    ]
    totals = summarize(exp)

    out = tmp_path / "summary.csv"
    export_summary_csv(str(out), totals)

    lines = out.read_text(encoding="utf-8").strip().splitlines()
    assert lines[0] == "key,value"
    # sorted keys => CAT:fuel, CAT:groceries, TOTAL
    assert lines[1] == "CAT:fuel,20.00"
    assert lines[2] == "CAT:groceries,15.50"
    assert lines[3] == "TOTAL,35.50"


def test_export_month_summary_csv(tmp_path):
    exp = [
        Expense(date(2026, 2, 1), "groceries", 10.0, ""),
        Expense(date(2026, 2, 2), "fuel", 20.0, ""),
        Expense(date(2026, 3, 1), "groceries", 30.0, ""),
    ]

    out = tmp_path / "feb_summary.csv"
    export_month_summary_csv(str(out), exp, "2026-02")

    content = out.read_text(encoding="utf-8")
    assert "TOTAL,30.00" in content
    assert "CAT:groceries,10.00" in content
    assert "CAT:fuel,20.00" in content
