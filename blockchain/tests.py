from django.test import TestCase
from blockchain.quantum_chain import create_block

class BlockchainTest(TestCase):

    def test_block_creation(self):
        block = create_block([1, 2, 3])
        self.assertIn("hash", block)
