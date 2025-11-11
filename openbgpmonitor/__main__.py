from openbgpmonitor.core.core_controller import CoreController
from openbgpmonitor.services.bgp.bird.bird import BGPPybird
from openbgpmonitor.services.tsdb.influxdb.influxdb import TSDBInfluxDB
from openbgpmonitor.services.logger import get_logger

LOG = get_logger(__name__)


def main():
    core_controller = CoreController(
        bgp_service=BGPPybird(), tsdb_service=TSDBInfluxDB()
    )
    core_controller.run()


if __name__ == "__main__":
    LOG.info("starting application")
    main()
