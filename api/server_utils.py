from __future__ import unicode_literals

import frappe
import re
import base64
import json
from frappe.utils.file_manager import get_file

def get_attachments(communications):
	for comm in communications:
		frappe.db.set_value("Communication", comm.name, "seen", 1)
		comm['content'] = re.sub('src="', 'src="' + frappe.utils.get_url(), comm.get('content'))

		file_attachments = []
		if comm.get('has_attachment'):
			files = frappe.get_list("File", filters={"attached_to_doctype": "Communication", "attached_to_name": comm.get('name')})

			for d in files:
				filename, content = get_file(d.name)
				file_attachments.append({
					"filename": filename,
					"content": base64.b64encode(content).decode('ascii')
				})

		file_attachments = json.dumps(file_attachments)
		comm.update({"attachments": file_attachments})

	return communications

def set_custom_field():
	if not frappe.conf.erpnext_support_url == frappe.utils.get_url():
		return

	make_custom_field("Issue", "Bench Site", "bench_site", "Data", "Customer", 1, 0)
	make_custom_field("Issue", "Client Issue Id", "client_issue_id", "Data", "Customer", 1, 0)
	make_custom_field("Issue", "Raised via Support App", "raised_via_support_app", "Check", "Customer", 1, 0)
	make_custom_field("Issue", "Support Rating", "support_rating", "Int", "Customer", 1, 0)
	make_custom_field("Issue", "Comment", "add_a_comment", "Text", "Customer", 1, 0)
	make_custom_field("Customer", "Self Hosted Details", "self_hosted_details", "Section Break", "Customer POS id", 0, 1)
	make_custom_field("Customer", "Bench Site", "bench_site", "Data", "Self Hosted Details", 0, 0)
	make_custom_field("Customer", "Self Hosted Users", "self_hosted_users", "Int", "Bench Site", 0, 0)
	make_custom_field("Customer", "Self Hosted Expiry", "self_hosted_expiry", "Date", "Self Hosted Users", 0, 0)
	make_custom_field("Customer", "Partner", "partner", "Data", "Self Hosted Expiry", 0, 0)
	make_custom_field("Issue", "Split Issue Sync", "split_issue_sync", "Check", "Issue Split From", 1, 0)

def make_custom_field(doctype, label, fieldname, fieldtype, insert_after, read_only=0, collapsible=0):
	if not frappe.db.exists('Custom Field', '{0}-{1}'.format(doctype, fieldname)):
		custom_field_issue_bench_site = frappe.get_doc({
			'doctype': 'Custom Field',
			'dt': doctype,
			'label': label,
			'fieldname': fieldname,
			'fieldtype': fieldtype,
			'insert_after': insert_after,
			'read_only': read_only,
			'collapsible': collapsible
		}).insert(ignore_permissions=True)

def is_server():
	if frappe.utils.get_url() == frappe.conf.erpnext_support_url:
		return True

	return False

def is_new(doc):
	if doc.creation == doc.modified:
		return True

	return False

def get_hash_for_client(bench_site):
	import hashlib
	digest = hashlib.sha224((bench_site + frappe.conf.erpnext_support_url + frappe.conf.erpnext_support_user).encode()).hexdigest()
	return digest[:8]