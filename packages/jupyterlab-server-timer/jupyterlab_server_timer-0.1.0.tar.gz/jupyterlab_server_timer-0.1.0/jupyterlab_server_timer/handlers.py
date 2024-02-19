import json
import os
from datetime import datetime

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado

server_load_time = datetime.now()

SERVER_STARTUP_DELAY = 20

class RouteHandler(APIHandler):
    @tornado.web.authenticated
    def get(self):

        run_time = 3600
        if 'JOB_RUN_TIME' in os.environ and os.environ['JOB_RUN_TIME'].isdigit():
            run_time = int(os.environ['JOB_RUN_TIME']) * 60

        start_time = load_time = int(server_load_time.timestamp())
        end_time = run_time + start_time - SERVER_STARTUP_DELAY

        if 'JOB_START_TIME' in os.environ and os.environ['JOB_START_TIME'].isdigit():
            start_time = int(os.environ['JOB_START_TIME'])
            end_time = run_time + start_time

        self.finish(json.dumps({
            "comment": "Server life span.",
            "start-time": start_time,
            "load-time": load_time,
            "end-time": end_time,
            "run-time": run_time
        }))

def setup_handlers(web_app):
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "jupyterlab-server-timer", "get-life-span")
    handlers = [(route_pattern, RouteHandler)]
    web_app.add_handlers(host_pattern, handlers)
