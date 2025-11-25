def calculate_overall_score(scorecard_metrics: dict, financial_ratios: dict):
    """
    Calculates overall score and grade based on operational and financial metrics.
    """
    score = 0
    max_score = 100
    
    # Operational Score (50%)
    op_score = 0
    
    # On-Time Delivery (25%)
    otd = scorecard_metrics.get("on_time_delivery_rate")
    if isinstance(otd, (int, float)):
        # Normalize: 100% -> 25 pts, 0% -> 0 pts
        op_score += (otd / 100) * 25
        
    # Invoice Paid Rate (25%)
    ipr = scorecard_metrics.get("invoice_paid_rate")
    if isinstance(ipr, (int, float)):
        op_score += (ipr / 100) * 25
        
    # Financial Score (50%)
    fin_score = 0
    
    # Current Ratio (15%) - Target > 1.5
    cr = financial_ratios.get("current_ratio")
    if isinstance(cr, (int, float)):
        if cr >= 1.5:
            fin_score += 15
        elif cr >= 1.0:
            fin_score += 10
        else:
            fin_score += 5
            
    # Net Margin (15%) - Target > 10%
    nm = financial_ratios.get("net_margin")
    if isinstance(nm, (int, float)):
        if nm >= 15:
            fin_score += 15
        elif nm >= 5:
            fin_score += 10
        elif nm > 0:
            fin_score += 5
            
    # Debt to Equity (20%) - Target < 2.0
    de = financial_ratios.get("debt_to_equity")
    if isinstance(de, (int, float)):
        if de <= 1.0:
            fin_score += 20
        elif de <= 2.0:
            fin_score += 10
        else:
            fin_score += 0
            
    total_score = op_score + fin_score
    
    # Determine Grade
    if total_score >= 85:
        grade = "Great"
    elif total_score >= 70:
        grade = "Good"
    elif total_score >= 50:
        grade = "Fair"
    else:
        grade = "Poor"
        
    return {
        "score": round(total_score, 1),
        "grade": grade,
        "breakdown": {
            "operational_score": round(op_score, 1),
            "financial_score": round(fin_score, 1)
        }
    }

def identify_lender_concerns(scorecard_metrics: dict, financial_ratios: dict):
    """
    Identifies red flags for lenders.
    """
    concerns = []
    
    # Operational Concerns
    otd = scorecard_metrics.get("on_time_delivery_rate")
    if isinstance(otd, (int, float)) and otd < 70:
        concerns.append(f"Low On-Time Delivery Rate ({otd}%). Risk of supply chain disruption.")
        
    ipr = scorecard_metrics.get("invoice_paid_rate")
    if isinstance(ipr, (int, float)) and ipr < 80:
        concerns.append(f"Low Invoice Paid Rate ({ipr}%). Potential cash flow or dispute issues.")
        
    # Financial Concerns
    cr = financial_ratios.get("current_ratio")
    if isinstance(cr, (int, float)) and cr < 1.0:
        concerns.append(f"Current Ratio is low ({cr}). Liquidity risk.")
        
    de = financial_ratios.get("debt_to_equity")
    if isinstance(de, (int, float)) and de > 2.5:
        concerns.append(f"High Leverage (Debt/Equity: {de}). Solvency risk.")
        
    nm = financial_ratios.get("net_margin")
    if isinstance(nm, (int, float)) and nm < 0:
        concerns.append(f"Negative Net Margin ({nm}%). Company is operating at a loss.")
        
    return concerns

def generate_rationale(grade: str, score: float, concerns: list):
    """
    Generates a text rationale for the grade.
    """
    rationale = f"Supplier is rated as {grade} (Score: {score}/100). "
    
    if grade == "Great":
        rationale += "Demonstrates strong operational performance and financial health. "
    elif grade == "Good":
        rationale += "Solid performance with minor areas for improvement. "
    elif grade == "Fair":
        rationale += "Performance is average. Several risks identified. "
    else:
        rationale += "Significant operational or financial risks detected. "
        
    if concerns:
        rationale += "Key concerns include: " + "; ".join(concerns[:2]) + "."
        
    return rationale
