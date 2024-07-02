#!/bin/bash
kubectl delete configmap scripts-cm
kubectl create configmap scripts-cm --from-file=locustfile.py=$HOME/aironworks/aironworks-testing/tests/tests_perf/warning_page_perf.py --from-file=perf_warning_page.csv=$HOME/aironworks/aironworks-testing/tests/resources/perf_warning_page.csv
