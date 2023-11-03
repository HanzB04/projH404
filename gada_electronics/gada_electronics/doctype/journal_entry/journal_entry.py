# Copyright (c) 2023, Your Name and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class JournalEntry(Document):
    
    def before_save(self):
        for accounting_ent in self.accounting_entries_table:
            self.create_gl_entry(accounting_ent)

    def create_gl_entry(self, accounting_ent):
        gl = frappe.new_doc('GL Entry')
        gl.posting_date = self.posting_date
        gl.party = accounting_ent.party
        gl.account = accounting_ent.account
        gl.debit_amount = accounting_ent.debit
        gl.credit_amount = accounting_ent.credit
        gl.voucher_type = "Journal Entry"
        gl.voucher_number = self.name + " - " + accounting_ent.account

        gl.insert()

    def on_cancel(self):
        for accounting_ent in self.accounting_entries_table:
            voucher_number = self.name + " - " + accounting_ent.account
            gl_entries = frappe.get_all('GL Entry', filters={'voucher_number': voucher_number}, fields=['name'])
            
            for gl_entry in gl_entries:
                frappe.db.set_value('GL Entry', gl_entry.name, 'is_cancelled', 1)
