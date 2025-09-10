# main.tf

terraform {
  required_providers {
    oci = {
      source  = "oracle/oci"
      version = "~> 5.0"
    }
  }
}

provider "oci" {
  tenancy_ocid     = var.tenancy_ocid
  user_ocid        = var.user_ocid
  fingerprint      = var.api_fingerprint
  private_key      = var.api_private_key_content != null ? var.api_private_key_content : file(var.api_private_key_path)
  region           = var.region
}


data "oci_identity_availability_domains" "ads" {
  compartment_id = var.tenancy_ocid
}

data "oci_core_images" "ubuntu_image" {
  compartment_id           = var.compartment_id
  operating_system         = "Canonical Ubuntu"
  operating_system_version = "22.04"
  shape                    = "VM.Standard.E2.1.Micro"
  sort_by                  = "TIMECREATED"
  sort_order               = "DESC"
}


resource "oci_core_vcn" "bot_compras_vcn_tf" {
  compartment_id = var.compartment_id
  display_name   = "bot-compras-vcn"
  cidr_block     = "10.0.0.0/16"
}

# security list
resource "oci_core_security_list" "bot_security_list" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_vcn.bot_compras_vcn_tf.id
  display_name   = "bot-security-list"
  # Regras de entrada
  ingress_security_rules {
    protocol = "6"   #TCP
    source   = "0.0.0.0/0"
    tcp_options {
      min = 22
      max = 22  
    }    
  }
  egress_security_rules {
    protocol = "all"
    destination = "0.0.0.0/0"
  }
}

resource "oci_core_subnet" "bot_compras_subnet_tf" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_vcn.bot_compras_vcn_tf.id
  display_name   = "bot-compras-subnet"
  cidr_block     = "10.0.1.0/24"
  security_list_ids = [oci_core_security_list.bot_security_list.id]
}


resource "oci_core_instance" "bot_compras_instance_tf" {
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
  compartment_id      = var.compartment_id
  display_name        = "bot-compras-instance-tf"
  shape               = "VM.Standard.E2.1.Micro"
  
  source_details {
    source_type = "image"
    source_id   = data.oci_core_images.ubuntu_image.images[0].id
  }   

  create_vnic_details {
    subnet_id = oci_core_subnet.bot_compras_subnet_tf.id
  }
}