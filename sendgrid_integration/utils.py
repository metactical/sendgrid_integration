import frappe
from sendgrid import SendGridAPIClient
import json
import requests

def create_list(doc,event):
    
    if doc.lead_source_id: #indicates that this list  is already existing
        return
    settings = frappe.get_doc("SendGrid Settings")
    if settings.enabled:
        api_key = settings.get_password("api_key")

        data = {
            "name": doc.name
        }
        headers = {'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'}
        url = settings.api_url + "/marketing/lists"
        
        response = requests.post(url,json=data,headers=headers)
    
        #create a send grid log
        log = create_log(response,request_data=data,resource_type="List")
        if response.status_code == 201:
            response_data = response.json()
            doc.lead_source_id = response_data["id"]
            log.status = "Success"
            log.api_response = json.dumps(response.json(),indent=4)
            doc.save()
        else:
            log.status = "Failed"
            log.api_response = json.dumps(response.json(),indent=4)
        log.insert()

def delete_list(doc,event):
    """delete a lead souce list from send grid"""
    
    if doc.lead_source_id: #this list id
        settings = frappe.get_doc("SendGrid Settings")
        if settings.enabled:
            api_key = settings.get_password("api_key")

            data = {
                "name": doc.name
            }
            headers = {'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'}
            url = settings.api_url + "/marketing/lists/" + doc.lead_source_id 
            
            response = requests.delete(url,headers=headers)
            log = create_log(response,request_data=data,resource_type="List")
            frappe.log_error("status_code",response.status_code)
            
            if response.status_code ==204:
                
                log.status = "Success"
                log.api_response = "The delete has been accepted and is processing."
            elif response.status_code == 200:
                log.status = "Success"
                log.api_response = "The delete has been accepted and is processing."
            
            else:
                log.status = "Failed"
                log.api_response = "delete failed or list does not exist"
            log.insert()
                
            
def create_log(response_object, request_data = {},resource_type=""):
    
    log = frappe.get_doc({
        'doctype': "SendGrid Log",
        "request_data" : json.dumps(request_data,indent=4),
        "resource_type" : resource_type,
        "status" : "Pending"
    })
    
    return log  
    