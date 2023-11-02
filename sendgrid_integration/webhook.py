import frappe
from sendgrid_integration.utils import create_log
import json
@frappe.whitelist(allow_guest=True)
def handle_sendgrid(*args,**kwargs):
    if kwargs and kwargs.get("request_data"):
        email_list = kwargs.get("request_data")
        email_dict = {"email_dict":email_list}
        frappe.enqueue(process_sendgrid_event,queue="default",email_dict=email_dict)
        
        frappe.local.response['code'] = 200
        frappe.local.response['message'] = "Webhook received and processed successfully"
        
 
        
def process_sendgrid_event(email_dict:dict):
    #create a sendgrid log
    log = create_log("response",resource_type="Webhook Event")
    log.api_response = json.dumps(email_dict, indent=4)
    log.status = ""
    
    email_list = email_dict["email_dict"]
    for obj in email_list:
        #we are only interested in subscribe and unsubcribe events for now
        #check if email is exsiting in the lead source table
        if frappe.db.exists("Lead Source Table",{"contact_email":obj.get("email")}):
            if obj.get("event") == "unsubscribe":
                frappe.db.set_value("Lead Source Table", {"contact_email":obj.get("email")},"is_subscribed",0)
    log.insert(ignore_permissions=True)
    frappe.db.commit()