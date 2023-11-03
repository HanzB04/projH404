# Copyright (c) 2023, H404 and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    col = get_col()
    data = filtered_data(filters)

    if not data:
        frappe.msgprint("There is no record found")
        return col, data

    return col, data

def get_col():
    return [
        {
            "fieldname": "posting_date",
            "label": "Posting Date",
            "fieldtype": "Date",
        },
        {
            "fieldname": "due_date",
            "label": "Due Date",
            "fieldtype": "Date",
        },
        {
            "fieldname": "account",
            "label": "Account",
            "fieldtype": "Link",
            "options": "Account",
        },
        {
            "fieldname": "debit_amount",
            "label": "Debit Amount",
            "fieldtype": "Currency",
            "options": "currency:PHP"
        },
        {
            "fieldname": "credit_amount",
            "label": "Credit Amount",
            "fieldtype": "Currency",
            "options": "currency:PHP"
        },
        {
            "fieldname": "voucher_type",
            "label": "Voucher Type",
            "fieldtype": "Dynamic Link",
            "options": "voucher_type",
            "width": 120,
        },
        {
            "fieldname": "voucher_number",
            "label": "Voucher Number",
            "fieldtype": "Dynamic Link",
            "options": "voucher_type",
        },
        {
            "fieldname": "party",
            "label": "Party",
            "fieldtype": "Data",
        },
    ]

def filtered_data(filters):
    filter_conditions = get_filter(filters)
    data = frappe.get_all(
        doctype='GL Entry',
        fields=['posting_date', 'due_date', 'account', 'debit_amount', 'credit_amount', 'voucher_type', 'voucher_number', 'party'],
        filters=filter_conditions
    )

    if not data:
        return []

    data = [entry for entry in data if not entry.get('is_cancelled')]
    return data

def get_filter(filters):
    filter_conditions = {}

    if filters.get("posting_date") and filters.get("end_date"):
        filter_conditions["posting_date"] = ['between', [filters['posting_date'], filters['end_date']]]
    elif filters.get("posting_date"):
        filter_conditions["posting_date"] = ['>=', filters['posting_date']]

    for key, value in filters.items():
        if value and key in ["party", "account"]:
            filter_conditions[key] = ['like', f'{value}%']

    return filter_conditions
