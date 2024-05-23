import csv
import logging

from gevent.event import Event
from locust import FastHttpUser, task, SequentialTaskSet, events
from locust.exception import StopUser

from src.configs.config_loader import AppConfigs

logger = logging.getLogger("locust")

all_users_spawned = Event()


@events.init.add_listener
def on_locust_init(environment, **kwargs):
    @environment.events.spawning_complete.add_listener
    def on_spawning_complete(**kwargs):
        logger.info(f"All users spawned. Releasing all users.")
        all_users_spawned.set()  # Signal that all users have been spawned


def load_csv(filename):
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)


csv_data = load_csv("tests/resources/perf_education_campaign.csv")


class MySequentialTaskSet(SequentialTaskSet):
    def on_start(self):
        self.user_data = csv_data[self.user.index % len(csv_data)]
        logger.info("wait self")
        self.wait()

    @task
    def get_education_assignment(self):
        user_index = self.user.index
        logger.info(f"user_index = {user_index}")
        logger.info(f"user_data = {self.user_data}")
        email = self.user_data["email"]
        assignment_id = self.user_data["id"]
        token = self.user_data["token"]

        response = self.client.get(f"/api/education/assignment/{assignment_id}",
                                   params={"email": email, "token": token},
                                   name="/api/education/assignment/{education_id}")

        logger.info(response.json())
        self.complete_task()

    def complete_task(self):
        self.user.task_index += 1
        if self.user.task_index >= len(self.tasks):
            logger.info(f"stop user {self.user.index}")
            raise StopUser()

    def stop(self):
        # Check if all tasks have been completed
        if self.user.task_index >= len(self.tasks):
            self.user.environment.runner.quit()


class CustomHttpUser(FastHttpUser):
    connection_timeout = 60.0
    insecure = False
    network_timeout = 60.0
    host = AppConfigs.BASE_URL
    tasks = [MySequentialTaskSet]
    user_index = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_index = 0
        self.index = CustomHttpUser.user_index
        CustomHttpUser.user_index += 1
