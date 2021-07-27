from datetime import datetime
import hashlib
import json

# Initial ledger for credentials
temp_ledger = {"test_rfid_device_01": "password1234", "test_temphumid_device_01": "password1234", "test_accel_device_01": "password1234", "test_motion_device_01": "password1234"}


class PrivateBlockchainManager(object):
    def __init__(self, db_model):
        self.db = db_model
        self.secret_pass = "daab03ff8f4c3b718549b51119ed88ce"
        if self.db.objects.count() == 0:
            transaction = self.create_transaction("genesis_block", "dummy_user", "dummy_password")
            self.create_block([json.dumps(transaction)])

        for key, value in temp_ledger.items():
            self.add_user(key, value, self.secret_pass)
    
    def add_user(self, user, password, secret):
        if self.secret_pass == secret:
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
                            
        if next((item for item in user_list if item['user'] == user and item['password'] == self.__generate_hash(password)), None) is not None:
            return True
        return False

    def create_transaction(self, action, user, password):
        return {"action": action, "user": user, "password": self.__generate_hash(password), "timestamp": datetime.now().timestamp()}

    def create_block(self, transactions, nonce=0):
        hash_val = json.loads(self.db.objects().order_by('-_id').limit(1).to_json())[0] if self.db.objects.count() > 0 else {}

        temp_db = self.db()
        temp_db.previous_hash = self.__generate_hash(hash_val, 'dict')
        temp_db.timestamp =  datetime.fromtimestamp(datetime.now().timestamp())
        temp_db.nonce = nonce
        temp_db.transactions = transactions
        temp_db.current_level = self.db.objects.count() + 1
        temp_db.save()

    def __generate_hash(self, input, mode=None):
        hash = hashlib.md5()
        if mode == 'dict':
            input = json.dumps(input, sort_keys=True)
        hash.update(input.encode())
        return hash.hexdigest()

