# Copyright (c) 2023, H404 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SalesInvoice(Document):

    @frappe.whitelist()
    def post_due(self):
        if type(self.payment_due_date) is str and type(self.posting_date) is str:
            if self.payment_due_date < self.posting_date:
                self.payment_due_date = "Today"
                return "Due date cannot be earlier than the posting date."

    def create_gl_entry(self, posting_date, due_date, party, account, debit_amount, credit_amount, voucher_type, voucher_number):
        gl = frappe.new_doc("GL Entry")
        gl.posting_date = posting_date
        gl.due_date = due_date
        gl.party = party
        gl.account = account
        gl.debit_amount = debit_amount
        gl.credit_amount = credit_amount
        gl.voucher_type = voucher_type
        gl.voucher_number = voucher_number

        gl.insert()

    def on_submit(self):
        self.create_gl_entry(
            posting_date=self.posting_date,
            due_date=self.payment_due_date,
            party=self.customer,
            account=self.debit_to, 
            debit_amount=self.total_amount,
            credit_amount=0,
            voucher_type="Sales Invoice",
            voucher_number=self.name
        )

        self.create_gl_entry(
            posting_date=self.posting_date,
            due_date=self.payment_due_date,
            party=self.customer,
            account=self.income_account,
            debit_amount=0,
            credit_amount=self.total_amount,
            voucher_type="Sales Invoice",
            voucher_number=self.name
        )

    def on_cancel(self):
        gl_entries = frappe.get_all(
            "GL Entry",
            filters={"voucher_type": "Sales Invoice", "voucher_number": self.name},
            fields=["name", "account", "debit_amount", "credit_amount"]
        )

        for entry in gl_entries:
            reverse = frappe.get_doc("GL Entry", entry.name)
            reverse.account = self.income_account if entry.account == self.debit_to else self.debit_to
            reverse.debit_amount, reverse.credit_amount = entry.credit_amount, entry.debit_amount
            reverse.is_cancelled = 1
            reverse.flags.ignore_permissions = True
            reverse.save()

    def on_trash(self):
        self.calculate_totals()
        gl_entries = frappe.get_all(
            "GL Entry",
            filters={"voucher_type": "Sales Invoice", "voucher_number": self.name},
            fields=["name", "account", "debit_amount", "credit_amount"]
        )

        for entry in gl_entries:
            reverse = frappe.get_doc("GL Entry", entry.name)
            reverse.account = self.income_account if entry.account == self.debit_to else self.debit_to
            reverse.debit_amount, reverse.credit_amount = entry.credit_amount, entry.debit_amount
            reverse.is_cancelled = 1
            reverse.flags.ignore_permissions = True
            reverse.save()

@frappe.whitelist()
def on_trash(doc, method):
    if doc.doctype == "Sales Invoice":
        doc.calculate_totals()
        gl_entries = frappe.get_all(
            "GL Entry",
            filters={"voucher_type": "Sales Invoice", "voucher_number": doc.name},
            fields=["name", "account", "debit_amount", "credit_amount"]
        )

        for entry in gl_entries:
            reverse = frappe.get_doc("GL Entry", entry.name)
            reverse.account = doc.income_account if entry.account == doc.debit_to else doc.debit_to
            reverse.debit_amount, reverse.credit_amount = entry.credit_amount, entry.debit_amount
            reverse.is_cancelled = 1
            reverse.flags.ignore_permissions = True
            reverse.save()
