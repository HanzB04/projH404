# Copyright (c) 2023, H404 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GLEntry(Document):
	#pass

	@frappe.whitelist()
	def post_due(self):
		if type(self.due_date) is str and type(self.posting_date) is str:
			if self.due_date < self.posting_date:
				self.due_date = "Today"
				return "Due date cannot be earlier than the posting date."
