import hashlib
from web3 import Web3
from eth_tester import EthereumTester

# Initialize a simulated local Ethereum blockchain via eth-tester
tester = EthereumTester()
w3 = Web3(Web3.EthereumTesterProvider(tester))

# Grab a dummy account provided by eth-tester for signing transactions
if w3.is_connected() and w3.eth.accounts:
    SENDER_ACCOUNT = w3.eth.accounts[0]
else:
    SENDER_ACCOUNT = None

def compute_sha256_hash(record_id: str, predicted_class: str, confidence: str, timestamp_str: str, shap_summary: str) -> str:
    """
    Concatenate the fields and compute a SHA-256 hash
    hash = SHA256(id || class || confidence || timestamp || shap_summary)
    """
    payload = f"{record_id}{predicted_class}{confidence}{timestamp_str}{shap_summary}"
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()

def log_to_blockchain(record_id: str, predicted_class: str, confidence: float, timestamp_str: str, shap_summary: str):
    """
    Logs the hash to the simulated database and simulated Web3 blockchain.
    Returns the computed block hash and transaction receipt hash.
    """
    from .models import BlockchainRecord
    
    confidence_str = f"{confidence:.4f}"
    
    # Generate SHA-256 Hash
    computed_hash = compute_sha256_hash(record_id, predicted_class, confidence_str, timestamp_str, shap_summary)
    
    # Simulate Blockchain Storage via Web3 (Sending a zero-eth transaction with the hash as data payload)
    tx_receipt_hash = None
    if SENDER_ACCOUNT:
        try:
            # We convert the hex hash to hexbytes for the transaction data
            data_payload = Web3.to_bytes(text=computed_hash)
            
            tx_hash = w3.eth.send_transaction({
                'from': SENDER_ACCOUNT,
                'to': SENDER_ACCOUNT,  # Send to self
                'data': data_payload,
                'gas': 2000000,
            })
            
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            tx_receipt_hash = tx_receipt.transactionHash.hex()
        except Exception as e:
            print(f"Web3 Simulation Error: {e}")

    # Store in our SQLite Ledger for Dashboard Viewing
    record = BlockchainRecord.objects.create(
        record_id=record_id,
        predicted_class=predicted_class,
        confidence_score=confidence,
        shap_summary=shap_summary,
        stored_hash=computed_hash,
        transaction_receipt=tx_receipt_hash
    )
    
    return record
