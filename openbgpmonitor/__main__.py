from openbgpmonitor.core.core_controller import CoreController
from openbgpmonitor.services.bgp.bird.bird import BGPPybird


def __main__():
    core_controller = CoreController(bgp_service=BGPPybird())
    core_controller.run()
