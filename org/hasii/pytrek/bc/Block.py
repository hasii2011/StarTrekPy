
import time
import hashlib


class Block(object):

    def __init__(self, index, proof, previous_hash, transactions, timestamp=None):
        self.index = index
        self.proof = proof
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()

    @property
    def get_block_hash(self):

        block_string = f"{self.index}{self.proof}{self.previous_hash}{self.transactions}{self.timestamp}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def __repr__(self):
        return f"{self.index} - {self.proof} - {self.previous_hash} - {self.transactions} - {self.timestamp}"
