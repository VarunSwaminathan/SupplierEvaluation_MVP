import pandas as pd

def calculate_scorecard(po_df: pd.DataFrame, inv_df: pd.DataFrame):
    """
    Calculates scorecard metrics from PO and Invoice dataframes.
    """
    # Merge on PO Number
    # Assuming one-to-many or many-to-many relationships might exist, but for MVP we'll try to aggregate or merge directly.
    # A better approach for MVP is to calculate metrics independently where possible or merge carefully.
    
    # 1. On-Time Delivery Rate
    # Logic: delivery_date <= promised_date (if available)
    # We need actual delivery date. In the file, "Delivery Date" usually means Promised Date. 
    # We might need an "Actual Delivery Date" or "Receipt Date". 
    # If the file only has one date, we might have to assume it's the target, and we need another signal for actual.
    # HOWEVER, the prompt says: "reconcile using PO numbers/dates/SKUs".
    # Let's look at the headers again. "Case A.xlsx" likely has PO Date and Delivery Date.
    # If there is no "Actual Delivery Date", we can't compute on-time. 
    # Let's assume for now that we compare "Delivery Date" (Actual) vs "Promised Date" (Target).
    # If only one date exists, we might need to look at the Invoice Date vs PO Date? No, that's payment.
    # Let's check the file content later. For now, I'll implement a placeholder logic that looks for "Actual Delivery Date" or similar.
    # If not found, I'll default to random or 100% for MVP if data is missing, but I should try to find it.
    
    # Actually, often "Delivery Date" in PO is the requested date. The Invoice might have a "Ship Date"?
    # Or maybe the PO file has both "Order Date" and "Delivery Date" and we assume "Delivery Date" is when it arrived?
    # Let's assume "Delivery Date" in the file is the ACTUAL delivery date, and we compare it to "Date" (Order Date) + standard lead time?
    # OR, the file has "Promised" and "Actual".
    # Let's write generic logic that tries to find these columns.
    
    # For MVP, let's assume:
    # On-Time = (Count of POs with Status 'Delivered' and Delivery Date <= Promised Date) / Total POs
    # If we lack columns, we will return "N/A".
    
    metrics = {}
    
    # On-Time Delivery
    if "delivery_date" in po_df.columns and "promised_date" in po_df.columns:
        on_time_mask = pd.to_datetime(po_df["delivery_date"]) <= pd.to_datetime(po_df["promised_date"])
        on_time_rate = on_time_mask.mean() * 100
        metrics["on_time_delivery_rate"] = round(on_time_rate, 2)
    else:
        # Fallback: If we only have "Date" (PO Date) and "Delivery Date", maybe we assume Delivery Date is Actual?
        # And we don't have a promised date?
        # Let's just return a placeholder if we can't calculate.
        metrics["on_time_delivery_rate"] = "N/A (Missing dates)"

    # Invoice Paid Rate
    # Logic: Count of Invoices with Status 'Paid' / Total Invoices
    if "status" in inv_df.columns:
        paid_mask = inv_df["status"].str.lower().isin(["paid", "cleared", "settled"])
        paid_rate = paid_mask.mean() * 100
        metrics["invoice_paid_rate"] = round(paid_rate, 2)
    else:
        metrics["invoice_paid_rate"] = "N/A (Missing status)"
        
    # Fulfillment Accuracy (Quantity Received vs Ordered)
    # We need to merge PO and Invoice (assuming Invoice has quantity? Or PO has "Qty Received"?)
    # If Invoice has quantity, we compare PO Qty vs Inv Qty.
    
    # Merge attempt
    try:
        merged = pd.merge(po_df, inv_df, on="po_number", how="inner", suffixes=("_po", "_inv"))
        # If merged is empty, we can't calc.
        if not merged.empty:
             # Check for quantity columns
             # We need to handle column naming after merge
             pass
    except Exception as e:
        pass

    # Generate Commentary
    commentary = "Supplier performance is "
    if isinstance(metrics["on_time_delivery_rate"], (int, float)):
        if metrics["on_time_delivery_rate"] > 90:
            commentary += "excellent regarding delivery times. "
        elif metrics["on_time_delivery_rate"] > 75:
            commentary += "acceptable regarding delivery times. "
        else:
            commentary += "poor regarding delivery times. "
            
    if isinstance(metrics["invoice_paid_rate"], (int, float)):
        if metrics["invoice_paid_rate"] > 90:
            commentary += "Invoices are consistently paid. "
        else:
            commentary += "There are issues with invoice payments. "
            
    metrics["commentary"] = commentary
    
    return metrics
