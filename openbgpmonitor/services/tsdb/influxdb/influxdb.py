from openbgpmonitor.core.ports.tsdb_interface import TSDBInterface
from openbgpmonitor.core.models.event_models import Event
from openbgpmonitor.config.config import CONFIG, Config

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


class TSDBInfluxDB(TSDBInterface):
    config: Config

    def __init__(self, config: Config = CONFIG):
        self.config = config

    def send_event(self, event: Event):
        with InfluxDBClient(
            url=self.config.influxdb_url,
            token=self.config.influxdb_token,
            org=self.config.influxdb_org,
        ) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            point = (
                Point(event.measurement)
                .tag("host", event.neighbor_name)
                .tag("event_type", event.event_type)
                .field("detail", event.details)
                .time(event.timestamp, WritePrecision.NS)
            )
            write_api.write(
                self.config.influxdb_bucket, self.config.influxdb_org, point
            )

    def send_event_list(self, event_list: list[Event]):
        with InfluxDBClient(
            url=self.config.influxdb_url,
            token=self.config.influxdb_token,
            org=self.config.influxdb_org,
        ) as client:
            formatted_events = []
            for event in event_list:
                formatted_events.append(
                    Point(event.measurement)
                    .tag("host", event.neighbor_name)
                    .tag("event_type", event.event_type)
                    .field("detail", event.details)
                    .time(event.timestamp, WritePrecision.NS)
                )
            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write(
                self.config.influxdb_bucket, self.config.influxdb_org, formatted_events
            )
