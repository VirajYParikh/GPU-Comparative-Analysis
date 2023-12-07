import argparse
import shlex
import subprocess


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cluster", type=str, help="The name of the cluster to delete")
    return parser.parse_args()


def main():
    args = _parse_args()
    print(f"Deleting {args.cluster} - this can take five minutes or more...")
    cmd = f"gcloud beta container --project csci-ga-3003-085-fall23-9f6d clusters delete {args.cluster} --quiet --zone us-central1"
    cp = subprocess.run(shlex.split(cmd), check=True, capture_output=True)
    print(f"STDOUT: {cp.stdout}")
    print(f"STDERR: {cp.stderr}")


if __name__ == "__main__":
    main()
