// Copyright (c) 2023, H404 and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Profit and Loss Statement"] = {
    "filters": [
        {
            "fieldname": "posting_date",
            "label": "Start Date",
            "fieldtype": "Date",
        },
        {
            "fieldname": "end_date",
            "label": "End Date",
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
