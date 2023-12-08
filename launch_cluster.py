import argparse
import random
import subprocess


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


def _run_command(cmd: list[str]):
    try:
        cp = subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.output}")
        raise e

    split_out = cp.stdout.decode().split("\n")
    split_err = cp.stderr.decode().split("\n")

    for line in split_out:
        print(line)

    for line in split_err:
        print(line)


def _launch_cluster(cluster_name: str, machine_type: str, a_type: str, sub: str):
    cli_args = [
        "gcloud",
        "beta",
        "container",
        "--project",
        "csci-ga-3003-085-fall23-9f6d",
        "clusters",
        "create",
        cluster_name,
        "--no-enable-basic-auth",
        "--cluster-version",
        "1.27.3-gke.100",
        "--release-channel",
        "None",
        "--machine-type",
        machine_type,
        "--accelerator",
        f"type={a_type},count=1",
        "--image-type",
        "COS_CONTAINERD",
        "--disk-type",
        "pd-balanced",
        "--disk-size",
        "100",
        "--metadata",
        "disable-legacy-endpoints=true",
        "--scopes",
        "https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append",
        "--num-nodes",
        "3",
        "--logging=SYSTEM,WORKLOAD",
        "--monitoring=SYSTEM",
        "--enable-private-nodes",
        "--master-ipv4-cidr",
        f"172.{sub}.0.0/28",
        "--enable-ip-alias",
        "--network",
        "projects/csci-ga-3003-085-fall23-9f6d/global/networks/csci-ga-3003-085-fall23-net",
        "--subnetwork",
        "projects/csci-ga-3003-085-fall23-9f6d/regions/us-central1/subnetworks/csci-ga-3003-085-fall23-subnet-02",
        "--no-enable-intra-node-visibility",
        "--default-max-pods-per-node",
        "110",
        "--security-posture=standard",
        "--workload-vulnerability-scanning=disabled",
        "--no-enable-master-authorized-networks",
        "--addons",
        "HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver",
        "--enable-autoupgrade",
        "--enable-autorepair",
        "--max-surge-upgrade",
        "1",
        "--max-unavailable-upgrade",
        "0",
        "--binauthz-evaluation-mode=DISABLED",
        "--enable-managed-prometheus",
        "--enable-shielded-nodes",
        "--node-locations",
        "us-central1-c",
        "--zone",
        "us-central1",
    ]

    print(
        f"Attempting to launch {cluster_name} - this can take five minutes or more..."
    )
    _run_command(cli_args)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--accelerator_type",
        type=str,
        required=True,
        help=f"Choose from {VALID_ACCELERATORS}",
    )
    return parser.parse_args()


def main():
    args = _parse_args()

    a_type = args.accelerator_type
    cluster_name = f"gke-gpu-{a_type}-1-cluster"

    sub = random.randint(0, 63) * 4

    machine_type: str

    if a_type == "nvidia-l4":
        machine_type = "g2-standard-12"

    if a_type == "nvidia-a100-80gb":
        machine_type = "a2-ultragpu-1g"

    if a_type == "nvidia-tesla-a100":
        machine_type = "a2-highgpu-1g"

    if a_type in [
        "nvidia-tesla-t4",
        "nvidia-tesla-v100",
        "nvidia-tesla-p4",
        "nvidia-tesla-p100",
        "nvidia-tesla-k80",
    ]:
        machine_type = "n1-highmem-8"

    if a_type not in VALID_ACCELERATORS:
        raise Exception(f"{a_type} is not a valid accelerator type")

    _launch_cluster(cluster_name, machine_type, a_type, sub)


if __name__ == "__main__":
    main()
