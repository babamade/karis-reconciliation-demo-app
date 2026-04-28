import os
from datetime import date
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from dotenv import load_dotenv

import database
import xero_auth

# Load environment variables
load_dotenv()

app = FastAPI(
    title="BP-Xero Cloud Bridge",
    description="Automation portal for synchronizing BP Premier data with Xero",
    version="1.0.0"
)

class SyncStatus(BaseModel):
    status: str
    message: str
    records_found: int
    records_synced: int

@app.get("/")
async def root():
    return {"message": "BP-Xero Cloud Bridge API is running"}

@app.get("/login")
async def login():
    """
    Redirect the user to Xero for authentication.
    """
    auth_url = xero_auth.get_authorization_url()
    return RedirectResponse(auth_url)

@app.get("/callback")
async def callback(request: Request):
    """
    Handle the callback from Xero and exchange the code for a token.
    """
    url = str(request.url)
    try:
        token = xero_auth.handle_callback(url)
        return {"message": "Successfully authenticated with Xero", "token_type": token.get("token_type")}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")

@app.get("/health")
async def health_check():
    # Simple check for environment variables
    bp_conn = "configured" if os.getenv("BP_SQL_CONNECTION_STRING") else "missing"
    xero_client = "configured" if os.getenv("XERO_CLIENT_ID") else "missing"
    
    return {
        "status": "healthy",
        "connections": {
            "bp_premier_config": bp_conn,
            "xero_config": xero_client,
            "vpn_status": "active (mocked)" # Real check would involve a ping to the SQL server
        }
    }

@app.post("/sync", response_model=SyncStatus)
async def trigger_sync(
    start_date: date = Query(..., description="The start date for the sync range"),
    end_date: date = Query(None, description="The end date for the sync range (defaults to start_date)")
):
    """
    Trigger a manual synchronization of paid invoices from BP Premier to Xero.
    """
    end_date = end_date or start_date
    
    if start_date > date.today():
        raise HTTPException(status_code=400, detail="Start date cannot be in the future")

    # 1. Fetch pending invoices from BP Premier
    try:
        pending_invoices = database.get_pending_invoices(start_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch invoices from BP Premier: {str(e)}")

    # 2. Check Xero Token
    # TODO: Implement token retrieval and refresh logic
    
    # 3. Perform Sync (Logic to be expanded)
    # For now, we return the count of records found
    
    return SyncStatus(
        status="success",
        message=f"Sync process completed for {start_date}",
        records_found=len(pending_invoices),
        records_synced=0  # Implementation pending Xero push logic
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
