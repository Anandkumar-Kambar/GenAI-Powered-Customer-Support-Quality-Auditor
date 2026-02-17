from abc import ABC, abstractmethod

class SummarizerBase(ABC):
    @abstractmethod
    def summarize(self, transcript: dict) -> dict:
        pass
