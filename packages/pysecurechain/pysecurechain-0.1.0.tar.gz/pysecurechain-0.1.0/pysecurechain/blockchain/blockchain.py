from abc import ABC, abstractmethod
from typing import Union


class BlockchainInterface(ABC):
    @abstractmethod
    def add_segment(
        self,
        segment_id: str,
    ):
        pass

    @abstractmethod
    def add_segment_transactions(
        self,
        segment_id: str,
        transactions: Union[dict, list[dict]],
    ):
        pass

    @abstractmethod
    def register_segment_transactions(
        self,
        segment_id: str,
    ):
        pass


class Blockchain(BlockchainInterface):
    __slots__ = ["segments"]

    def __init__(self):
        self.segments = dict()


blockchain = Blockchain()
blockchain.segments = [1234]
