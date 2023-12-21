# Comparative Performance of NVIDIA Accelerators on GKE

## Introduction:
Today, deep learning models are rapidly advancing and being used for multiple applications throughout the world. These deep learning models are trained all large datasets and have extremely complex configurations and computations owing to the number of parameters they require which are in the order of 10’s and 20’s. A simple computer with average computing power cannot handle such loads. GPU’s therefore become very important to run these models. However, GPUs are expensive and utilize a lot of energy. Not all companies can afford to buy GPU’s. Bigger companies therefore make use of Cloud to provide GPU services to these companies. 

Different GPUs have different computing powers and have varying load capacities and therefore pricing structures. Therefore it becomes very important to understand the exact requirements of the application and choose the right GPU. This can not only help save money but also realize lower computation times and memory utilization.

## Project Idea and objective:
Our project revolved around the analysis of the performance of various NVIDIA accelerators available on GKE over different models and jobs. This comparative analysis would help us understand which accelerators are performing better than the others and whether we can observe any outlying results. We will be conducting all these tests on Google’s Cloud Console making use of the accelerators they have available for us to use.

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
4. Since we were planning on repeating this task multiple times we decided to write a script that allowed us to spin up a cluster on the project and region of choice by simply passing the accelerator type in the argument of the command. 


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

6. Once the cluster is configured, we need to wait for its deployment on GKE, after which we need to install the drivers of the desired compatible version based on the accelerator we are running the cluster.

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

Before we move to the results, please take note of the following:
1. We ran three different architectures from the pytorch examples models:

<div align="center">
<img width="708" alt="Screenshot 2023-12-20 at 9 55 03 PM" src="https://github.com/VirajYParikh/cloud-ml-final-project/assets/67093208/14bbe19c-603f-4115-a363-a817f2c05279">
</div>

2. Following are the available accelerators on GKE on which we ran the experiments:

<div align="center">
<img width="747" alt="Screenshot 2023-12-20 at 9 55 26 PM" src="https://github.com/VirajYParikh/cloud-ml-final-project/assets/67093208/bde76958-7502-4bbf-becc-9f8871b12e19">
</div>

3. We ran each model on all the accelerators thrice to ensure consistency in the results that we obtain while running the jobs and received the following results.


## Profiling Results:

### Basic MNIST Example:
<div align="center">
<img width="793" alt="Screenshot 2023-12-20 at 10 01 25 PM" src="https://github.com/VirajYParikh/cloud-ml-final-project/assets/67093208/3e6d3a1a-7a61-490e-87a0-36cc9c1cfb8c">
</div>

<div align="center">
<img width="746" alt="Screenshot 2023-12-20 at 10 01 39 PM" src="https://github.com/VirajYParikh/cloud-ml-final-project/assets/67093208/442e6d85-b169-452a-b544-71ae9c72787c">
</div>

### GCN Example:

<div align="center">
<img width="811" alt="Screenshot 2023-12-20 at 10 19 12 PM" src="https://github.com/VirajYParikh/cloud-ml-final-project/assets/67093208/7a3871b5-1d14-4e71-b84f-5999b31d1749">
</div>

<div align="center">
<img width="827" alt="Screenshot 2023-12-20 at 10 19 26 PM" src="https://github.com/VirajYParikh/cloud-ml-final-project/assets/67093208/ed9baf07-511a-4b13-9721-910a2171c5ec">
</div>

### CIFAR-10 Example:

<div align="center">
<img width="827" alt="Screenshot 2023-12-20 at 10 20 05 PM" src="https://github.com/VirajYParikh/cloud-ml-final-project/assets/67093208/36a9c9eb-de81-406b-888f-4da7107b90f5">
</div>

<div align="center">
<img width="738" alt="Screenshot 2023-12-20 at 10 20 29 PM" src="https://github.com/VirajYParikh/cloud-ml-final-project/assets/67093208/dce13ee9-092b-45ee-b1cc-ac13bb92e04a">
</div>

