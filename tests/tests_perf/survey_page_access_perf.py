import csv
import logging

from locust import FastHttpUser, task, SequentialTaskSet, events
from locust.exception import StopUser

logger = logging.getLogger('locust')


# all_users_spawned = Event()


def load_csv(filename):
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)


csv_data = load_csv('perf_warning_page.csv')  # Change the file path for local execution


@events.init.add_listener
def on_locust_init(environment, **kwargs):
    @environment.events.spawning_complete.add_listener
    def on_spawning_complete(**kwargs):
        logger.info(f'All users spawned. Releasing all users.')
        # all_users_spawned.set()  # Signal that all users have been spawned


class MySequentialTaskSet(SequentialTaskSet):
    def on_start(self):
        logger.info('wait self')
        self.wait()

    @task
    def survey_page_access(self):
        user_index = self.user.index
        logger.info(f'{user_index=}')
        data = csv_data[user_index % len(csv_data)]
        logger.info(f'{data=}')
        data_values = list(data.values())
        logger.info(f'{data_values=}')
        attack_url = data_values[0].split('/')[1]

        url = data_values[0]

        json = {'url': f'{url}'}
        logger.info(f'{json=}')
        with self.client.post(
            f'/api/public/verify_url_click', json=json, catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f'{json=}|{response.text=}|{response.status_code=}')
            survey_id = response.json()['data']['id']
            survey_token = response.json()['data']['survey_token']
        logger.info(f'{response=}')

        params = {'token': f'{survey_token}', 'attack_id': f'{survey_id}'}
        url = f'/api/survey/get_surveys_for_attack'
        self.client.base_url = 'https://staging.app.aironworks.com'

        with self.client.get(
            f'/{url}',
            catch_response=True,
            params=params,
            name=f'{self.client.base_url}/api/survey/get_survey',
        ) as response:
            if response.status_code != 200:
                response.failure(
                    f'{attack_url=},{response.text=},{response.status_code=}'
                )
        self.complete_task()

    def complete_task(self):
        logger.info(f'stop user {self.user.index}')
        raise StopUser()


class CustomHttpUser(FastHttpUser):
    connection_timeout = 60.0
    insecure = False
    network_timeout = 60.0
    host = 'https://staging.sd.aironworks.com'
    tasks = [MySequentialTaskSet]
    user_index = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index = CustomHttpUser.user_index
        CustomHttpUser.user_index += 1
