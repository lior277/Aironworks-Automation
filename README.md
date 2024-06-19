# AironWorks Testing

## Performance Testing

### locust commandline example for local execution:

locust -f locustfile.py --headless -u 100 -r 10 -t 10m --host http://example.com --csv=results --logfile=locust.log
locust -f tests/tests_perf/education_content_perf.py --headless -u 1000 -r 100 -t 1m --host https://staging.app.aironworks.com --csv=results/results --logfile=results/locust.log

#### Here's what each flag means:

* -f locustfile.py: Specifies the Locust file to run. Replace locustfile.py with the path to your Locust file.
* --headless: Runs Locust in headless mode (without the web UI).
* -u 100: Sets the total number of users to simulate.
* -r 10: Sets the spawn rate (users per second).
* -t 10m: Sets the total duration of the test (10 minutes in this case).
* --host http://example.com: Specifies the host to load test. Replace http://example.com with the target host.
* --csv=FILENAME_PREFIX: Saves the results to CSV files with the specified prefix.
* --logfile=FILENAME: Saves log output to the specified file.
* --run-time=TIME: Specifies how long the test should run (e.g., 1h for 1 hour).