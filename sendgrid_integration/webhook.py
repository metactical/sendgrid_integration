import frappe

@frappe.whitelist(allow_guest=True)
def handle_sendgrid(*args,**kwargs):
    frappe.log_error("args", args)
    
    frappe.log_error("kwargs", kwargs)