from abc import ABC


class TSDBInterface(ABC):
    def send_event(self, event):
        raise NotImplementedError
