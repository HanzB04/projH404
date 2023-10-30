# Copyright (c) 2023, H404 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PaymentEntry(Document):

    def create_gl_entry(self, posting_date, payment_type, party_type, party, account_paid_from, account_paid_to, amount):
        gl = frappe.new_doc("GL Entry")
        gl.posting_date = posting_date
        gl.party_type = party_type
        gl.party = party
        gl.account = account_paid_from
        gl.debit_amount = amount if payment_type == "Receive" else 0
        gl.credit_amount = amount if payment_type == "Pay" else 0
        gl.voucher_type = "Payment Entry"
        gl.voucher_number = self.name

        gl.insert()

        if account_paid_from != account_paid_to:
            gl = frappe.new_doc("GL Entry")
            gl.posting_date = posting_date
            gl.party_type = party_type
            gl.party = party
            gl.account = account_paid_to
            gl.debit_amount = 0 if payment_type == "Receive" else amount
            gl.credit_amount = 0 if payment_type == "Pay" else amount
            gl.voucher_type = "Payment Entry"
            gl.voucher_number = self.name

            gl.insert()

    def on_submit(self):
        self.create_gl_entry(
            posting_date=self.posting_date,
            payment_type=self.payment_type,
            party_type=self.party_type,
            party=self.party,
            account_paid_from=self.account_paid_from,
            account_paid_to=self.account_paid_to,
            amount=self.amount
        )

    def on_cancel(self):
        if self.party_type == "Customer":
            gl_entries = frappe.get_all(
                "GL Entry",
                filters={"voucher_type": "Payment Entry", "voucher_number": self.name},
                fields=["name", "account", "debit_amount", "credit_amount"]
            )

            for entry in gl_entries:
                reverse_entry = frappe.get_doc("GL Entry", entry.name)
                reverse_entry.account = self.account_paid_from
                reverse_entry.debit_amount, reverse_entry.credit_amount = entry.credit_amount, entry.debit_amount
                reverse_entry.is_cancelled = 1
                reverse_entry.flags.ignore_permissions = True
                reverse_entry.save()

        elif self.party_type == "Supplier":
            gl_entries = frappe.get_all(
                "GL Entry",
                filters={"voucher_type": "Payment Entry", "voucher_number": self.name},
                fields=["name", "account", "debit_amount", "credit_amount"]
            )

            for entry in gl_entries:
                reverse_entry = frappe.get_doc("GL Entry", entry.name)
                reverse_entry.account = self.account_paid_from
                reverse_entry.debit_amount, reverse_entry.credit_amount = entry.credit_amount, entry.debit_amount
                reverse_entry.is_cancelled = 1
                reverse_entry.flags.ignore_permissions = True
                reverse_entry.save()
