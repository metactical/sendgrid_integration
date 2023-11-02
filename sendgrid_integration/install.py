import frappe
import os, shutil


def after_install():
    replace_app_py()

def replace_app_py():
    """replace the default app.py in the frappe
        to fix the issue with when request data from api is not a dict 
    """
    try:
        destination_path  = frappe.utils.get_bench_path() + "/apps/frappe/frappe/app.py"
        source = frappe.utils.get_bench_path() + "/apps/sendgrid_integration/sendgrid_integration/app.py"
        shutil.copyfile(source, destination_path)
    except Exception as e:
        print(e)