import hashlib
import json
import random
from collections import OrderedDict
from datetime import datetime
 
 
class Jae_MerkTree:
 
	def __init__(self,listoftransaction=None):
		self.listoftransaction = listoftransaction
		self.past_transaction = OrderedDict()
  
	def create_tree(self):
 
		listoftransaction = self.listoftransaction
		past_transaction = self.past_transaction
		temp_transaction = []
 
		for index in range(0,len(listoftransaction),2):
 
			current = repr(listoftransaction[index])
 
			if index+1 != len(listoftransaction):
				current_right = repr(listoftransaction[index+1])
 
			else:
				current_right = ''
 
			current_hash = hashlib.sha256(current.encode('utf-8'))
 
			if current_right != '':
				current_right_hash = hashlib.sha256(current_right.encode('utf-8'))
 
			past_transaction[listoftransaction[index]] = current_hash.hexdigest()
 
			if current_right != '':
				past_transaction[listoftransaction[index+1]] = current_right_hash.hexdigest()
 
			if current_right != '':
				temp_transaction.append(current_hash.hexdigest() + current_right_hash.hexdigest())
 
			else:
				temp_transaction.append(current_hash.hexdigest())
 
		if len(listoftransaction) > 1:
			self.listoftransaction = temp_transaction
			self.past_transaction = past_transaction
 
			self.create_tree()
 
	def Get_past_transacion(self):
		return self.past_transaction
 
	def Get_Root_leaf(self):
		last_key = list(self.past_transaction.keys())[-1]
		return self.past_transaction[last_key]
 
class property:
    def __init__(self, pid, price, owner):
        self.pid = pid
        self.price = price
        self.owner = owner
 
class user:
    def __init__(self, uid, ustake, wallet, properties):
        self.uid = uid
        self.ustake = ustake
        self.wallet = wallet
        self.properties = properties                        #list of properties (stored as list of pids)
 
class transaction:
    def __init__(self, buyer, seller, pid):
        self.buyer = buyer
        self.seller = seller
        self.pid = pid
 
genesis_winner = user(0,0,0,[])
class Blockchain:
   
    def __init__(self):
        self.chain = []
        self.create_block(previous_hash='0', winner = genesis_winner,mrklrt='0')
 
    def create_block(self, previous_hash, winner,mrklrt):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.now()),
                 'previous_hash': previous_hash,
                 'validator': winner.uid,
                 'Merkle_root': mrklrt
                 }
        if(block['index']==1):
             response = {'message': 'Genesis Block CREATED',
                'index': len(self.chain) + 1,
                'timestamp': str(datetime.now()),
                'previous_hash': 'NULL',
                'validator': 0,
                'Merkle_Root': 0}
             print(response)
        self.chain.append(block)
        winner.ustake += 42
        return block
 
    def print_previous_block(self):
        return self.chain[-1]
       
    def proof_of_stake(self, user_list):
        lottery = list()
        for i in user_list:
            for j in range(i.ustake):
                lottery.append(i)
        random.shuffle(lottery)
        winner_index = random.randint(0,len(lottery)-1)
        winner = lottery[winner_index]   
        return winner
 
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
 
    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
         
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
 
            previous_block = block
            block_index += 1
         
        return True
 
user_list = list()
property_list = list()
transaction_list = list()
 
def menu():
    print("\nChoose action: \n")
    print("1. Add New User")
    print("2. Add New Property")
    print("3. Enter a transaction")
    print("4. Calculate hashes of all transactions in a block")
    print("5. View transaction history of a property")
    print("6. Exit\n")
 
