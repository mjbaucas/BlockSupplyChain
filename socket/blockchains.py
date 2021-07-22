from datetime import datetime
import hashlib

class PrivateBlock():
    def __init__(self, transactions, current_level, previous_hash):
        self.previous_hash = previous_hash
        self.timestamp = datetime.now().timestamp()
        self.nonce = 0
        self.transactions = transactions
        self.current_level = current_level

