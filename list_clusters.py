import argparse
import shlex
import subprocess


def main():
    parser = argparse.ArgumentParser(prog="list_clusters")
    parser.parse_args()

    cmd = f"gcloud beta container --project csci-ga-3003-085-fall23-9f6d clusters list 2>&1 | grep gke-gpu"

    cp = subprocess.run(shlex.split(cmd), check=True, capture_output=True, shell=True)

    print("Listing clusters:\n")
    print(cp.stdout)


if __name__ == "__main__":
    main()
