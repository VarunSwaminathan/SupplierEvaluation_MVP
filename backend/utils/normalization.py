
def normalize_columns(df, file_type="po"):
    """
    Normalizes dataframe columns based on file type.
    """
    df.columns = df.columns.str.strip().str.lower()
    
    column_map = {}
    
    if file_type == "po":
        column_map = {
            "po number": "po_number",
            "po #": "po_number",
            "order number": "po_number",
            "date": "date",
            "order date": "date",
            "sku": "sku",
            "item": "sku",
            "quantity": "quantity",
            "qty": "quantity",
            "delivery date": "delivery_date",
            "promised date": "delivery_date",
            "vendor": "vendor",
            "supplier": "vendor",
            # Case A specific
            "oms_po_nbr": "po_number",
            "issue_date": "date",
            "must_arrive_by_date": "promised_date",
            "del_gate_in_date": "delivery_date",
            "item_id": "sku",
            "ordered_qty": "quantity"
        }
    elif file_type == "invoice":
        column_map = {
            "invoice number": "invoice_number",
            "inv #": "invoice_number",
            "po number": "po_number",
            "po #": "po_number",
            "amount": "amount",
            "total": "amount",
            "date": "date",
            "invoice date": "date",
            "status": "status",
            "payment status": "status",
            # Case A specific
            "inv_nbr": "invoice_number",
            "invoice_nbr": "invoice_number",
            "po_nbr": "po_number",
            "inv_amt": "amount",
            "invoice_amt_due": "amount",
            "inv_dt": "date",
            "invoice_date": "date",
            "inv_status": "status"
        }
        
    df = df.rename(columns=column_map)
    return df
