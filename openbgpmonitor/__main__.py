from openbgpmonitor.core.core_controller import CoreController
from openbgpmonitor.services.bgp.bird.bird import BGPPybird


def main():
    core_controller = CoreController(bgp_service=BGPPybird())
    core_controller.run()


if __name__ == "__main__":
    main()
