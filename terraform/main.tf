provider "google" {
  project = var.project_id
  region  = var.region
}

# --- Secret Manager ---

resource "google_secret_manager_secret" "xero_client_id" {
  secret_id = "XERO_CLIENT_ID"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "xero_client_secret" {
  secret_id = "XERO_CLIENT_SECRET"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "bp_sql_conn" {
  secret_id = "BP_SQL_CONNECTION_STRING"
  replication {
    auto {}
  }
}

# --- Networking ---

resource "google_vpc_access_connector" "connector" {
  name          = var.vpc_connector_name
  region        = var.region
  ip_cidr_range = var.ip_cidr_range
  network       = var.vpc_network
}

# --- Cloud Run ---

resource "google_cloud_run_v2_service" "bridge_service" {
  name     = var.service_name
  location = var.region

  template {
    containers {
      image = "gcr.io/${var.project_id}/${var.service_name}:latest"
      
      env {
        name = "XERO_CLIENT_ID"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.xero_client_id.secret_id
            version = "latest"
          }
        }
      }

      env {
        name = "XERO_CLIENT_SECRET"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.xero_client_secret.secret_id
            version = "latest"
          }
        }
      }

      env {
        name = "BP_SQL_CONNECTION_STRING"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.bp_sql_conn.secret_id
            version = "latest"
          }
        }
      }

      ports {
        container_port = 8080
      }
    }

    vpc_access {
      connector = google_vpc_access_connector.connector.id
      egress    = "ALL_TRAFFIC"
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

# --- IAM ---

resource "google_project_iam_member" "secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_cloud_run_v2_service.bridge_service.template[0].service_account}"
}
