import pdfplumber
import re
import io

def parse_financial_pdf(file_content: bytes, filename: str):
    """
    Parses financial data from a PDF file.
    """
    text = ""
    with pdfplumber.open(io.BytesIO(file_content)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
            
    # Extract key values using regex
    # We look for patterns like "Revenue ... 1,000,000" or "Total Assets ... 500,000"
    # This is a heuristic approach.
    
    data = {}
    
    # Define patterns for key metrics
    patterns = {
        "revenue": [r"Revenue", r"Sales", r"Total Revenue", r"Net Sales"],
        "net_income": [r"Net Income", r"Net Profit", r"Profit for the year"],
        "total_assets": [r"Total Assets"],
        "total_liabilities": [r"Total Liabilities"],
        "current_assets": [r"Total Current Assets", r"Current Assets"],
        "current_liabilities": [r"Total Current Liabilities", r"Current Liabilities"],
        "inventory": [r"Inventory", r"Inventories"],
        "equity": [r"Total Equity", r"Shareholders' Equity", r"Total Shareholders' Equity"]
    }
    
    for key, keywords in patterns.items():
        for keyword in keywords:
            # Regex to find the keyword followed by numbers at the end of the line (or near it)
            # We handle currency symbols, commas, and parentheses for negatives
            # Example: "Total Assets $ 1,234,567"
            regex = rf"{keyword}.*?([\d,]+(?:\.\d+)?)"
            match = re.search(regex, text, re.IGNORECASE)
            if match:
                value_str = match.group(1).replace(",", "")
                try:
                    data[key] = float(value_str)
                    break # Found a match for this key, stop looking
                except ValueError:
                    continue
    
    # Fallback: If critical data is missing, try LLM
    # Critical keys: revenue, net_income, total_assets, total_liabilities
    critical_keys = ["revenue", "net_income", "total_assets", "total_liabilities"]
    missing_critical = [k for k in critical_keys if k not in data]
    
    if missing_critical:
        from services.llm_analysis import extract_financials_with_llm
        print(f"Missing critical keys {missing_critical}. Attempting LLM extraction...")
        llm_data = extract_financials_with_llm(text)
        
        # Merge LLM data if not already present
        for k, v in llm_data.items():
            if k not in data and v is not None:
                data[k] = float(v) if isinstance(v, (int, float, str)) else v
                    
    return data

def calculate_ratios(data: dict):
    """
    Calculates financial ratios from parsed data.
    """
    ratios = {}
    
    # Liquidity Ratios
    if data.get("current_assets") and data.get("current_liabilities"):
        ratios["current_ratio"] = round(data["current_assets"] / data["current_liabilities"], 2)
        
        inventory = data.get("inventory", 0)
        ratios["quick_ratio"] = round((data["current_assets"] - inventory) / data["current_liabilities"], 2)
    else:
        ratios["current_ratio"] = "N/A"
        ratios["quick_ratio"] = "N/A"
        
    # Profitability Ratios
    if data.get("net_income") and data.get("revenue"):
        ratios["net_margin"] = round((data["net_income"] / data["revenue"]) * 100, 2)
    else:
        ratios["net_margin"] = "N/A"
        
    # Leverage Ratios
    if data.get("total_liabilities") and data.get("equity"):
        ratios["debt_to_equity"] = round(data["total_liabilities"] / data["equity"], 2)
    else:
        ratios["debt_to_equity"] = "N/A"
        
    return ratios
