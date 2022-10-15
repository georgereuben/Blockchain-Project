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

def calculate_hashes():
    pass

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


        