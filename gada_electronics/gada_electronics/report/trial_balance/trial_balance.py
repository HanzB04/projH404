# Copyright (c) 2023, H404 and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    col = get_col()
    data, total_balance = filtered_data(filters)

    if not data:
        frappe.msgprint("There is no record found")
        return col, data

    total_balance_row = {"account": "Total Balance", "total_debit": total_balance['total_debit'], "total_credit": total_balance['total_credit']}
    data.append(total_balance_row)

    return col, data

def get_col():
    return [
        {
            "fieldname": "account",
            "label": "Account",
            "fieldtype": "Link",
            "options": "Account",
            "width": 400
        },
        {
            "fieldname": "total_debit",
            "label": "Total Debit",
            "fieldtype": "Currency",
            "options": "currency:PHP",
			"width": 250
        },
        {
            "fieldname": "total_credit",
            "label": "Total Credit",
            "fieldtype": "Currency",
            "options": "currency:PHP",
			"width": 250
        },
    ]

def filtered_data(filters):
    filter_conditions = get_filter(filters)

    data = frappe.get_all(
        doctype='GL Entry',
        fields=['account', 'debit_amount', 'credit_amount', 'is_cancelled'],
        filters=filter_conditions
    )

    total_balance = {'total_debit': 0, 'total_credit': 0}
    account_totals = {}
    for entry in data:
        if entry.get('is_cancelled'):
            continue

        account = entry.get('account')
        debit_amount = entry.get('debit_amount') or 0
        credit_amount = entry.get('credit_amount') or 0

        if account not in account_totals:
            account_totals[account] = {'total_debit': 0, 'total_credit': 0}

        account_totals[account]['total_debit'] += debit_amount
        account_totals[account]['total_credit'] += credit_amount

    for account, totals in account_totals.items():
        total_balance['total_debit'] += totals['total_debit']
        total_balance['total_credit'] += totals['total_credit']

    return [{'account': account, **totals} for account, totals in account_totals.items()], total_balance

def get_filter(filters):
    filter_conditions = {}
    
    for key, value in filters.items():
        if value:
            if key == "account":
                filter_conditions[key] = ['like', f'{value}%']

    return filter_conditions