class PublicBlockchainManager(object):
    def __init__(self, public_db_model, pending_db_model, difficulty, max):
        self.public_db = public_db_model
        self.pending_db = pending_db_model
        self.difficulty = difficulty
        self.max = max
        self.secret_pass = "daab03ff8f4c3b718549b51119ed88ce"

        if self.public_db.objects.count() == 0:
            transaction = self.create_transaction("genesis_block", {"placeholder": "placeholder"})
            self.create_block([json.dumps(transaction)])

    def get_public_blocks(self):
        temp_list = json.loads(self.public_db.objects().order_by('-_id').to_json())
        #temp_list = json.loads(self.public_db.objects().order_by('-_id').limit(1).to_json())[0]
        return temp_list    
    
    def get_pending_blocks(self):
        temp_list = json.loads(self.pending_db.objects().order_by('_id').to_json())
        #temp_list = json.loads(self.pending_db.objects().order_by('_id').limit(1).to_json())[0]
        return temp_list    

    def check_participant(self, participant):
        temp_list = self.get_public_blocks()
        user_list = []
        for index in range(0, len(temp_list)-1):
            if temp_list[index]["current_level"] == temp_list[index+1]["current_level"] + 1:
                transactions = temp_list[index]["transactions"]
                for transaction in transactions:
                    transaction = json.loads(transaction)
                    if transaction["action"] == 'register_participant':
                        user_list.append(transaction)

        if next((item for item in user_list if item['data']['key'] == participant), None) is not None:
            return True
        return False
    
    def count_participants(self):
        temp_list = self.get_public_blocks()
        counter = 0
        for index in range(0, len(temp_list)-1):
            if temp_list[index]["current_level"] == temp_list[index+1]["current_level"] + 1:
                transactions = temp_list[index]["transactions"]
                for transaction in transactions:
                    transaction = json.loads(transaction)
                    if transaction["action"] == 'register_participant':
                        counter+=1
        return counter

    def search_participant(self, userid):
        temp_list = self.get_public_blocks()
        counter = 0
        for index in range(0, len(temp_list)-1):
            if temp_list[index]["current_level"] == temp_list[index+1]["current_level"] + 1:
                transactions = temp_list[index]["transactions"]
                for transaction in transactions:
                    transaction = json.loads(transaction)
                    if transaction["action"] == 'register_participant':
                        return transaction["data"]["key"]
        return None 

    def create_transaction(self, action, data):
        return {"action": action, "data": data, "timestamp": datetime.now().timestamp()}

    def create_block(self, transactions, nonce=0):
        hash_val = json.loads(self.public_db.objects().order_by('-_id').limit(1).to_json())[0] if self.public_db.objects.count() > 0 else {}

        temp_db = self.public_db()
        temp_db.previous_hash = self.__generate_hash(hash_val, 'dict')
        temp_db.timestamp =  datetime.fromtimestamp(datetime.now().timestamp())
        temp_db.nonce = nonce
        temp_db.transactions = transactions
        temp_db.current_level = self.public_db.objects.count() + 1
        temp_db.save()

    def create_pending_block(self, transactions, nonce=0):
        temp_db = self.pending_db()
        temp_db.previous_hash = self.__generate_hash(json.loads(self.public_db.objects().order_by('-_id').limit(1).to_json())[0], 'dict')
        temp_db.timestamp =  datetime.fromtimestamp(datetime.now().timestamp())
        temp_db.nonce = nonce
        temp_db.transactions = transactions
        temp_db.current_level = self.public_db.objects.count() + 1
        temp_db.locked = False
        temp_db.votes = 0
        temp_db.save()

    def add_participant(self, participant):
        try:
            key = self.search_participant(participant)
            if key is None:
                key = self.__generate_hash(participant + str(datetime.now().timestamp()))
                transaction = self.create_transaction("register_participant", {"userid": participant, "key": key})
                self.create_block([json.dumps(transaction)])
            return key 
        except Exception as e:
            print(e)
            return None

    def add_data_transaction(self, data, data_type):
        temp = self.check_status(0)
        temp_transaction = self.create_transaction("add_" + data_type + "_data", data)
        temp_transaction = json.dumps(temp_transaction)
        if temp is None:
            self.create_pending_block([temp_transaction])
        else:
            block = self.pending_db.objects.get(id = temp["_id"]["$oid"])
            new_transaction_list = temp["transactions"]
            new_transaction_list.append(temp_transaction)
            block.transactions = new_transaction_list
            block.save()

    def add_block_to_chain(self):
        temp = self.check_status(1)
        if temp is not None and temp["locked"] == False:
            block = self.pending_db.objects.get(id = temp["_id"]["$oid"])
            block.locked = True
            block.save()

            if temp["votes"] >= self.count_participants()/2:  
                temp_db = self.public_db()
                temp_db.previous_hash =  temp["previous_hash"]
                temp_db.timestamp =  temp["timestamp"]
                temp_db.nonce = temp["nonce"]
                temp_db.transactions = temp["transactions"]
                temp_db.current_level =  temp["current_level"]
                temp_db.save()
                block.delete()

    def __generate_hash(self, input, mode=None):
        hash = hashlib.md5()
        if mode == 'dict':
            input = json.dumps(input, sort_keys=True)
        hash.update(input.encode())
        return hash.hexdigest()

    def check_status(self, mode=0):
        block = None
        counter = 0
        while True:
            if counter < self.pending_db.objects.count(): 
                temp_block = json.loads(self.pending_db.objects().order_by('_id').to_json())[counter]
                if len(temp_block["transactions"]) < self.max and mode == 0:
                    return temp_block
                elif  len(temp_block["transactions"]) == self.max and mode == 1:
                    return temp_block
                counter+=1
            else:
                return block

    def generate_proof_of_work(self, id):
        block = self.pending_model_to_dict(id)
        print(block)
        computed_hash = self.compute_hash(block)
        while not computed_hash.startswith('0' * self.difficulty):
            block["nonce"] += 1
            computed_hash = self.compute_hash(block)
        return computed_hash

    def verify_proof_of_work(self, id, proof):
        print(self.pending_model_to_dict(id) == proof)
        return proof == self.generate_proof_of_work(id)
    
    def compute_hash(self, block):
        block_string = json.dumps(block, indent=4, sort_keys=True, default=str)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def pending_model_to_dict(self, id):
        block = self.pending_db.objects.get(id = id)
        if block is not None:
            temp_block = {}
            temp_block["previous_hash"] = block["previous_hash"]
            temp_block["timestamp"] = block["timestamp"]
            temp_block["nonce"] = block["nonce"]
            temp_block["transactions"] = block["transactions"]
            temp_block["current_level"] = block["current_level"]
            return temp_block
        return None
    
    def get_full_block(self):
        block = self.__check_status(1)
        if block is not None:
            return pending_model_to_dict(block["_id"]["$oid"])
        else:
            return None

    def vote_to_add_block(self, id):
        block = self.pending_db.objects.get(id = id)
        if block is not None:
            block.votes += 1
            block.save()