# Unfortunately, students don't have the correct scopes to use terraform in our class project, but I did
# get this working in a personal project

data "google_client_config" "default" {}

provider "kubernetes" {
  host                   = "https://${module.gke.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(module.gke.ca_certificate)
}

provider "google" {
  project = "csci-ga-3003-085-fall23-9f6d"
  region  = "us-central1"
}

resource "google_compute_network" "vpc_network" {
  name                    = "vpc-01"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "default" {
  name          = "us-central1-01"
  ip_cidr_range = "10.0.1.0/24"
  region        = "us-central1"
  network       = google_compute_network.vpc_network.id
  secondary_ip_range {
    range_name    = "us-central1-01-gke-01-pods"
    ip_cidr_range = "192.168.10.0/26"
  }
  secondary_ip_range {
    range_name    = "us-central1-01-gke-01-services"
    ip_cidr_range = "192.168.11.0/26"
  }
}

module "gke" {
  source                     = "terraform-google-modules/kubernetes-engine/google//modules/private-cluster"
  project_id                 = "csci-ga-3003-085-fall23-9f6d"
  name                       = "cameron-gke-test-1"
  region                     = "us-central1"
  zones                      = ["us-central1-a"]
  network                    = "vpc-01"
  subnetwork                 = "us-central1-01"
  ip_range_pods              = "us-central1-01-gke-01-pods"
  ip_range_services          = "us-central1-01-gke-01-services"
  http_load_balancing        = false
  network_policy             = false
  horizontal_pod_autoscaling = true
  filestore_csi_driver       = false
  enable_private_nodes       = true
  master_ipv4_cidr_block     = "172.16.0.0/28"

  #   master_authorized_networks_config {
  #   }

  #   private_cluster_config {
  #     enable_private_endpoint = true
  #     enable_private_nodes    = true
  #     master_ipv4_cidr_block  = "172.16.0.0/28"
  #   }

  node_pools = [
    {
      name               = "default-node-pool"
      machine_type       = "e2-medium"
      node_locations     = "us-central1-a"
      min_count          = 1
      max_count          = 3
      local_ssd_count    = 0
      spot               = false
      disk_size_gb       = 100
      disk_type          = "pd-standard"
      image_type         = "COS_CONTAINERD"
      enable_gcfs        = false
      enable_gvnic       = false
      logging_variant    = "DEFAULT"
      auto_repair        = true
      auto_upgrade       = true
      preemptible        = false
      initial_node_count = 3
    },
  ]

  node_pools_oauth_scopes = {
    all = [
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]
  }

  node_pools_labels = {
    all = {}

    default-node-pool = {
      default-node-pool = true
    }
  }

  node_pools_metadata = {
    all = {}

    default-node-pool = {
      node-pool-metadata-custom-value = "my-node-pool"
    }
  }

  node_pools_taints = {
    all = []

    default-node-pool = [
      {
        key    = "default-node-pool"
        value  = true
        effect = "PREFER_NO_SCHEDULE"
      },
    ]
  }

  node_pools_tags = {
    all = []

    default-node-pool = [
      "default-node-pool",
    ]
  }
}
