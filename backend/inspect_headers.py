import pandas as pd
import sys

try:
    po_path = r'c:\Users\varun\Documents\ABridge_TakeHome\Case Study Financials (Dataset)\PO and Invoice Files\Case A.xlsx'
    inv_path = r'c:\Users\varun\Documents\ABridge_TakeHome\Case Study Financials (Dataset)\PO and Invoice Files\Case A INV.xlsx'
    
    print("Reading PO...")
    df_po = pd.read_excel(po_path)
    print(f"PO Headers: {df_po.columns.tolist()}")
    
    print("Reading INV...")
    df_inv = pd.read_excel(inv_path)
    print(f"INV Headers: {df_inv.columns.tolist()}")
except Exception as e:
    print(e)