def add_user():
    uid = int(input("Enter the user id: "))
    ustake = 0
    uwallet = int(input("Enter the user wallet: "))
 
    n = int(input("Enter the number of properties of the user: "))
    uproperties = list()
 
    for i in range(n):
        p = int(input("Enter the property id: "))
        flag = 0
        for j in property_list:
            print("\n " + str(j.pid) + " ")
            if(j.pid == p):
                flag = 1
                break
 
        if(not flag):                                                           # if property does not exist
            print("Property not found, adding to user's property list")
            price = int(input("Enter the property price: "))
            ustake += price
            property_list.append(property(p, price, uid))                   
 
            # ADD PROPERTY PRICES TO USER STAKE HERE
        flag = 1
        for j in property_list:
            if(j.pid == p):                               # already owned property
                if(j.owner != uid):
                    print("User is not the owner of the property")
                    flag = 0
        if(flag):        
            uproperties.append(p)                                           # uproperties - list of pids             
 
    return user(uid, ustake, uwallet, uproperties)
 
def add_property():
    pid = int(input("Enter the property ID: "))
    price = int(input("Enter the property price: "))
    owner = int(input("Enter the property owner ID: "))

    flag = 0
    for i in range (0, len(property_list)):
        if(property_list[i].pid == pid):
            flag = 1
            break
    if(flag):
        print("Property already exists in the system")
        return
 
    flag = 0
    for i in range (0, len(user_list)):
        if(user_list[i].uid == owner):
            flag = 1
            break
    if(not flag):
        print("Owner not found")
        return
 
    return property(pid, price, owner)
 
def enter_transaction():
    buyer = int(input("Enter the buyer id: "))
    seller = int(input("Enter the seller id: "))
    pid = int(input("Enter the property id: "))
 
    flag = 0
    for i in range (0, len(user_list)):
        if(user_list[i].uid == buyer):
            b_index = i
            flag = 1
            break
    if(not flag):
        print("Buyer not found")
        return
    
    flag = 0
    for i in range (0, len(user_list)):
        if(user_list[i].uid == seller):
            s_index = i
            flag = 1
            break
    if(not flag):
        print("Seller not found")
        return
 
    flag = 0
    for i in range(0, len(property_list)):
        if(property_list[i].pid == pid):
            flag = 1
            p_index = i
            break
    if(not flag):
        print("Property not found")
        return
 
    if(property_list[p_index].owner != seller):
        print("Seller is not the owner of the property")
        return
 
    if(property_list[p_index].price > user_list[b_index].wallet):
        print("Buyer does not have enough money")
        return
 
    # add more testcases
 
    property_list[p_index].owner = buyer
 
    user_list[b_index].ustake += property_list[p_index].price
    user_list[s_index].ustake -= property_list[p_index].price
 
    user_list[b_index].wallet -= property_list[p_index].price
    user_list[s_index].wallet += property_list[p_index].price
 
    return transaction(buyer, seller, pid)
 
 
def calculate_merkle():
    Jae_Tree = Jae_MerkTree()
    Jae_Tree.listoftransaction = transaction_list
    Jae_Tree.create_tree()
    past_transaction = Jae_Tree.Get_past_transacion()
    return Jae_Tree.Get_Root_leaf()
 
blockchain = Blockchain() 
def calculate_hashes():
    previous_block = blockchain.print_previous_block()
    winner = blockchain.proof_of_stake(user_list)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(previous_hash, winner,calculate_merkle())
     
    response = {'message': 'A block is CREATED',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'previous_hash': block['previous_hash'],
                'validator': block['validator'],
                'Merkle_Root': block['Merkle_root']}
    print(response)
    print("User " + repr(block['validator']) + " updated stake is: " + repr(winner.ustake))
    
    return
 
 
def view_transaction_history(p):
    ctr = 0
    for t in transaction_list:
        if(t.pid == p):
            print(str(ctr) + ".\n" + str(t.buyer) + " bought " + str(t.pid) + " from " + str(t.seller))
    return
 
def main():
    while True:
        menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            user_list.append(add_user())
        elif choice == "2":
            property_list.append(add_property())
        elif choice == "3":
            transaction_list.append(enter_transaction())
        elif choice == "4":
            calculate_hashes()
        elif choice == "5":
            p = int(input("Enter the property ID: "))
            view_transaction_history(p)
        elif choice == "6":
            break
        else:
            print("Invalid choice")
 
if __name__ == "__main__":
    main()
 