#!/bin/bash
gcloud beta container --project "phishdetectai" clusters create-auto "locust-cluster" --region "asia-northeast1" --release-channel "regular" --network "projects/phishdetectai/global/networks/default" --subnetwork "projects/phishdetectai/regions/asia-northeast1/subnetworks/default" --cluster-ipv4-cidr "/17" --binauthz-evaluation-mode=DISABLED
