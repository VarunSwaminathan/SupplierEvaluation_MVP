from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
import pandas as pd
from services.ingestion import parse_po_file, parse_invoice_file
from services.scorecard import calculate_scorecard
from fastapi.middleware.cors import CORSMiddleware
import io

app = FastAPI(title="Supplier Evaluation MVP")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "content-type", "ngrok-skip-browser-warning"],
)

@app.post("/upload/scorecard")
async def create_scorecard(
    po_files: List[UploadFile] = File(...),
    inv_files: List[UploadFile] = File(...)
):
    try:
        # Process PO Files
        po_dfs = []
        for file in po_files:
            content = await file.read()
            df = parse_po_file(content, file.filename)
            po_dfs.append(df)
        
        if po_dfs:
            full_po_df = pd.concat(po_dfs, ignore_index=True)
        else:
            raise HTTPException(status_code=400, detail="No valid PO files provided")

        # Process Invoice Files
        inv_dfs = []
        for file in inv_files:
            content = await file.read()
            df = parse_invoice_file(content, file.filename)
            inv_dfs.append(df)
            
        if inv_dfs:
            full_inv_df = pd.concat(inv_dfs, ignore_index=True)
        else:
            raise HTTPException(status_code=400, detail="No valid Invoice files provided")

        # Calculate Scorecard
        scorecard = calculate_scorecard(full_po_df, full_inv_df)
        
        return {
            "status": "success",
            "data": scorecard,
            "details": {
                "po_records": len(full_po_df),
                "inv_records": len(full_inv_df)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from services.financials import parse_financial_pdf, calculate_ratios

@app.post("/upload/financials")
async def analyze_financials(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        if not file.filename.endswith('.pdf'):
            continue
            
        content = await file.read()
        try:
            parsed_data = parse_financial_pdf(content, file.filename)
            ratios = calculate_ratios(parsed_data)
            results.append({
                "filename": file.filename,
                "parsed_data": parsed_data,
                "ratios": ratios
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e)
            })
            
    return {"status": "success", "results": results}

from services.synthesis import calculate_overall_score, identify_lender_concerns, generate_rationale

@app.post("/upload/full_evaluation")
async def full_evaluation(
    po_files: List[UploadFile] = File(...),
    inv_files: List[UploadFile] = File(...),
    financial_files: List[UploadFile] = File(...)
):
    try:
        # 1. Process PO & Invoice Files
        po_dfs = []
        for file in po_files:
            content = await file.read()
            df = parse_po_file(content, file.filename)
            po_dfs.append(df)
        full_po_df = pd.concat(po_dfs, ignore_index=True) if po_dfs else pd.DataFrame()

        inv_dfs = []
        for file in inv_files:
            content = await file.read()
            df = parse_invoice_file(content, file.filename)
            inv_dfs.append(df)
        full_inv_df = pd.concat(inv_dfs, ignore_index=True) if inv_dfs else pd.DataFrame()

        scorecard_metrics = calculate_scorecard(full_po_df, full_inv_df)

        # 2. Process Financial Files
        # For MVP, we assume one set of financials or aggregate them. 
        # Let's take the first valid financial file for ratios or average them.
        # Simplification: Use the first PDF found.
        financial_ratios = {}
        for file in financial_files:
            if file.filename.endswith('.pdf'):
                content = await file.read()
                parsed_data = parse_financial_pdf(content, file.filename)
                financial_ratios = calculate_ratios(parsed_data)
                break # Just use one for now

        # 3. Synthesis
        overall = calculate_overall_score(scorecard_metrics, financial_ratios)
        
        # Use LLM for analysis
        from services.llm_analysis import generate_lender_analysis
        analysis = generate_lender_analysis(
            scorecard_metrics, 
            financial_ratios, 
            overall["score"], 
            overall["grade"]
        )
        
        # Fallback to static concerns if LLM fails or returns empty risks
        static_concerns = identify_lender_concerns(scorecard_metrics, financial_ratios)
        final_concerns = analysis.get("risks", [])
        if not final_concerns or "LLM Error" in final_concerns:
             final_concerns = static_concerns

        return {
            "status": "success",
            "supplier_grade": overall["grade"],
            "overall_score": overall["score"],
            "rationale": analysis.get("rationale", "Analysis unavailable."),
            "lender_concerns": final_concerns,
            "strengths": analysis.get("strengths", []),
            "details": {
                "operational_metrics": scorecard_metrics,
                "financial_ratios": financial_ratios,
                "score_breakdown": overall["breakdown"]
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Supplier Evaluation API is running"}
