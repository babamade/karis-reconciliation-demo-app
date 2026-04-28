variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region for deployment"
  type        = string
  default     = "australia-southeast1"
}

variable "service_name" {
  description = "The name of the Cloud Run service"
  type        = string
  default     = "bp-xero-bridge"
}

variable "vpc_connector_name" {
  description = "The name of the Serverless VPC Access connector"
  type        = string
  default     = "bp-vpc-connector"
}

variable "vpc_network" {
  description = "The VPC network name to connect to"
  type        = string
  default     = "default"
}

variable "ip_cidr_range" {
  description = "The IP range for the VPC connector"
  type        = string
  default     = "10.8.0.0/28"
}
