"""Constants for cluster operations"""

VALID_ACCELERATORS = [
    "nvidia-a100-80gb",
    "nvidia-tesla-a100",
    "nvidia-l4",
    "nvidia-tesla-t4",
    "nvidia-tesla-p4",
    "nvidia-tesla-v100",
    "nvidia-tesla-p100",
    "nvidia-tesla-k80",
]
NETWORK = (
    "projects/csci-ga-3003-085-fall23-9f6d/global/networks/csci-ga-3003-085-fall23-net"
)
SUBNETWORK = "projects/csci-ga-3003-085-fall23-9f6d/regions/us-central1/subnetworks/csci-ga-3003-085-fall23-subnet-02"
PROJECT = "csci-ga-3003-085-fall23-9f6d"
ZONE = "us-central1"
REGION = "us-central1-c"
SCOPES = "https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append"
