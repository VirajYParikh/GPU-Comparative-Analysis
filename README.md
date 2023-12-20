# Comparative Performance of NVIDIA Accelerators on GKE

## Introduction:
Today, deep learning models are rapidly advancing and being used for multiple applications throughout the world. These deep learning models are trained all large datasets and have extremely complex configurations and computations owing to the number of parameters they require which are in the order of 10’s and 20’s. A simple computer with average computing power cannot handle such loads. GPU’s therefore become very important to run these models. However, GPUs are expensive and utilize a lot of energy. Not all companies can afford buying GPU’s. Bigger companies therefore make use of Cloud to provide GPU services to these companies. 

Different GPU’s have different computing powers, and have varying load capacity and therefore pricing structure. Therefore it becomes very important to understand the exact requirements of the application and choose the right GPU. This can not only help save money but also realize lower computation times and memory utilization.

## Project Idea and objective:
Our project revolved around the analysis of the performance of various NVIDIA accelerators available on GKE over different models and jobs. This comparative analysis would help us understand which accelerators are performing better over the others and whether we can observe any outlying results. We will be conducting all these tests on Google’s Cloud Console making use of the accelerators they have available for us to use.

## Implementation:
The implementation of this project required several steps:

#### Step 1:
Bringing up the Kubernetes cluster with the appropriate accelerator:
Firstly to connect to GCP, we need to install the GCP CLI:
Install the package:
```bash
brew install --cask google-cloud-sdk
```

Once gcloud is installed,  we need to login to our instance using:
```bash 
$ gcloud auth login 
```
After which we need to setup the default region and project id to connect with.

This step involved various substeps and configurations to be considered while creating the cluster. 
1. Selecting the correct accelerator
2. Configuring the correct flags
3. Ensuring the region and the project we are connecting to is correct
4. Since we were planning on repeating this task multiple times we decided to write a script which allowed us to spin up a cluster on the project and region of choice by simply passing the accelerator type in the argument of the command. 


### Creating a cluster

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

5. To now connect to the cluster we need to run the following command: 

### Get credentials for a cluster

```bash
# Replace gke-gpu-nvidia-tesla-k80-1-cluster with the name of a newly created cluster
$ gcloud container clusters get-credentials gke-gpu-nvidia-tesla-k80-1-cluster --region us-central1 --project csci-ga-3003-085-fall23-9f6d
Fetching cluster endpoint and auth data.
kubeconfig entry generated for gke-gpu-nvidia-tesla-k80-1-cluster.
```

6. Once the cluster was configured, we need to wait for its deployment on GKE, after which we need to install the drivers of the desired compatible version based on the accelerator we are running the cluster.

### Install NVIDIA drivers

```bash
$ kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/master/nvidia-driver-installer/cos/daemonset-preloaded.yaml
daemonset.apps/nvidia-driver-installer created
```

#### Step 2: 
Creating the Docker Image to install packages compatible with the NVIDIA drivers, CUDA and torch packages:

Before we deploy our job to the cluster we need to create a docker container where we can run the pod. The docker image was created using a VM we ran on Google Cloud Console. We installed docker on that VM and installed all the required images we needed with the necessary dependencies and pushed the image to docker hub from which the pod would be able to extract the image to run the Job.

#### Step 3:
Creating the Yaml file to deploy the job on the Cluster created on GKE:

After creating the image and pushing it successfully to docker hub we wrote a Yaml file for running the job inside the cluster that was created in on GKE.
We deployed a Job, with the name of the image that needed to be extracted from docker hub in the yaml file and hit the following command to deploy the job in GKE:

### Launch a job

```bash
$ kubectl apply -f kubernetes/mnist_training_job.yaml
job.batch/mnist-training-job created
```

Before we did this we ensured that we had Kubernetes installed on our machine by running:
```bash 
$ pip install kubectl
```

Once the job is deployed, a pod will be created in the cluster within which our job will run.
You can see the status of your job and pod using the following commands:
### Get job status

```bash
$ kubectl get pods
```

```bash
kubectl get pods
NAME                       READY   STATUS    RESTARTS   AGE
mnist-training-job-gzbs7   0/1     Pending   0          20s
```
To see the results of the job you can run the following command:
```bash
$ kubectl logs `pod id`
```

### Deleting a cluster

```bash
# Replace gke-gpu-nvidia-tesla-k80-1-cluster with the name of the cluster you want to delete
$ python3 delete_cluster.py --cluster gke-gpu-nvidia-l4-1-cluster
Deleting gke-gpu-nvidia-l4-1-cluster - this can take five minutes or more...

Deleting cluster gke-gpu-nvidia-l4-1-cluster.........done.
Deleted [https://container.googleapis.com/v1beta1/projects/csci-ga-3003-085-fall23-9f6d/zones/us-central1/clusters/gke-gpu-nvidia-l4-1-cluster].
```



