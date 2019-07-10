
from unittest import main

from logging import getLogger
from logging import Logger

from BaseTest import BaseTest

from org.hasii.pytrek.bc.BlockChain import BlockChain
from org.hasii.pytrek.bc.Block import Block


class BlockChainTest(BaseTest):

    @classmethod
    def setUpClass(cls):
        """"""
        BaseTest.setUpLogging()

    def setUp(self):
        """"""

        self.logger: Logger = getLogger(__name__)

    def testBasic(self):

        blockchain: BlockChain = BlockChain()

        self.logger.info(">>>>> Before Mining...")
        self.logger.info(blockchain.chain)

        last_block: Block = blockchain.get_last_block
        last_proof = last_block.proof
        proof = blockchain.create_proof_of_work(last_proof)

        self.logger.debug(f"proof: {proof}")
        #
        # Sender "0" means that this node has mined a new block
        # For mining the Block(or finding the proof), we must be awarded with some amount(in our case this is 1)
        #
        blockchain.create_new_transaction(sender="0", recipient="address_x", amount=1)

        last_hash = last_block.get_block_hash
        block = blockchain.create_new_block(proof, last_hash)
        self.logger.debug(f"new block:{block}")

        self.logger.info(">>>>> After Mining...")
        self.logger.info(blockchain.chain)


if __name__ == '__main__':
    main()
