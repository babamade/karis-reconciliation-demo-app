# Project Wiki: BP-Xero Cloud Bridge

This wiki provides detailed technical documentation for the BP-Xero Cloud Bridge automation portal.

## 1. System Architecture

The application is a serverless bridge connecting a cloud-based web portal with an on-premise medical database.

### Infrastructure Components
- **Compute:** [Google Cloud Run](https://cloud.google.com/run) (Python 3.11 / FastAPI).
- **Network Bridge:** [Serverless VPC Access Connector](https://cloud.google.com/vpc/docs/configure-serverless-vpc-access) (connects Cloud Run to the on-premise SQL Server via VPN).
- **Secret Management:** [GCP Secret Manager](https://cloud.google.com/secret-manager) (stores Xero credentials and SQL connection strings).
- **Access Control:** [Google Identity-Aware Proxy (IAP)](https://cloud.google.com/iap) (ensures only authorized Karis Medical Group staff can access the UI).

## 2. Integration Logic

### BP Premier (SQL Server)
The bridge connects to the BP Premier database using `pyodbc` over the VPC connector.

**Primary Query for Reconciliation:**
```sql
SELECT 
    i.InvoiceNumber,
    i.FullAmount,
    p.PaymentDate,
    p.PaymentType,
    dr.Surname AS DoctorName
FROM Invoices i
JOIN Payments p ON i.InvoiceID = p.InvoiceID
JOIN Providers dr ON i.ProviderID = dr.ProviderID
WHERE CAST(p.PaymentDate AS DATE) = :target_date
AND i.Status = 'Paid';
```
*Note: We filter strictly for 'Paid' status to ensure only reconciled transactions are transmitted.*

### Xero (OAuth 2.0 PKCE)
The integration uses the `xero-python` SDK with the following scopes:
- `accounting.transactions`
- `payments`
- `offline_access` (for refresh tokens)

## 3. Data Flow
1. **Trigger:** User initiates a sync via the `/sync` endpoint (manual trigger).
2. **Fetch:** The Bridge queries BP Premier for all invoices paid on the selected date.
3. **Deduplication:** (Logic Pending) The Bridge checks Xero for existing invoice numbers to prevent double-entry.
4. **Push:** Validated invoices are pushed to Xero as 'Paid' transactions.
5. **Logging:** Sync status is returned to the user and (ideally) logged in a local metadata table.

## 4. Configuration & Secrets

### Environment Variables / Secrets
| Name | Source | Description |
| :--- | :--- | :--- |
| `XERO_CLIENT_ID` | Secret Manager | Xero App Client ID |
| `XERO_CLIENT_SECRET` | Secret Manager | Xero App Client Secret |
| `BP_SQL_CONNECTION_STRING` | Secret Manager | ODBC connection string for BP Premier |
| `XERO_REDIRECT_URI` | Env Variable | Callback URL (e.g., `https://[app-url]/callback`) |

## 5. Deployment Guide (Terraform)
The infrastructure is managed via Terraform in the `terraform/` directory.

1. **Initialize:** `terraform init`
2. **Plan:** `terraform plan -var="project_id=vertexaitesting-458008"`
3. **Apply:** `terraform apply`

## 6. Security Standards
- **No Clinical Data:** The bridge is hardcoded to never query clinical notes, diagnoses, or patient history.
- **Encryption:** All data in transit is encrypted via TLS 1.3 (HTTPS) and the VPC tunnel.
- **Audit:** All actions in GCP are logged via Cloud Audit Logs.

## 7. Troubleshooting
- **VPN Issues:** If the `/health` check fails for `bp_premier`, verify the VPC connector status and the on-premise VPN tunnel.
- **Token Expiry:** If Xero pushes fail, navigate to `/login` to re-authorize the application.
