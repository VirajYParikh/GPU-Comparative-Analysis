import argparse

from common import run_command
from constants import PROJECT, ZONE


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cluster", type=str, help="The name of the cluster to delete", required=True
    )
    return parser.parse_args()


def main():
    args = _parse_args()
    print(f"Deleting {args.cluster} - this can take five minutes or more...")
    cli_args = [
        "gcloud",
        "beta",
        "container",
        "--project",
        PROJECT,
        "clusters",
        "delete",
        args.cluster,
        "--quiet",
        "--zone",
        ZONE,
    ]
    run_command(cli_args)


if __name__ == "__main__":
    main()