### Aggregated Results:
We aggregated all the results that we achieved and focused mainly on the CUDA times to since our main objective was to perform a comparative analysis on the accelerator performances on different workloads. 

<div align="center">
<img width="685" alt="Screenshot 2023-12-20 at 10 25 48 PM" src="https://github.com/VirajYParikh/cloud-ml-final-project/assets/67093208/c52382c0-63b7-4e75-8c68-1ce551aaa439">
</div>

### Inferences:
1. The A100s are dominating given their high-performance specs. 
2. There is an interesting observation: L4 accelerators are doing better than the A100’s as well. 
3. The K80 accelerator is the least performing solution being very old and lacking sophisticated specs as the newer ones. 

Lets talk about L4 and A100:

<div align="center">
<img width="690" alt="Screenshot 2023-12-20 at 10 27 23 PM" src="https://github.com/VirajYParikh/cloud-ml-final-project/assets/67093208/565f63fe-ceaa-43b6-93fc-556ecf3db8e3">
</div>

We expected the A100 to come out at the top, however, for all the models, the L4 accelerator has performed better than its counterpart. As we compare their specs we realize the following:

1. L4 has higher number of CUDA Cores
2. L4 has higher FLOPS

Both the above reasons account for high performance. 

Now, as we know the models we consider in this project are quite simple with not much data load -  the MNIST model which is the heaviest out of all the three models has a mere 1 Million parameters. In such a case if we observe the memory bandwidth for both the accelerators, we realize that both the accelerators can easily handle such loads, with the L4 dominating in performance given the reasons mentioned above.

However, if we talk about models with much higher number of parameters and much greater loads, there would certainly be a variation in the performance with the A100 dominating L4 given their 5x more bandwidth over L4. 


### Deleting a cluster

```bash
# Replace gke-gpu-nvidia-tesla-k80-1-cluster with the name of the cluster you want to delete
$ python3 delete_cluster.py --cluster gke-gpu-nvidia-l4-1-cluster
Deleting gke-gpu-nvidia-l4-1-cluster - this can take five minutes or more...

Deleting cluster gke-gpu-nvidia-l4-1-cluster.........done.
Deleted [https://container.googleapis.com/v1beta1/projects/csci-ga-3003-085-fall23-9f6d/zones/us-central1/clusters/gke-gpu-nvidia-l4-1-cluster].
```

## Conclusion:
We were obviously expecting the A100 to come out at the top however, we were taken by surprise with the results we got where the L4 dominated. Such experiments always help open up our minds and allow us to spread validated information among the masses to help the community.

A100s today are much more expensive than all the other accelerators and are much more popular and therefore hard to get, which is probably why the L4s were introduced, essentially to handle smaller workloads faster and at a cheaper cost. 

Thus, before choosing an accelerator, one must consider all the factors we spoke about. This will allow them to use finances, energy and resources wisely.

### Challenges we faced:
1. It was really hard to initiate a cluster - there are several configurations and flags to be set to get the right cluster set for the right purpose.
2. Different accelerators required different CUDA versions and NVIDIA driver versions installed which proved to be an obstacle being completely new to this implementation.
3. Newer accelerators require CUDA >= 12 versions installed. 
4. A100s are difficult to get: Requires a combination of luck and patience.


## Links and References:
1. Source Code: https://github.com/VirajYParikh/cloud-ml-final-project
2. Final Presentation: https://docs.google.com/presentation/d/17JCuM_he77VJZz8E_83Ni4qT1sPqyecY64MVJDpffYU/edit#slide=id.p
3. Calculations: https://docs.google.com/spreadsheets/d/1o9j5yhOEjILh7YE4avyjN2AcwYXpW90jDQKMmFYVnoI/edit#gid=0
4. Models and Codes: https://github.com/pytorch/examples
5. Kubernetes Cluster Creation: https://cloud.google.com/kubernetes-engine/docs/how-to/creating-a-zonal-cluster
6. Job deployment: https://cloud.google.com/kubernetes-engine/docs/concepts/gpus
7. Cluster creation: https://youtu.be/hxpGC19PzwI?feature=shared
