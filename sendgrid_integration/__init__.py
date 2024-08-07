import frappe
from sendgrid_integration.overrides import custom_init_request
import frappe.app

__version__ = '0.0.1'

frappe.app.init_request = custom_init_request