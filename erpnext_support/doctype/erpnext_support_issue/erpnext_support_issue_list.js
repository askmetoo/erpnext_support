frappe.listview_settings['ERPNext Support Issue'] = {

	onload: function() {
		frappe.route_options = {
			"status": "Open"
		};

		$(".list-sidebar").prepend(`
			<ul class="list-unstyled sidebar-menu">
				<b><u><a href="https://erpnext.com/docs/user/manual" target="_blank">${__('ERPNext User Manual')}</a></u></b>
			</ul>
		`);
	},
	primary_action: function() {
		new frappe.views.ReplyComposer({doc: {}, is_new: 1});
	}
};
