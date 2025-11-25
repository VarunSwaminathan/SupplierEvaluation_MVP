import pandas as pd
from io import BytesIO
from utils.normalization import normalize_columns

def parse_po_file(file_content: bytes, filename: str) -> pd.DataFrame:
    if filename.endswith('.xlsx'):
        df = pd.read_excel(BytesIO(file_content))
    elif filename.endswith('.csv'):
        df = pd.read_csv(BytesIO(file_content))
    else:
        raise ValueError("Unsupported file format")
        
    df = normalize_columns(df, file_type="po")
    
    # Ensure required columns exist, fill missing with defaults if needed
    required_cols = ["po_number", "date", "sku", "quantity", "delivery_date"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = None # Or handle error
            
    return df

def parse_invoice_file(file_content: bytes, filename: str) -> pd.DataFrame:
    if filename.endswith('.xlsx'):
        df = pd.read_excel(BytesIO(file_content))
    elif filename.endswith('.csv'):
        df = pd.read_csv(BytesIO(file_content))
    else:
        raise ValueError("Unsupported file format")
        
    df = normalize_columns(df, file_type="invoice")
    
    # Derive status if missing but payment info exists
    if "status" not in df.columns:
        if "amount_paid" in df.columns and "amount" in df.columns:
            # If amount_paid >= amount (allowing for small float diffs), it's Paid
            df["status"] = df.apply(
                lambda x: "Paid" if pd.notnull(x["amount_paid"]) and pd.notnull(x["amount"]) and x["amount_paid"] >= x["amount"] - 0.01 else "Pending", 
                axis=1
            )
        elif "date_paid" in df.columns:
            df["status"] = df["date_paid"].apply(lambda x: "Paid" if pd.notnull(x) else "Pending")
    
    required_cols = ["invoice_number", "po_number", "amount", "date", "status"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = None
            
    return df
