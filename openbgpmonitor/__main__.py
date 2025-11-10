from openbgpmonitor.core.core_controller import CoreController
from openbgpmonitor.services.bgp.bird.bird import BGPPybird
from openbgpmonitor.services.tsdb.influxdb.influxdb import TSDBInfluxDB


def main():
    core_controller = CoreController(
        bgp_service=BGPPybird(), tsdb_service=TSDBInfluxDB()
    )
    core_controller.run()


if __name__ == "__main__":
    main()
