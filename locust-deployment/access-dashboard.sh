#!/bin/bash
kubectl port-forward -n k6-operator-system service/grafana 5050:80
