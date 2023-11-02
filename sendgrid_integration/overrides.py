import frappe
from frappe.utils import cint, get_site_name, sanitize_html
import os
from werkzeug.exceptions import HTTPException, NotFound


_site = None
_sites_path = os.environ.get("SITES_PATH", ".")

def custom_init_request(request):
	frappe.log_error("Hello")
	frappe.local.request = request
	frappe.local.is_ajax = frappe.get_request_header("X-Requested-With") == "XMLHttpRequest"

	site = _site or request.headers.get("X-Frappe-Site-Name") or get_site_name(request.host)
	frappe.init(site=site, sites_path=_sites_path, force=True)

	if not (frappe.local.conf and frappe.local.conf.db_name):
		# site does not exist
		raise NotFound

	if frappe.local.conf.maintenance_mode:
		frappe.connect()
		if frappe.local.conf.allow_reads_during_maintenance:
			setup_read_only_mode()
		else:
			raise frappe.SessionStopped("Session Stopped")
	else:
		frappe.connect(set_admin_as_user=False)

	request.max_content_length = cint(frappe.local.conf.get("max_file_size")) or 10 * 1024 * 1024

	custom_make_form_dict(request)

	if request.method != "OPTIONS":
		frappe.local.http_request = frappe.auth.HTTPRequest()

	for before_request_task in frappe.get_hooks("before_request"):
		frappe.call(before_request_task)



def custom_make_form_dict(request):
	import json
	request_data = request.get_data(as_text=True)
	if "application/json" in (request.content_type or "") and request_data:
		args = json.loads(request_data)
	else:
		args = {}
		args.update(request.args or {})
		args.update(request.form or {})

	if isinstance(args,list):
		args = {"request_data": args} #specifically for sendgrid, which sends a list of dicts
  
	if not isinstance(args, dict):
		frappe.throw(_("Invalid request arguments"))

	frappe.local.form_dict = frappe._dict(args)

	if "_" in frappe.local.form_dict:
		# _ is passed by $.ajax so that the request is not cached by the browser. So, remove _ from form_dict
		frappe.local.form_dict.pop("_")


def setup_read_only_mode():
	"""During maintenance_mode reads to DB can still be performed to reduce downtime. This
	function sets up read only mode

	- Setting global flag so other pages, desk and database can know that we are in read only mode.
	- Setup read only database access either by:
		- Connecting to read replica if one exists
		- Or setting up read only SQL transactions.
	"""
	frappe.flags.read_only = True

	# If replica is available then just connect replica, else setup read only transaction.
	if frappe.conf.read_from_replica:
		frappe.connect_replica()
	else:
		frappe.db.begin(read_only=True)

