import argparse
import random
import subprocess
from typing import List


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


def _run_command(cmd: List[str]):
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
        PROJECT,
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
        SCOPES,
        "--num-nodes",
        "1",
        "--logging=SYSTEM,WORKLOAD",
        "--monitoring=SYSTEM",
        "--enable-private-nodes",
        "--master-ipv4-cidr",
        f"172.{sub}.0.0/28",
        "--enable-ip-alias",
        "--network",
        NETWORK,
        "--subnetwork",
        SUBNETWORK,
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
        REGION,
        "--zone",
        ZONE,
    ]

    print(
        f"Attempting to launch {cluster_name} - this can take five minutes or more..."
    )
    run_command(cli_args)


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
