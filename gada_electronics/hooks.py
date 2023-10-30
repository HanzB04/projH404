from . import __version__ as app_version

app_name = "gada_electronics"
app_title = "Gada Electronics"
app_publisher = "H404"
app_description = "We sell electronic products"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "gada.electronics@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/gada_electronics/css/gada_electronics.css"
# app_include_js = "/assets/gada_electronics/js/gada_electronics.js"

# include js, css files in header of web template
# web_include_css = "/assets/gada_electronics/css/gada_electronics.css"
# web_include_js = "/assets/gada_electronics/js/gada_electronics.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "gada_electronics/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "gada_electronics.install.before_install"
# after_install = "gada_electronics.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "gada_electronics.uninstall.before_uninstall"
# after_uninstall = "gada_electronics.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "gada_electronics.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"gada_electronics.tasks.all"
#	],
#	"daily": [
#		"gada_electronics.tasks.daily"
#	],
#	"hourly": [
#		"gada_electronics.tasks.hourly"
#	],
#	"weekly": [
#		"gada_electronics.tasks.weekly"
#	]
#	"monthly": [
#		"gada_electronics.tasks.monthly"
#	]
# }

# Testing
# -------

# before_tests = "gada_electronics.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "gada_electronics.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "gada_electronics.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Request Events
# ----------------
# before_request = ["gada_electronics.utils.before_request"]
# after_request = ["gada_electronics.utils.after_request"]

# Job Events
# ----------
# before_job = ["gada_electronics.utils.before_job"]
# after_job = ["gada_electronics.utils.after_job"]

# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"gada_electronics.auth.validate"
# ]
