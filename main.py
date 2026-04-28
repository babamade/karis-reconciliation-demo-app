import os
from datetime import date
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from dotenv import load_dotenv

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
    records_synced: int

@app.get("/")
async def root():
    return {"message": "BP-Xero Cloud Bridge API is running"}

@app.get("/health")
async def health_check():
    # TODO: Add logic to check VPN connectivity to BP Premier and Xero Token status
    return {
        "status": "healthy",
        "connections": {
            "bp_premier": "pending_check",
            "xero": "pending_check"
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

    # TODO: Implement the actual sync logic:
    # 1. Connect to BP Premier SQL Server via VPC Connector
    # 2. Fetch paid invoices for the date range
    # 3. Authenticate with Xero
    # 4. Check for existing invoices in Xero (deduplication)
    # 5. Push new invoices to Xero
    
    return SyncStatus(
        status="success",
        message=f"Sync initiated for range: {start_date} to {end_date}",
        records_synced=0  # Placeholder
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
