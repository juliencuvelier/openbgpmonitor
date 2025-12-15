from abc import ABC
from openbgpmonitor.core.models.event_models import Event


class TSDBInterface(ABC):
    """Abstract base class for sending events to a Time Series Database (TSDB).

    This interface defines methods for sending single events or lists of events
    to a TSDB. Implementations should provide concrete logic for these methods.
    """

    def send_event(self, event: Event):
        """Send a single event to the TSDB.

        Args:
            event (Event): The event to be sent.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError

    def send_event_list(self, event_list: list[Event]):
        """Send a list of events to the TSDB.

        Args:
            event_list (list[Event]): The list of events to be sent.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError
