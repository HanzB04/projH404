// Copyright (c) 2023, H404 and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Profit and Loss Statement"] = {
    "filters": [
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
    ],
};
