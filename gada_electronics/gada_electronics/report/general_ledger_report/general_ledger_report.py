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
            "fieldname": "account",
            "label": "Account",
            "fieldtype": "Link",
            "options": "Account",
            "width": 450
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
            "width": 120,
        },
        {
            "fieldname": "party",
            "label": "Party",
            "fieldtype": "Data",
            "width": 250
        },
        {
            "fieldname": "due_date",
            "label": "Due Date",
            "fieldtype": "Date",
        },
    ]

def filtered_data(filters):
    filter_conditions = get_filter(filters)
    data = frappe.get_all(
        doctype='GL Entry',
        fields=['posting_date', 'account', 'debit_amount', 'credit_amount', 'voucher_type', 'voucher_number', 'party', 'due_date'],
        filters=filter_conditions
    )

    data = [entry for entry in data if not entry.get('is_cancelled')]
    return data

def get_filter(filters):
    filter_conditions = {}
    
    for key, value in filters.items():
        if value:
            if key in ["party", "account"]:
                filter_conditions[key] = ['like', f'{value}%']
            elif key in ["posting_date", "due_date"]:
                filter_conditions[key] = ['>=', value]

    return filter_conditions
