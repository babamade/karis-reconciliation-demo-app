import os
import pyodbc
from datetime import date
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """
    Establishes a connection to the BP Premier SQL Server.
    Uses BP_SQL_CONNECTION_STRING from environment variables.
    """
    conn_str = os.getenv("BP_SQL_CONNECTION_STRING")
    if not conn_str:
        raise ValueError("BP_SQL_CONNECTION_STRING environment variable is not set")
    
    try:
        return pyodbc.connect(conn_str)
    except Exception as e:
        print(f"Error connecting to BP Premier: {e}")
        raise

def get_pending_invoices(target_date: date) -> List[Dict[str, Any]]:
    """
    Queries BP Premier for paid invoices on a specific date that are pending sync.
    """
    query = """
    SELECT 
        i.InvoiceNumber,
        i.FullAmount,
        p.PaymentDate,
        p.PaymentType,
        dr.Surname AS DoctorName
    FROM Invoices i
    JOIN Payments p ON i.InvoiceID = p.InvoiceID
    JOIN Providers dr ON i.ProviderID = dr.ProviderID
    WHERE CAST(p.PaymentDate AS DATE) = ?
    AND i.Status = 'Paid'
    """
    
    invoices = []
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, target_date)
                columns = [column[0] for column in cursor.description]
                for row in cursor.fetchall():
                    invoices.append(dict(zip(columns, row)))
    except Exception as e:
        print(f"Database query failed: {e}")
        # In a real app, we'd use proper logging
    
    return invoices
