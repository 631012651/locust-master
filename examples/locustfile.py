

import gevent
from locust import HttpUser, task, between
from locust.env import Environment
from locust.stats import stats_printer
from locust.log import setup_logging

setup_logging("INFO", None)


class User(HttpUser):
    wait_time = between(1, 3)
    host = "https://docs.locust.io"

    @task
    def my_task(self):
        self.client.get("/")

    @task
    def task_404(self):
        self.client.get("/non-existing-path")

# setup Environment and Runner
env = Environment(user_classes=[User])
env.create_local_runner()

# start a WebUI instance
env.create_web_ui("127.0.0.1", 8089)

# start a greenlet that periodically outputs the current stats
gevent.spawn(stats_printer(env.stats))

# start the test
env.runner.start(1, hatch_rate=10)

# in 60 seconds stop the runner
gevent.spawn_later(60, lambda: env.runner.quit())

# wait for the greenlets
env.runner.greenlet.join()

# stop the web server for good measures
env.web_ui.stop()

'''
import random
from locust import HttpUser, task, between
from locust import events

class QuickstartUser(HttpUser):
    wait_time = between(5, 9)

    @task
    def index_page(self):
        self.client.get("/hello")
        self.client.get("/world")

    @task(3)
    def view_item(self):
        item_id = random.randint(1, 10000)
        self.client.get(f"/item?id={item_id}", name="/item")

    def on_start(self):
        self.client.post("/login", {"username":"foo", "password":"bar"})

    @events.init.add_listener
    def on_locust_init(web_ui, **kw):
        @web_ui.app.route("/added_page")
        def my_added_page():
            return "Another page"
'''