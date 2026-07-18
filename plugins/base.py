from abc import ABC, abstractmethod

class Plugin(ABC):
    name = "base"
    priority = 100 #lower would be checked first

    @abstractmethod
    def matches(self, command: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def run(self, command: str) -> bool:
        raise NotImplementedError