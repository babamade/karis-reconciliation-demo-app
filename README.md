# BP-Xero Cloud Bridge (Web Portal)

## Overview
The **BP-Xero Cloud Bridge** is a web-based automation portal designed for **Karis Medical Group**. it facilitates the synchronization of financial data between the on-premise **BP Premier** SQL database and **Xero** accounting software. 

The application provides a centralized dashboard for Practice Managers to trigger manual syncs, monitor reconciliation health, and manage OAuth2 tokens for Xero integration.

## Key Features
- **Dashboard:** Real-time visibility into connection status (BP Premier VPN & Xero Token).
- **Manual Sync:** Trigger data synchronization for specific date ranges.
- **Data Preview:** Preview pending invoices before they are pushed to Xero.
- **Deduplication:** Automated checks to prevent duplicate entries in Xero.
- **Secure Access:** Protected by Google Identity-Aware Proxy (IAP).

## Architecture
The system is built on Google Cloud Platform (GCP) and bridges cloud services with on-premise infrastructure.

- **Frontend/Backend:** Python 3.11+ using FastAPI.
- **Database:** Microsoft SQL Server (BP Premier) accessed via Serverless VPC Access.
- **Integration:** `xero-python` SDK for Xero API interaction.
- **Security:** GCP Secret Manager for credentials; IAP for user authentication.

## Tech Stack
- **Language:** [Python 3.11+](https://www.python.org/)
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) / [Streamlit](https://streamlit.io/)
- **DB Driver:** `pyodbc` with Microsoft ODBC Driver for SQL Server
- **API SDK:** `xero-python`
- **Cloud:** Google Cloud Run, Secret Manager, VPC Access Connector

## Getting Started

### Prerequisites
- Python 3.11 or higher
- Microsoft ODBC Driver 17/18 for SQL Server
- GCP Project with Secret Manager and VPC Access configured
- Xero Developer Account and App credentials

### Local Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/babamade/karis-reconciliation-demo-app.git
   cd karis-reconciliation-demo-app
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file with the following keys:
   - `XERO_CLIENT_ID`
   - `XERO_CLIENT_SECRET`
   - `BP_SQL_CONNECTION_STRING`
   - `GCP_PROJECT_ID`

## Deployment
This application is designed to be deployed on **Google Cloud Run**.

1. **Build the container:**
   ```bash
   gcloud builds submit --tag gcr.io/[PROJECT_ID]/bp-xero-bridge
   ```

2. **Deploy to Cloud Run:**
   ```bash
   gcloud run deploy bp-xero-bridge \
     --image gcr.io/[PROJECT_ID]/bp-xero-bridge \
     --vpc-connector [CONNECTOR_NAME] \
     --allow-unauthenticated=false
   ```

## Security & Privacy
- **Identity-Aware Proxy:** All access is restricted to authorized Google Workspace users.
- **Data Privacy:** Only financial transaction data is synced. No clinical notes or sensitive patient health records are queried.

## License
Confidential - For use by Karis Medical Group only.
