# pos_serial_validation.py (Server-side code)
import frappe
from frappe import _
from frappe.model.document import Document

class POSSerialValidation(Document):
    def validate(self):
        self.validate_pos_opening_entry()
        self.validate_unique_serial_numbers()
    
    def validate_pos_opening_entry(self):
        """Validate that the selected POS Opening Entry is pending"""
        if self.pos_opening_entry:
            pos_status = frappe.db.get_value("POS Opening Entry", self.pos_opening_entry, "status")
            if pos_status != "Open":
                frappe.throw(_("Selected POS Opening Entry must be in 'Open' status"))
    
    def validate_unique_serial_numbers(self):
        """Ensure serial numbers are unique in the table"""
        serial_numbers = []
        for row in self.serial_numbers:
            if row.serial_no in serial_numbers:
                frappe.throw(_("Serial Number {0} is entered multiple times").format(row.serial_no))
            serial_numbers.append(row.serial_no)