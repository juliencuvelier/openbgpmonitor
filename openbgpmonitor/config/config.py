from openbgpmonitor.config.models.config_model import Config

config_dict = {
    "local_as": 65100,
    "peer_list": [
        {"remote_ip": "192.168.122.59", "remote_as": 65001, "name": "firstpeer"},
        {"remote_ip": "192.168.122.9", "remote_as": 65002, "name": "secondpeer"},
    ],
}

CONFIG: Config = Config.model_validate(config_dict)
