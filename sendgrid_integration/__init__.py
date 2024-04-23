
__version__ = '0.0.1'

from sendgrid_integration.overrides import custom_init_request
import frappe.app

frappe.app.init_request = custom_init_request