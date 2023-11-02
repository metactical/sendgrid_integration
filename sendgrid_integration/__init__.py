
__version__ = '0.0.1'

from sendgrid_integration.overrides import custom_init_request,custom_make_form_dict

from frappe.app import init_request , make_form_dict


make_form_dict = custom_make_form_dict
# if __name__ == '__main__':
#     init_request = custom_init_request