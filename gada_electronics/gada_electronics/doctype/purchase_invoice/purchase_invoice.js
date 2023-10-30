// Copyright (c) 2023, H404 and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Invoice', {
	// refresh: function(frm) {

	// }
	posting_date: function(frm){
		frm.call(
			{
				doc: frm.doc,
				method: 'post_due',
				always: function (response) {
					if(response.message != undefined){
						frappe.throw(response.message)
					}
				},
			}
		)
	},

	payment_due_date: function(frm){
		frm.call(
			{
				doc: frm.doc,
				method: 'post_due',
				always: function (response) {
					if(response.message != undefined){
						frappe.throw(response.message)
					}
				},
			}
		)
	},

    onload: function(frm){
		frm.set_query('supplier', () => {
			return {
				filters: {
					party_type: 'Supplier',
				}
			}
		})

		frm.set_query('credit_to', () => {
			return {
				filters: {
					account_type: 'Asset',
				}
			}
		})
		frm.set_query('expense_account', () => {
			return {
				filters: {
					account_type: 'Expense',
				}
			}
		})
	},
     items_table_on_form_rendered: function(frm){
	 	frm.set_value()
	 },
	    on_submit: function(frm){
		
	 }
});

frappe.ui.form.on('Sales Invoice Item', 'qty', function(frm, cdt, cdn){
    var d = locals[cdt][cdn];
    frappe.model.set_value(d.doctype, d.name, 'amount', flt(d.qty * d.rate));
});

frappe.ui.form.on('Sales Invoice Item', {
    qty: function(frm, cdt, cdn) {
        calc_amount_qty(frm);
    },
    rate: function(frm, cdt, cdn) {
        calc_amount_qty(frm);
    }
});

frappe.ui.form.on('Purchase Invoice', {
    refresh: function(frm) {
        calc_total_amount_qty(frm);
    },
    before_save: function(frm) {
        calc_total_amount_qty(frm);
    }
});

function calc_amount_qty(frm) {
    var totalAmount = 0;
    var totalQty = 0;

    $.each(frm.doc.items_table || [], function(i, item) {
        totalQty += flt(item.qty);
        totalAmount += flt(item.qty * item.rate);
    });

    frm.set_value('total_qty', totalQty);
    frm.set_value('total_amount', totalAmount);
}

function calc_total_amount_qty(frm) {
    calc_amount_qty(frm);
}
