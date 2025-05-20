// Copyright (c) 2025, YourCompany and contributors
// For license information, please see license.txt

frappe.ui.form.on('Item Daily Tracker', {
    refresh: function(frm) {
        // Add custom buttons
        frm.add_custom_button(__('Fetch Data'), function() {
            frm.save();
        });
        
        // Highlight differences in the table
        frm.fields_dict['items'].grid.wrapper.find('.grid-row').each(function(i, item) {
            var difference = frm.doc.items[i].difference;
            if (difference !== 0) {
                $(item).find('.grid-row-check').parent().css('background-color', '#fff9f9');
            }
        });
    },
    
    pos_opening_entry: function(frm) {
        // If POS Opening Entry is set, get related company
        if (frm.doc.pos_opening_entry) {
            frappe.call({
                method: 'frappe.client.get_value',
                args: {
                    doctype: 'POS Opening Entry',
                    filters: {
                        name: frm.doc.pos_opening_entry
                    },
                    fieldname: ['company', 'period_start_date']
                },
                callback: function(response) {
                    var data = response.message;
                    if (data) {
                        frm.set_value('company', data.company);
                        frm.set_value('date', data.period_start_date);
                    }
                }
            });
        }
    }
});