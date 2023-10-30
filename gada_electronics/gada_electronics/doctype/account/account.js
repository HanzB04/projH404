// Copyright (c) 2023, H404 and contributors
// For license information, please see license.txt

frappe.ui.form.on('Account', {
    validate: function(frm) {
        var accountNumber = frm.doc.account_number;
        if (!/^\d+$/.test(accountNumber)) {
            frappe.msgprint(__("Account Number must contain only numbers."));
            frappe.validated = false;
        }
    }
});
