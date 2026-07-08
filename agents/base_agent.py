from abc import ABC, abstractmethod


class BaseAgent(ABC):

    def __init__(self, name: str):

        self.name = name

    @abstractmethod
    def run(self, data):
        """
        Every agent implements its own run() method.
        """
        pass