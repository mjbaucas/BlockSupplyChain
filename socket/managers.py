import hashlib
from blockchains import PrivateBlock
import json

# Initial ledger for credentials
temp_ledger = {"test_rfid_device_01": "password1234", "test_temphumid_device_01": "password1234", "test_accel_device_01": "password1234", "test_motion_device_01": "password1234"}

class PrivateBlockchainManager(object):
    def __init__(self):
        self.secret_pass = "daab03ff8f4c3b718549b51119ed88ce"
        self.blockchain = []
        for key, value in temp_ledger.items():
            self.add_user(key, value, self.secret_pass)

    def add_user(self, user, password, secret):
        if secret == self.secret_pass:
            if len(self.blockchain) == 0:
                self.blockchain.append(self.create_gen_block())
            priv_block = self.create_block(user, password)
            self.blockchain.append(priv_block)

    def check_user(self, user, password):
        temp_list = self.blockchain
        user_list = []
        for index in range(len(temp_list)-1, 0, -1):
            if temp_list[index]["current_level"] == temp_list[index-1]["current_level"] + 1:
                if temp_list[index]["previous_hash"] == self.__generate_hash(self, temp_list[index-1], mode=None):
                    transactions = temp_list[index]["transactions"]
                    for transaction in transactions:
                        if transaction["action"] == 'add_user':
                            user_list.append(transaction)
                            
        if next((item for item in user_list if item['user'] == 'rand' and item['password'] == self.__generate_hash(password)), None) is not None:
            return True
        return False

    def create_block(self, user, password):
        temp_transaction = {'action': 'add_user', 'user': user, 'password': self.__generate_hash(password)}
        return PrivateBlock(temp_transaction, len(self.blockchain), self.__generate_hash(self.blockchain[-1]))

    def create_gen_block(self):
        return PrivateBlock([], len(self.blockchain), self.__generate_hash({}, 'dict'))

    def __generate_hash(self, input, mode=None):
        hash = hashlib.md5()
        if mode == 'dict':
            input = json.dumps(input, sort_keys=True)
        hash.update(str(input).encode())
        return hash.hexdigest()

