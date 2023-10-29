import frappe
import requests , json

def update_logs():
    """update logs for send grid api that are asynchronous"""
    frappe.enqueue(update_log, queue='long', timeout=600)  # timeout is optional
    

def update_log():
    
    logs = frappe.get_all("SendGrid Log",{"status":"Processing"},["name","job_id"])
    settings = frappe.get_doc("SendGrid Settings")
    if settings.enabled:
        api_key = settings.get_password("api_key")

        headers = {'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'}
        if logs:
            for log in logs:
                url = "https://api.sendgrid.com/v3/marketing/contacts/imports/"  + log.get("job_id")
                r = requests.get(url,headers=headers)
                if r.status_code == 200:
                    response_data = json.dumps(r.json(), indent=4)
                    frappe.db.set_value("SendGrid Log",log.get("name"),"job_response",response_data)
                    frappe.db.set_value("SendGrid Log",log.get("name"),"status","Success")
                    
                else:
                    response_data = json.dumps(r.json(), indent=4)
                    frappe.db.set_value("SendGrid Log",log.get("name"),"status","Success")
                    frappe.db.set_value("SendGrid Log",log.get("name"),"job_response",response_data)  
                frappe.db.commit()
        
        