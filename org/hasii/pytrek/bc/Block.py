
import time
from hashlib import sha256


class Block(object):

    def __init__(self, index: int, proof: int, previous_hash: sha256, transactions, timestamp=None):

        self.index: int = index
        self.proof: int = proof

        self.previous_hash:sha256 = previous_hash

        self.transactions = transactions
        self.timestamp = timestamp or time.time()

    @property
    def get_block_hash(self) -> sha256:

        block_string = f"{self.index}{self.proof}{self.previous_hash}{self.transactions}{self.timestamp}"
        return sha256(block_string.encode()).hexdigest()

    def __repr__(self):
        return f"{self.index} - {self.proof:4} - {self.previous_hash} - {self.transactions} - {self.timestamp}\n"
