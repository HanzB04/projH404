# Copyright (c) 2023, H404 and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()
    data = get_filtered_data(filters)
    calculate_totals(data, filters)

    if not data:
        frappe.msgprint("There is no record found")
        return columns, data

    return columns, data

def get_columns():
    return [
        {
            "fieldname": "account",
            "label": "Account",
            "fieldtype": "Dynamic Link",
            "options": "Chart of Accounts",
            "width": 400
        },
        {
            "fieldname": "amount",
            "label": "Amount",
            "fieldtype": "Currency",
            "options": "currency",
        },
    ]

def get_filtered_data(filters):
    filter_conditions = get_filters(filters)
    print(f"Filter Conditions: {filter_conditions}")

    filtered_data = frappe.get_all(
        doctype='GL Entry',
        fields=['account', 'debit_amount', 'credit_amount', 'is_cancelled'],
        filters=filter_conditions,
        or_filters=[
            ['account', 'like', '%Income%'],
            ['account', 'like', '%Expense%'],
        ]
    )
    print(f"Filtered Data: {filtered_data}")
    return filtered_data

def get_filters(filters):
    filter_conditions = []

    for key, value in filters.items():
        if value:
            if key == "account":
                filter_conditions.append(['account', 'like', f'{value}%'])
            elif key == "posting_date":
                filter_conditions.append(['posting_date', 'between', [filters.get("posting_date"), filters.get("end_date")]])

    return filter_conditions

def calculate_totals(data, filters):
    result_data = []
    total_income = 0
    total_expense = 0
    income_data = []
    expense_data = []

    for row in data:
        if row.get("is_cancelled"):
            continue

        amount = row.get("debit_amount", 0) + row.get("credit_amount", 0)

        if 'Income' in row.get("account", "") and amount != 0:
            total_income += amount
            income_data.append({"account": row["account"], "amount": amount, "type": None})
        elif 'Expense' in row.get("account", "") and amount != 0:
            total_expense += amount
            expense_data.append({"account": row["account"], "amount": amount, "type": None})

    total_profit_loss_amount = total_income - total_expense

    result_data.append({"account": "------Total Income", "amount": total_income, "type": "Credit"} if total_income != 0 else "")
    result_data.extend(income_data)
    result_data.append({"account": "----------------------------------------------------------------", "amount": None})
    result_data.append({"account": "------Total Expense", "amount": total_expense, "type": "Debit"} if total_expense != 0 else "")
    result_data.extend(expense_data)
    result_data.append({"account": "------Total Profit", "amount": total_profit_loss_amount, "type": None})

    data.clear()
    data.extend(result_data)
