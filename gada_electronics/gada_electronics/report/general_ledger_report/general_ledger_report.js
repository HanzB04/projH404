// Copyright (c) 2023, H404 and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["General Ledger Report"] = {
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
		{
			"fieldname": "party",
			"label": "Party",
			"fieldtype": "Link",
			"options": "Party",
		},
	]
};

