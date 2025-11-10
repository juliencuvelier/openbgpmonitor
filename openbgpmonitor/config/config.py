from openbgpmonitor.config.models.config_model import Config
from dotenv import load_dotenv
import os

load_dotenv()
config_dict = {
    "influxdb_url": os.getenv("INFLUXDB_URL"),
    "influxdb_token": os.getenv("INFLUXDB_TOKEN"),
    "influxdb_org": os.getenv("INFLUXDB_ORG"),
    "influxdb_bucket": os.getenv("INFLUXDB_BUCKET"),
    "probe_name": os.getenv("PROBE_NAME"),
    "local_as": 65100,
    "peer_list": [
        {"remote_ip": "192.168.122.59", "remote_as": 65001, "name": "firstpeer"},
        {"remote_ip": "192.168.122.9", "remote_as": 65002, "name": "secondpeer"},
    ],
}

CONFIG: Config = Config.model_validate(config_dict)
