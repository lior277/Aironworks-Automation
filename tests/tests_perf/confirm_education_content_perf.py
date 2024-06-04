import csv
import logging

from gevent.event import Event
from locust import FastHttpUser, task, SequentialTaskSet, events
from locust.exception import StopUser

logger = logging.getLogger("locust")

# all_users_spawned = Event()


def load_csv(filename):
    with open(filename, mode="r") as file:
        reader = csv.DictReader(file)
        return list(reader)


csv_data = load_csv(
    "perf_education_campaign.csv"
)  # Change the file path for local execution


@events.init.add_listener
def on_locust_init(environment, **kwargs):
    @environment.events.spawning_complete.add_listener
    def on_spawning_complete(**kwargs):
        logger.info(f"All users spawned. Releasing all users.")
        # all_users_spawned.set()  # Signal that all users have been spawned


class MySequentialTaskSet(SequentialTaskSet):
    def on_start(self):
        logger.info("wait self")
        self.wait()

    @task
    def get_and_submit_education_assignment(self):
        user_index = self.user.index
        logger.info(f"{user_index=}")
        data_values = list(csv_data[user_index % len(csv_data)].values())
        assignment_id = data_values[1]
        url = f"/api/education/assignment/{assignment_id}"
        param = {"email": data_values[0], "token": data_values[4]}
        with self.client.get(
            url,
            params=param,
            catch_response=True,
            name="/api/education/assignment/{education_id}",
        ) as response:
            if response.status_code != 200:
                response.failure(f"{response.text=}")

        url2 = f"/api/education/assignment/{assignment_id}/submit"
        with self.client.post(
            url2,
            json=param,
            catch_response=True,
            name="/api/education/assignment/{education_id}/submit",
        ) as response:
            if response.status_code != 200:
                response.failure(f"{response.text=}")
        self.complete_task()

    def complete_task(self):
        logger.info(f"stop user {self.user.index}")
        raise StopUser()


class CustomHttpUser(FastHttpUser):
    connection_timeout = 60.0
    insecure = False
    network_timeout = 60.0
    host = "https://staging.app.aironworks.com"
    tasks = [MySequentialTaskSet]
    user_index = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index = CustomHttpUser.user_index
        CustomHttpUser.user_index += 1
