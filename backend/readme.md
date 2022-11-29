### SSH to TPU Instance example
gcloud compute tpus tpu-vm ssh stable-diff --zone europe-west4-a --project stable-diffusion-368310

### start service with privilaged flag example

sudo docker run  -p 8080:8080 --privileged gcr.io/stable-diffusion-368310/backend:v4
