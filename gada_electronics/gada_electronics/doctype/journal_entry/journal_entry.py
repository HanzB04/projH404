# Copyright (c) 2023, H404 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class JournalEntry(Document):

    def create_gl_entry(self, posting_date, accounting_entries_table, description):
        for entry in accounting_entries_table:
            account = entry.get('account')
            party_type = entry.get('party_type')
            party = entry.get('party')
            debit_amount = entry.get('debit')
            credit_amount = entry.get('credit')

            if debit_amount:
                gl = frappe.new_doc("GL Entry")
                gl.posting_date = posting_date
                gl.party_type = party_type
                gl.party = party
                gl.account = account
                gl.debit_amount = debit_amount
                gl.credit_amount = 0
                gl.voucher_type = "Journal Entry"
                gl.voucher_number = self.name
                gl.insert()

            if credit_amount:
                gl = frappe.new_doc("GL Entry")
                gl.posting_date = posting_date
                gl.party_type = party_type
                gl.party = party
                gl.account = account
                gl.debit_amount = 0
                gl.credit_amount = credit_amount
                gl.voucher_type = "Journal Entry"
                gl.voucher_number = self.name
                gl.insert()

        self.description_of_transaction = description
        self.total_debit = sum(entry.get('debit', 0) for entry in accounting_entries_table)
        self.total_credit = sum(entry.get('credit', 0) for entry in accounting_entries_table)
        self.difference = self.total_debit - self.total_credit

    def on_submit(self):
        self.create_gl_entry(
            posting_date=self.posting_date,
            accounting_entries_table=self.accounting_entries_table,
            description=self.description_of_transaction
        )