---

# Project: BP-Xero Cloud Bridge (Web Portal)
**Version:** 2.0.0  
**Owner:** Practice Management / System Administration  
**Deployment:** Google Cloud Run (Serverless)  
**Access:** Web Browser (Authenticated via IAP)

## 1. Project Overview
A web-based automation portal designed for **Karis Medical Group** to synchronize financial data between the on-premise **BP Premier** database and **Xero**. This application provides a user-friendly dashboard to trigger syncs, monitor reconciliation health, and manage OAuth2 tokens for Xero.

## 2. Cloud Architecture

### Infrastructure (Google Cloud Platform)
* **Compute:** **Cloud Run** (Dockerized Python application).
* **Networking:** Serverless VPC Access connector to bridge the cloud environment to the on-premise BP Premier SQL server via VPN/Cloud Router.
* **Secrets:** **GCP Secret Manager** to store Xero Client IDs, Client Secrets, and SQL connection strings.
* **CI/CD:** Artifact Registry for container image management.

### Backend Stack
* **Framework:** Python 3.11+ using **FastAPI** (for high-performance async operations).
* **Database Connectivity:** `pyodbc` with the Microsoft ODBC Driver for SQL Server.
* **Xero Integration:** `xero-python` SDK with OAuth 2.0 PKCE flow.

### Frontend UI
* **Framework:** **Streamlit** (for rapid internal tool development) or **FastAPI + Jinja2/Tailwind**.
* **Features:** Real-time sync progress bars, "Sync Now" trigger button, and status tables for "Ready to Reconcile" vs "Synced."

## 3. Functional Requirements

### Dashboard Capabilities
* **Connection Status:** Visual indicators for BP Premier (VPN status) and Xero (Token validity).
* **Manual Trigger:** Ability for the Practice Manager to initiate a sync for a specific date range outside of automated schedules.
* **Data Preview:** A table showing "Paid" invoices in BP Premier that are pending upload to Xero.

### Reconciliation Logic
* **Filtering:** Only fetch invoices where `Payments.PaymentDate` is current and `Invoices.Status` = 'Paid'.
* **Deduplication:** Check Xero for existing Invoice Numbers before pushing to prevent double-entry.
* **Tracking:** Update a local metadata table (or Xero Private Note) to mark the record as `Synced_to_Xero`.

## 4. Security & Access Control
* **Authentication:** Deployment behind **Google Identity-Aware Proxy (IAP)** to ensure only authorized Karis Medical Group staff (via Google Workspace) can access the URL.
* **Data In Transit:** All traffic encrypted via HTTPS/TLS 1.3.
* **Privacy:** Ensure no sensitive clinical data (clinical notes/diagnoses) is queried; only financial transaction data and generic patient identifiers are transmitted.

## 5. Deployment Workflow
1.  **Containerization:** Build the image using a `Dockerfile` based on `python:3.11-slim`.
2.  **Secret Mapping:** Map GCP Secrets to Environment Variables in the Cloud Run configuration.
3.  **VPC Connector:** Configure the Cloud Run service to use the VPC connector to reach the Merredin-based SQL Server.
4.  **Endpoint:** Assign a custom domain or use the `.a.run.app` URL secured by IAP.

## 6. SQL Integration Logic
```sql
/* Query used by the Web App to populate the 'Pending Sync' table */
SELECT 
    i.InvoiceNumber,
    i.FullAmount,
    p.PaymentDate,
    p.PaymentType,
    dr.Surname AS DoctorName
FROM Invoices i
JOIN Payments p ON i.InvoiceID = p.InvoiceID
JOIN Providers dr ON i.ProviderID = dr.ProviderID
WHERE p.PaymentDate = :web_input_date
AND i.Status = 'Paid';
```

## 7. Immediate Action Items
* [ ] Configure **GCP Serverless VPC Access** to allow the Cloud Run instance to "see" the local PowerEdge T140 server.
* [ ] Set up a **Xero App** with the `payments`, `accounting.transactions`, and `offline_access` scopes.
* [ ] Build the initial FastAPI prototype with a single `/health` endpoint and `/sync` trigger.

---


