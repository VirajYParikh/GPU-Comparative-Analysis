# cloud-ml-final-project

## Creating a cluster

```bash
# Replace nvidia-l4 with the accelerator you want to use
$ python3 launch_cluster.py --accelerator_type nvidia-l4
Attempting to launch gke-gpu-nvidia-l4-1-cluster - this can take five minutes or more...
NAME                         LOCATION     MASTER_VERSION  MASTER_IP       MACHINE_TYPE   NODE_VERSION    NUM_NODES  STATUS
gke-gpu-nvidia-l4-1-cluster  us-central1  1.27.3-gke.100  104.155.162.86  g2-standard-4  1.27.3-gke.100  3          RUNNING

Note: The Pod address range limits the maximum size of the cluster. Please refer to https://cloud.google.com/kubernetes-engine/docs/how-to/flexible-pod-cidr to learn how to optimize IP address allocation.
Note: Machines with GPUs have certain limitations which may affect your workflow. Learn more at https://cloud.google.com/kubernetes-engine/docs/how-to/gpus
Creating cluster gke-gpu-nvidia-l4-1-cluster in us-central1............done.
Created [https://container.googleapis.com/v1beta1/projects/csci-ga-3003-085-fall23-9f6d/zones/us-central1/clusters/gke-gpu-nvidia-l4-1-cluster].
To inspect the contents of your cluster, go to: https://console.cloud.google.com/kubernetes/workload_/gcloud/us-central1/gke-gpu-nvidia-l4-1-cluster?project=csci-ga-3003-085-fall23-9f6d
kubeconfig entry generated for gke-gpu-nvidia-l4-1-cluster.
```

## Deleting a cluster

```bash
# Replace gke-gpu-nvidia-tesla-k80-1-cluster with the name of the cluster you want to delete
$ python3 delete_cluster.py --cluster gke-gpu-nvidia-l4-1-cluster
Deleting gke-gpu-nvidia-l4-1-cluster - this can take five minutes or more...

Deleting cluster gke-gpu-nvidia-l4-1-cluster.........done.
Deleted [https://container.googleapis.com/v1beta1/projects/csci-ga-3003-085-fall23-9f6d/zones/us-central1/clusters/gke-gpu-nvidia-l4-1-cluster].
```

## Get credentials for a cluster

```bash
# Replace gke-gpu-nvidia-tesla-k80-1-cluster with the name of a newly created cluster
$ gcloud container clusters get-credentials gke-gpu-nvidia-tesla-k80-1-cluster --region us-central1 --project csci-ga-3003-085-fall23-9f6d
Fetching cluster endpoint and auth data.
kubeconfig entry generated for gke-gpu-nvidia-tesla-k80-1-cluster.
```

## Install NVIDIA drivers

```bash
$ kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/master/nvidia-driver-installer/cos/daemonset-preloaded.yaml
daemonset.apps/nvidia-driver-installer created
```

## Launch a job

```bash
$ kubectl apply -f kubernetes/mnist_training_job.yaml
job.batch/mnist-training-job created
```

## Get job status

```bash
kubectl get pods
NAME                       READY   STATUS    RESTARTS   AGE
mnist-training-job-gzbs7   0/1     Pending   0          20s
```
