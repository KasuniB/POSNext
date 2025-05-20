// Copyright (c) 2025, YourCompany and contributors
// For license information, please see license.txt

frappe.ui.form.on('Item Daily Tracker', {
    refresh: function(frm) {
        // Add custom button to fetch data
        frm.add_custom_button(__('Fetch Data'), function() {
            // Trigger save to call validate and fetch_reconciliation_data
            frm.save();
        });
        
        // Highlight differences in the items table
        frm.fields_dict['items'].grid.wrapper.find('.grid-row').each(function(i, item) {
            var row = frm.doc.items[i];
            if (row && row.difference !== 0) {
                $(item).css('background-color', '#fff9f9');
            }
        });
    },
    
    pos_opening_entry: function(frm) {
        // When POS Opening Entry is set, fetch company and date
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
                        // Automatically trigger data fetch
                        frm.save();
                    }
                }
            });
        } else {
            // Clear fields if pos_opening_entry is unset
            frm.set_value('company', '');
            frm.set_value('date', '');
            frm.set_value('items', []);
        }
    }
});
