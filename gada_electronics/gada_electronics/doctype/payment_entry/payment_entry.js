// Copyright (c) 2023, H404 and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Entry', {
    onload: function(frm) {
        setInitialValues(frm);

        applyPaymentTypeFilters(frm);

        frm.fields_dict['party_type'].df.onchange = function() {
            setInitialValues(frm);
            applyPaymentTypeFilters(frm);
        };

        frm.fields_dict['payment_type'].df.onchange = function() {
            applyPaymentTypeFilters(frm);
        };
    }
});

function setInitialValues(frm) {
    const partyType = frm.doc.party_type;
    if (partyType === 'Customer') {
        frm.set_value('payment_type', 'Receive');
        frm.set_value('party', '');
        frm.set_query('party', function() {
            return {
                filters: {
                    'party_type': 'Customer',
                }
            };
        });
    } else if (partyType === 'Supplier') {
        frm.set_value('payment_type', 'Pay');
        frm.set_value('party', '');
        frm.set_query('party', function() {
            return {
                filters: {
                    'party_type': 'Supplier',
                }
            };
        });
    } else {
        frm.set_value('payment_type', '');
        frm.set_value('party', '');
        frm.set_query('party', function() {
            return {
                filters: {
                    'party_type': ''
                }
            };
        });
    }
}

function applyPaymentTypeFilters(frm) {
    const paymentType = frm.doc.payment_type;

    if (paymentType === 'Receive') {
        frm.set_query('account_paid_from', function() {
            return {
                filters: {
                    'account_type': 'Asset',
                }
            };
        });

        frm.set_query('account_paid_to', function() {
            return {
                filters: {
                    'account_type': 'Income',
                }
            };
        });
    } else if (paymentType === 'Pay') {
        frm.set_query('account_paid_from', function() {
            return {
                filters: {
                    'account_type': 'Asset',
                }
            };
        });

        frm.set_query('account_paid_to', function() {
            return {
                filters: {
                    'account_type': 'Liability',
                }
            };
        });
    } else {
        frm.set_value('account_paid_from', '');
        frm.set_value('account_paid_to', '');
    }
}
