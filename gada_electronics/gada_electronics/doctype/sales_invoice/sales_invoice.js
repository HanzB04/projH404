// Copyright (c) 2023, H404 and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Invoice', {
    posting_date: function(frm){
        frm.call({
            doc: frm.doc,
            method: 'post_due',
            always: function (response) {
                if(response.message != undefined){
                    frappe.throw(response.message);
                }
            },
        });
    },
    
    payment_due_date: function(frm){
        frm.call({
            doc: frm.doc,
            method: 'post_due',
            always: function (response) {
                if(response.message != undefined){
                    frappe.throw(response.message);
                }
            },
        });
    },

    onload: function(frm){
        frm.set_query('customer', () => {
            return {
                filters: {
                    party_type: 'Customer',
                }
            };
        });

        frm.set_query('debit_to', () => {
            return {
                filters: {
                    account_type: 'Asset',
                }
            };
        });

        frm.set_query('income_account', () => {
            return {
                filters: {
                    account_type: 'Income',
                }
            };
        });
    },

    on_submit: function(frm){
        
    }
});

frappe.ui.form.on('Sales Invoice Item', {
    qty: function(frm, cdt, cdn) {
        calc_amount_qty(frm);
    },
    rate: function(frm, cdt, cdn) {
        calc_amount_qty(frm);
    },
    items_table_remove: function(frm, cdt, cdn) {
        calc_total_amount_qty(frm);
    }
});

frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {
        calc_total_amount_qty(frm);
    },
    before_save: function(frm) {
        calc_total_amount_qty(frm);
    }
});

function calc_amount_qty(frm) {
    var totalAmount = 0;

    $.each(frm.doc.items_table || [], function(i, item) {
        frappe.model.set_value(item.doctype, item.name, 'amount', flt(item.qty * item.rate));
        totalAmount += flt(item.amount);
    });

    frm.set_value('total_amount', totalAmount);
}

function calc_total_amount_qty(frm) {
    var totalQty = 0;

    $.each(frm.doc.items_table || [], function(i, item) {
        totalQty += flt(item.qty);
    });

    frm.set_value('total_qty', totalQty);
    calc_amount_qty(frm);
}
