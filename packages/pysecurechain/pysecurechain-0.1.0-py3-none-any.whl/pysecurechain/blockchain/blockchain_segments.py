from abc import ABC, abstractmethod
from typing import Any, Union, Iterable

from pysecurechain import Block
from pysecurechain.exceptions import (
    BlockchainAttributeTypeError,
    BlockchainAttributeKeyError,
)


class BlockchainSegmentInterface(ABC):
    @abstractmethod
    def create_genesis_block(self):
        pass

    @abstractmethod
    def add_transactions(self, transactions: Union[Any, Iterable[Any]]) -> bool:
        pass

    @abstractmethod
    def register_transactions(self) -> bool:
        pass


class BlockchainSegment(BlockchainSegmentInterface):
    __slots__ = ["segment_id", "unconfirmed_transactions", "chain"]

    __attrs = {"segment_id": str, "unconfirmed_transactions": list, "chain": list}

    def create_genesis_block(self):
        return Block.create_genesis_block(segment_id=self.segment_id)

    def add_transactions(self, transactions: Union[Any, Iterable[Any]]):
        if not isinstance(transactions, Iterable):
            transactions = [transactions]
        self.unconfirmed_transactions.extend(list(transactions))
        return True

    def register_transactions(self) -> bool:
        self.chain.append(Block())

    @classmethod
    def __validate_attrs(cls, key: str, value: Any) -> None:
        """Checking the data types of class attributes."""
        if not isinstance(value, cls.__attrs[key]):
            raise TypeError

    def __setattr__(self, key, value):
        if key in self.__attrs:
            try:
                self.__validate_attrs(key, value)
            except TypeError:
                raise BlockchainAttributeTypeError
            else:
                return object.__setattr__(self, key, value)
        raise BlockchainAttributeKeyError

    def __init__(self, segment_id: str, transactions: list = None, chain: list = None):
        self.segment_id = segment_id
        self.unconfirmed_transactions = [] if transactions is None else transactions
        self.chain = [] if chain is None else chain
