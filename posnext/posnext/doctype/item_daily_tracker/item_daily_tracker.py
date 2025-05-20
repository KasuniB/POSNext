# Copyright (c) 2025, YourCompany and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ItemDailyTracker(Document):
    def validate(self):
        # Clear existing items before fetching new ones
        self.items = []
        
        if self.pos_opening_entry:
            self.fetch_reconciliation_data()
    
    def fetch_reconciliation_data(self):
        """
        Fetches data from POS Serial Validation and POS Closing Entry,
        then compares the counts for each item code
        """
        # Get all items from POS Serial Validation
        serial_items = {}
        serial_validations = frappe.get_all(
            "POS Serial Validation",
            filters={"pos_opening_entry": self.pos_opening_entry},
            fields=["name"]
        )
        
        for validation in serial_validations:
            # Get all serial numbers in this validation
            serial_details = frappe.get_all(
                "Serial Numbers Table",  # Assuming this is the child table in POS Serial Validation
                filters={"parent": validation.name},
                fields=["item_code", "item_name", "serial_no"]
            )
            
            for detail in serial_details:
                item_code = detail.item_code
                if item_code not in serial_items:
                    serial_items[item_code] = {
                        "item_name": detail.item_name,
                        "serial_count": 0,
                        "serials": []
                    }
                
                # Count only unique serial numbers
                if detail.serial_no not in serial_items[item_code]["serials"]:
                    serial_items[item_code]["serials"].append(detail.serial_no)
                    serial_items[item_code]["serial_count"] += 1
        
        # Get all items from POS Closing Entry
        invoice_items = {}
        closing_entries = frappe.get_all(
            "POS Closing Entry",
            filters={"pos_opening_entry": self.pos_opening_entry},
            fields=["name"]
        )
        
        for closing in closing_entries:
            # Get all invoices in this closing entry
            invoices = frappe.get_all(
                "POS Invoice Reference",  # Assuming this is the child table in POS Closing Entry
                filters={"parent": closing.name},
                fields=["pos_invoice"]
            )
            
            for inv in invoices:
                # Get items from each invoice
                items = frappe.get_all(
                    "POS Invoice Item",  # Assuming this is the child table in POS Invoice
                    filters={"parent": inv.pos_invoice},
                    fields=["item_code", "item_name", "qty"]
                )
                
                for item in items:
                    item_code = item.item_code
                    if item_code not in invoice_items:
                        invoice_items[item_code] = {
                            "item_name": item.item_name,
                            "invoice_count": 0
                        }
                    
                    invoice_items[item_code]["invoice_count"] += item.qty
        
        # Combine data and populate the child table
        all_item_codes = set(list(serial_items.keys()) + list(invoice_items.keys()))
        
        for item_code in all_item_codes:
            serial_count = serial_items.get(item_code, {}).get("serial_count", 0)
            invoice_count = invoice_items.get(item_code, {}).get("invoice_count", 0)
            item_name = serial_items.get(item_code, {}).get("item_name") or invoice_items.get(item_code, {}).get("item_name") or ""
            
            # Calculate difference
            difference = serial_count - invoice_count
            
            # Add to child table
            self.append("items", {
                "item_code": item_code,
                "item_name": item_name,
                "serial_count": serial_count,
                "invoice_count": invoice_count,
                "difference": difference
            })