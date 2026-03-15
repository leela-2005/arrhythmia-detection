import hashlib
import time

# In-memory blockchain
blockchain = []

def create_block(data):
    """
    Creates a blockchain block for ECG data integrity
    """

    previous_hash = blockchain[-1]["hash"] if blockchain else "0"

    payload = f"{data}{previous_hash}{time.time()}"
    current_hash = hashlib.sha256(payload.encode()).hexdigest()

    block = {
        "hash": current_hash,
        "prev_hash": previous_hash,
        "timestamp": time.time(),
        "data": data
    }

    blockchain.append(block)
    return block
