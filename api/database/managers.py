from datetime import datetime
import hashlib
import json

# Initial ledger for credentials
temp_ledger = {"test_rfid_device_01": "password1234", "test_temphumid_device_01": "password1234", "test_accel_device_01": "password1234", "test_motion_device_01": "password1234"}


class PrivateBlockchainManager(object):
    def __init__(self, db_model):
        self.db = db_model
        self.secret_pass = "daab03ff8f4c3b718549b51119ed88ce"
        for key, value in temp_ledger.items():
            self.add_user(key, value, self.secret_pass)
    
    def add_user(self, user, password, secret):
        if self.secret_pass == secret:
            if self.db.objects.count() == 0:
                self.create_gen_block()
            if self.check_user(user, password) == False:
                transaction = self.create_transaction("add_user", user, password)
                self.create_block([json.dumps(transaction)])
                return True
            return False

    def get_users(self):
        temp_list = json.loads(self.db.objects().order_by('-_id').to_json())
        #temp_list = json.loads(self.db.objects().order_by('-_id').limit(1).to_json())[0]
        return temp_list    

    def check_user(self, user, password):
        temp_list = self.get_users()
        user_list = []
        for index in range(0, len(temp_list)-1):
            if temp_list[index]["current_level"] == temp_list[index+1]["current_level"] + 1:
                if temp_list[index]["previous_hash"] == hashlib.md5(json.dumps(temp_list[index+1], sort_keys=True).encode()).hexdigest():
                    transactions = temp_list[index]["transactions"]
                    for transaction in transactions:
                        transaction = json.loads(transaction)
                        if transaction["action"] == 'add_user':
                            user_list.append(transaction)
                            
        if next((item for item in user_list if item['user'] == 'rand' and item['password'] == self.__generate_hash(password)), None) is not None:
            return True
        return False

    def create_transaction(self, action, user, password):
        return {"action": action, "user": user, "password": self.__generate_hash(password), "timestamp": datetime.now().timestamp()}

    def create_block(self, transactions, nonce=0):
        temp_db = self.db()
        temp_db.previous_hash = self.__generate_hash(json.loads(self.db.objects().order_by('-_id').limit(1).to_json())[0], 'dict')
        temp_db.timestamp =  datetime.fromtimestamp(datetime.now().timestamp())
        temp_db.nonce = nonce
        temp_db.transactions = transactions
        temp_db.current_level = self.db.objects.count() + 1
        temp_db.save()

    def create_gen_block(self, nonce=0):
        temp_db = self.db()
        temp_db.previous_hash = self.__generate_hash({}, 'dict')
        temp_db.timestamp =  datetime.fromtimestamp(datetime.now().timestamp())
        temp_db.nonce = nonce
        temp_db.transactions = []
        temp_db.current_level = self.db.objects.count() + 1
        temp_db.save()

    def __generate_hash(self, input, mode=None):
        hash = hashlib.md5()
        if mode == 'dict':
            input = json.dumps(input, sort_keys=True)
        hash.update(input.encode())
        return hash.hexdigest()
