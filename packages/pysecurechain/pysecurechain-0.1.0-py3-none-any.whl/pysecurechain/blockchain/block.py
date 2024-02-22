import hashlib
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Any

from pysecurechain.exceptions import (
    BlockchainAttributeTypeError,
    BlockchainAttributeKeyError,
)


class BlockInterface(ABC):
    @abstractmethod
    def calculate_hash(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def create_genesis_block(
        cls,
        segment_id: str,
        id: int = 0,
        previous_hash: str = "0",
        data: str = "Genesis Block",
        timestamp: datetime = datetime.utcnow(),
    ):
        pass


class Block(BlockInterface):
    """Block, a single component unit of the blockchain."""

    __attrs = {
        "id": int,
        "segment_id": str,
        "timestamp": datetime,
        "data": list,
        "previous_hash": str,
        "actual_hash": str,
    }

    @classmethod
    def __validate_attrs(cls, key: str, value: Any) -> None:
        """Checking the data types of class attributes."""
        if not isinstance(value, cls.__attrs[key]):
            raise TypeError

    def calculate_hash(self) -> str:
        """Calculating the hash function for self block of the blockchain."""
        return hashlib.scrypt(
            password="".join(
                [str(value) for value in self.__dict__.values() if value is not None]
            ).encode("utf-8"),
            salt="pysecurechain".encode("utf-8"),
            n=16384,
            r=8,
            p=1,
            dklen=256,
        ).hex()

    @classmethod
    def create_genesis_block(
        cls,
        segment_id: str,
        id: int = 0,
        previous_hash: str = "0",
        data: str = "Genesis Block",
        timestamp: datetime = datetime.utcnow(),
    ):
        return Block(
            id=id,
            segment_id=segment_id,
            previous_hash=previous_hash,
            data=data,
            timestamp=timestamp,
        )

    def __setattr__(self, key, value):
        if key in self.__attrs:
            try:
                self.__validate_attrs(key, value)
            except TypeError:
                raise BlockchainAttributeTypeError
            else:
                return object.__setattr__(self, key, value)
        raise BlockchainAttributeKeyError

    def __init__(
        self,
        id: int,
        segment_id: str,
        previous_hash: str,
        data: Optional[list] = None,
        timestamp: Optional[datetime] = None,
        actual_hash: Optional[str] = None,
    ):
        self.id = id
        self.segment_id = segment_id
        self.previous_hash = previous_hash
        self.data = [] if data is None else data
        self.timestamp = datetime.utcnow() if timestamp is None else timestamp
        self.actual_hash = self.calculate_hash() if actual_hash is None else actual_hash

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        attrs = ", ".join([f"{key}={value}" for key, value in self.__dict__.items()])
        return f"{self.__class__.__name__}({attrs})"
