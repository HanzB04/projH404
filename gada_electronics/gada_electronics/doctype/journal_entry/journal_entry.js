// Copyright (c) 2023, iaiaian1 and contributors
// For license information, please see license.txt

frappe.ui.form.on('Journal Entry', {
	//refresh: function(frm) {
	//},

	before_save: function(frm) {
		if (frm.doc.difference != 0) {
			frappe.throw("Debit and Credit is not balanced");
		}
	},
});

frappe.ui.form.on('Accounting Entries Table', {
	debit: function(frm, cdt, cdn) {
		updateTotals(frm);
	},

	credit: function(frm, cdt, cdn) {
		updateTotals(frm);
	},

	accounting_entries_table_remove: function(frm) {
		updateTotals(frm);
	},
});

function updateTotals(frm) {
    let debit = 0;
    let credit = 0;

    frm.doc.accounting_entries_table.forEach(element => {
        if (element.debit && !isNaN(element.debit)) {
            debit += element.debit;
        }

        if (element.credit && !isNaN(element.credit)) {
            credit += element.credit;
        }
    });

    frm.set_value('total_debit', debit);
    frm.set_value('total_credit', credit);
    frm.set_value('difference', Math.abs(credit - debit));
    frm.refresh();
}

