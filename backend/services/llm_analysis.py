import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_lender_analysis(scorecard_metrics: dict, financial_ratios: dict, overall_score: float, grade: str):
    """
    Generates a professional lender analysis using OpenAI.
    """
    if not os.getenv("OPENAI_API_KEY"):
        return {
            "rationale": "OpenAI API Key not found. Using default rationale.",
            "risks": ["API Key missing"],
            "strengths": ["N/A"]
        }

    prompt = f"""
    You are a Senior Credit Officer at a commercial bank. Analyze the following supplier data and provide a professional credit assessment.
    
    **Supplier Grade**: {grade} (Score: {overall_score}/100)
    
    **Operational Metrics**:
    {json.dumps(scorecard_metrics, indent=2)}
    
    **Financial Ratios**:
    {json.dumps(financial_ratios, indent=2)}
    
    **Instructions**:
    1. **Rationale**: Write a concise, professional paragraph (approx. 3-4 sentences) justifying the grade. Focus on the interplay between operational reliability and financial health.
    2. **Risks**: List 2-3 specific risks for a lender (e.g., liquidity issues, supply chain reliability).
    3. **Strengths**: List 2-3 key strengths.
    
    Return the output as a JSON object with keys: "rationale", "risks" (list of strings), "strengths" (list of strings).
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o", # Or gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are a helpful financial analyst assistant."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        return json.loads(content)
        
    except Exception as e:
        return {
            "rationale": f"Error generating analysis: {str(e)}",
            "risks": ["LLM Error"],
            "strengths": ["N/A"]
        }

def extract_financials_with_llm(text: str):
    """
    Uses LLM to extract financial data from raw text when regex fails.
    """
    if not os.getenv("OPENAI_API_KEY"):
        return {}
        
    prompt = f"""
    Extract the following financial metrics from the text below. Return a JSON object with keys: 
    "revenue", "net_income", "total_assets", "total_liabilities", "current_assets", "current_liabilities", "inventory", "equity".
    
    If a value is not found, use null. Return ONLY the JSON.
    
    **Text**:
    {text[:4000]} # Truncate to avoid token limits if needed
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a data extraction assistant. Extract financial numbers accurately."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"LLM Extraction Error: {e}")
        return {}
