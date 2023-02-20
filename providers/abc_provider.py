from abc import ABC, abstractmethod


class ProviderABC(ABC):
    def start(self):
        raise NotImplementedError()
