#!/bin/bash
kubectl delete configmap scripts-and-dataset-cm 
kubectl delete configmap scripts-and-dataset-cm2

kubectl create configmap scripts-and-dataset-cm --from-file=confirm_education_content_perf.js --from-file=education_content_perf.js --from-file=perf_education_campaign.json
kubectl create configmap scripts-and-dataset-cm2 --from-file=survey_page_access_perf.js --from-file=survey_page_submission_perf.js --from-file=warning_page_perf.js --from-file=perf_warning_page.json