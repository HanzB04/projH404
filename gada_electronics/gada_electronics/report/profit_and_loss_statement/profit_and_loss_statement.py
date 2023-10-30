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
			"width": 250
        },
    ]

def get_filtered_data(filters):
    filter = get_filters(filters)
    print(f"Filter: {filter}")
    filtered_data = frappe.get_all(
        doctype='GL Entry',
        fields=['account', 'debit_amount', 'credit_amount', 'is_cancelled'],
        filters=filter,
        or_filters=[
            ['account', 'like', '%Income%'],
            ['account', 'like', '%Expense%'],
        ]
    )
    print(f"Filtered Data: {filtered_data}")
    return filtered_data

def get_filters(filters):
    filter = []
    for key, value in filters.items():
        if filters.get(key):
            if key == "account":
                filter.append({key: ['like', f'{value}%']})
            if filters.get("posting_date"):
                filter.append({"posting_date": [">=", filters.get("posting_date")]})
            if filters.get("due_date"):
                filter.append({"due_date": ["<=", filters.get("due_date")]})
            if filters.get("voucher_type"):
                filter.append({"voucher_type": filters.get("voucher_type")})
            if filters.get("income_account"):
                filter.append({"account": filters.get("income_account")})

    return filter

def calculate_totals(data, filters):
    result_data = []
    total_income = 0
    total_expense = 0
    income_data = []
    expense_data = []

    for row in data:
        # Skip canceled entries
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