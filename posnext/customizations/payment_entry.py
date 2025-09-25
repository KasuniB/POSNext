import frappe

def update_banked_amount(doc, method):
    # Find the Chief Cashier Closing Entry that references this Payment Entry
    chief_entry = frappe.db.get_value("Chief Cashier Closing Entry", {"name": doc.custom_cashier_pos_closing_entry})

    if chief_entry:
        # Calculate banked and unbanked amounts
        banked_amount = frappe.db.sql("""
            SELECT IFNULL(SUM(pe.paid_amount), 0)
            FROM `tabPayment Entry` pe
            WHERE pe.docstatus = 1
              AND pe.payment_type = 'Internal Transfer'
              AND pe.custom_cashier_pos_closing_entry = %s
        """, (chief_entry,))[0][0]

        total_amount = frappe.db.get_value("Chief Cashier Closing Entry", chief_entry, "total_amount") or 0
        unbanked_amount = total_amount - banked_amount

        # Update the Chief Cashier Closing Entry
        frappe.db.set_value("Chief Cashier Closing Entry", chief_entry, {
            "banked_amount": banked_amount,
            "unbanked_amount": unbanked_amount
        })

        # Optionally log for debugging
        frappe.logger("payment_entry").info(f"Updated Chief Cashier Closing Entry: {chief_entry} | Banked: {banked_amount} | Unbanked: {unbanked_amount}")