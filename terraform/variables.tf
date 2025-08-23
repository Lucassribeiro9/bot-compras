variable "tenancy_ocid" { type = string }
variable "compartment_id" { type = string }
variable "user_ocid" { type = string }
variable "api_fingerprint" { type = string }
variable "api_private_key_content" {
    type = string
    default = null
    sensitive = true
}
variable "api_private_key_path" {
    type = string
    default = null
}
variable "region" { type = string }
