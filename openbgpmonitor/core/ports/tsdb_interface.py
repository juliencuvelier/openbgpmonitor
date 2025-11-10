from abc import ABC
from openbgpmonitor.core.models.event_models import Event


class TSDBInterface(ABC):
    def send_event(self, event: Event):
        raise NotImplementedError

    def send_event_list(self, event_list: list[Event]):
        raise NotImplementedError
