import hashlib
import json
from collections import OrderedDict


# 1. Declare the class trees
class Jae_MerkTree:

	# 2. Initiate the class object
	def __init__(self,listoftransaction=None):
		self.listoftransaction = listoftransaction
		self.past_transaction = OrderedDict()

	# 3. Create the Merkle Tree  
	def create_tree(self):

		# 3.0 Continue on the declaration
		listoftransaction = self.listoftransaction
		past_transaction = self.past_transaction
		temp_transaction = []

		# 3.1 Loop until the list finishes
		for index in range(0,len(listoftransaction),2):

			# 3.2 Get the most left element 
			current = listoftransaction[index]

			# 3.3 If there is still index left get the right of the left most element
			if index+1 != len(listoftransaction):
				current_right = listoftransaction[index+1]

			# 3.4 If we reached the limit of the list then make a empty string
			else:
				current_right = ''

			# 3.5 Apply the Hash 256 function to the current values
			current_hash = hashlib.sha256(current.encode('utf-8'))

			# 3.6 If the current right hash is not a '' <- empty string
			if current_right != '':
				current_right_hash = hashlib.sha256(current_right.encode('utf-8'))

			# 3.7 Add the Transaction to the dictionary 
			past_transaction[listoftransaction[index]] = current_hash.hexdigest()

			# 3.8 If the next right is not empty
			if current_right != '':
				past_transaction[listoftransaction[index+1]] = current_right_hash.hexdigest()

			# 3.9 Create the new list of transaction
			if current_right != '':
				temp_transaction.append(current_hash.hexdigest() + current_right_hash.hexdigest())

			# 3.01 If the left most is an empty string then only add the current value
			else:
				temp_transaction.append(current_hash.hexdigest())

		# 3.02 Update the variables and rerun the function again 
		if len(listoftransaction) > 1:
			self.listoftransaction = temp_transaction
			self.past_transaction = past_transaction

			# 3.03 Call the function repeatly again and again until we get the root 
			self.create_tree()

	# 4. Return the past Transaction 
	def Get_past_transacion(self):
		return self.past_transaction

	# 5. Get the root of the transaction
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
        flag = 1
        p = int(input("Enter the property id: "))
        if(p not in property_list):                                      # if property exists
            print("Property not found, adding to user's property list")
            price = int(input("Enter the property price: "))
            ustake += price
            property_list.append(property(p, price, uid))

            # ADD PROPERTY PRICES TO USER STAKE HERE
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

    if(owner not in user_list):
        print("Owner not found")
        return

    return property(pid, price, owner)

def enter_transaction():
    buyer = int(input("Enter the buyer id: "))
    seller = int(input("Enter the seller id: "))
    pid = int(input("Enter the property id: "))

    flag = 0
    for i in user_list:
        if(i.uid == buyer):
            flag = 1
            break
    if(not flag):
        print("Buyer not found")
        return
    
    flag = 0
    for i in user_list:
        if(i.uid == seller):
            flag = 1
            break
    if(not flag):
        print("Seller not found")
        return
    
    flag = 0
    ctr=-1
    for i in property_list:
        ctr+=1
        if(i.pid == pid):
            flag = 1
            break
    if(not flag):
        print("Property not found")
        return
    
    if(property_list[ctr].owner != seller):
        print("Seller is not the owner of the property")
        return

    if(property_list[ctr].price > user_list[buyer].wallet):
        print("Buyer does not have enough money")
        return

    # add more testcases

    property_list[pid].owner = buyer

    user_list[buyer].ustake += property_list[pid].price
    user_list[seller].ustake -= property_list[pid].price

    user_list[buyer].wallet -= property_list[pid].price
    user_list[seller].wallet += property_list[pid].price

    return transaction(buyer, seller, pid)

def calculate_hashes():
    Jae_Tree = Jae_MerkTree()
    Jae_Tree.listoftransaction = transaction_list
    Jae_Tree.create_tree()
    past_transaction = Jae_Tree.Get_past_transacion()
    print ('Final root of the tree : ',Jae_Tree.Get_Root_leaf())
	# c) pass on the transaction list 
	
	# d) Create the Merkle Tree transaction
	
	# e) Retrieve the transaction 
	
	# f) Get the last transaction and print all 
	
    return

def view_transaction_history(p):
    ctr = 0
    for t in transaction_list:
        if(t.pid == p.pid):
            print(ctr + ".\n" + t.buyer + " bought " + t.pid + " from " + t.seller)
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
            view_transaction_history()
        elif choice == "6":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()


        