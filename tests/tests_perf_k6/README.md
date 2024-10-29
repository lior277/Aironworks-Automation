How to use
#############

**Note: Be sure to check the current environment and all variables before processing, as the prepare data step will clean all employees data on the customer admin account and add new employee data**

run `pytest -vv -n 1 tests/test_perf_k6/prepare_data.py` to create data for the run

run `./upload-test.sh` (fix the script to load the perf test from the correct directory)

apply test run yaml using

```sh
kubectl apply -f <test yaml file>
```

For example

```
kubectl apply -f education_content_run.yaml
```

View the pods run 

```
kubectl get pods -w                           
```

Check the pod log

```
kubectl logs <pod-name>
```

For example:

```
kubectl logs survey-page-submission-4-6g8v5
```
