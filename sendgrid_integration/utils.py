import frappe
from sendgrid import SendGridAPIClient
import json
import requests

def create_list(doc,event):
    
    if doc.lead_source_id: #indicates that this list  is already existing
        return
    frappe.log_error("Called")
    settings = frappe.get_doc("SendGrid Settings")
    if settings.enabled:
        api_key = settings.get_password("api_key")
        sg = SendGridAPIClient(api_key)

        data = {
            "name": doc.name
        }
        headers = {'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'}
        url = settings.api_url + "/marketing/lists"
        
        response = requests.post(url,json=data,headers=headers)
    
        #create a send grid log
        log = create_log(response,request_data=data,resource_type="List")
        if response.status_code == 200:
            response_data = response.json()
            doc.lead_source_id = response_data["id"]
            
            log.status = "Success"
            log.api_repsonse = json.dumps(response_data,indent=4)
        else:
            log.status = "Failed"
            log.api_response = json.dumps(response.json(),indent=4)
        log.save()
        frappe.db.commit()
            
def create_log(response_object, request_data = {},resource_type=""):
    
    log = frappe.get_doc({
        'doctype': "SendGrid Log",
        "request_data" : json.dumps(request_data,indent=4),
        "resource_type" : resource_type,
        "status" : "Pending"
    })
    
    return log  
    