#!/bin/bash
kubectl delete configmap scripts-cm
kubectl create configmap scripts-cm --from-file=k8test.js
