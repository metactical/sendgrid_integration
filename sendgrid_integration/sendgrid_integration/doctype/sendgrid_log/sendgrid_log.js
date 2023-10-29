// Copyright (c) 2023, Nigmacorp and contributors
// For license information, please see license.txt

frappe.ui.form.on('SendGrid Log', {
	refresh: function(frm) {
		frm.add_custom_button('Retry', () => {
			if (frm.doc.status == "Failed"){
				frappe.confirm('This will attempt to find a retry api action using the request data',
			  ()=>{
				  frappe.call({
					  method:"sendgrid_integration.utils.retry_log",
					  args:{
						  "resource_type":frm.doc.resource_type,
						  "request_data" : frm.doc.request_data
					  },
					  freeze:true,
					  freeze_message: __("Retrying..."),
					  callback:(r)=>{
						  console.log(r)
						if (r.message){
							frm.set_value("api_response",r.message.api_response)
							frm.set_value("status",r.message.status)
							frm.save()
							frm.refresh_fields()

						}  
						 
					  }
				  })
			  },
			  ()=>{
				  console.log('Do nothing')
			  })
			}			
			
			
			 
			 
		}, );
	}
});
