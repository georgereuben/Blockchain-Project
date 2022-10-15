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

user_set = set()
property_set = set()
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
        if(p not in property_set):                                      # if property exists
            print("Property not found, adding to user's property list")
            price = int(input("Enter the property price: "))
            ustake += price
            property_set.add(property(p, price, uid))

            # ADD PROPERTY PRICES TO USER STAKE HERE
        if(property_set[p].owner != uid):                               # already owned property
            print("User is not the owner of the property")
            continue
        uproperties.append(p)                                           # uproperties - list of pids             

    return user(uid, ustake, uwallet, uproperties)

def add_property():
    pid = int(input("Enter the property ID: "))
    price = int(input("Enter the property price: "))
    owner = int(input("Enter the property owner ID: "))

    if(owner not in user_set):
        print("Owner not found")
        return

    return property(pid, price, owner)

def enter_transaction():
    buyer = int(input("Enter the buyer id: "))
    seller = int(input("Enter the seller id: "))
    pid = int(input("Enter the property id: "))

    if(buyer not in user_set):
        print("Buyer not found")
        return
    
    if(seller not in user_set):
        print("Seller not found")
        return
    
    if(pid not in property_set):
        print("Property not found")
        return
    
    if(property_set[pid].owner != seller):
        print("Seller is not the owner of the property")
        return

    if(property_set[pid].price > user_set[buyer].wallet):
        print("Buyer does not have enough money")
        return

    # add more testcases

    property_set[pid].owner = buyer

    user_set[buyer].ustake += property_set[pid].price
    user_set[seller].ustake -= property_set[pid].price

    user_set[buyer].wallet -= property_set[pid].price
    user_set[seller].wallet += property_set[pid].price

    return transaction(buyer, seller, pid)

def calculate_hashes():
    pass

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
            user_set.add(add_user())
        elif choice == "2":
            property_set.add(add_property())
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


        