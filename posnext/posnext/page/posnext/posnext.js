frappe.provide('posnext.PointOfSale');
frappe.pages['posnext'].on_page_load = function(wrapper) {
	frappe.ui.make_app_page({
		parent: wrapper,
		title: __('Point of Sale'),
		single_column: true
	});
	// frappe.require('pos_controller.js', function() {
		wrapper.pos = new posnext.PointOfSale.Controller(wrapper);
		window.cur_pos = wrapper.pos;
	// });
}
frappe.pages['posnext'].refresh = function(wrapper) {
	if (document.scannerDetectionData) {
		onScan.detachFrom(document);
		wrapper.pos.wrapper.html("");
		wrapper.pos.check_opening_entry();
	}
};