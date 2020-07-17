

from google.cloud import datastore
from google.cloud import ndb


foodBank = ndb.Client()

# [START FoodItem]
class FoodItem(ndb.Model):
    """Model for representing food item entry"""
    bankName = ndb.StringProperty()
    foodType = ndb.StringProperty()
    foodDesc = ndb.StringProperty()
    itemCount = ndb.IntegerProperty()
# [END FoodItem]


# [START inputting]
def storeFoodItem(bank, fType, desc, quantity):
    bank = bank.upper()
    fType = fType.upper()
    desc = desc.lower()
    with foodBank.context():
        query = FoodItem.query(FoodItem.bankName == bank, FoodItem.foodType == fType, FoodItem.foodDesc == desc)

        if query.count():
            item = query.get()
            item.itemCount += quantity
        else:
            item = FoodItem(bankName = bank,
                            foodType = fType,
                            foodDesc = desc,
                            itemCount = quantity)

        item.put()


def inputDonations():
    print('Which bank is being donated to?')
    bank = input("Enter bank: ")

    fType = input(
            '''Enter food type (q to quit):
            1. Canned
            2. Boxed
            3. Jarred
            ''')
    while fType != 'q':
        fDesc = input("Enter food description: ")
        quantity = int(input("Enter number of item being donated: "))

        storeFoodItem(bank, fType, fDesc, quantity)

        fType = input(
            '''Enter food type (q to quit):
            1. Canned
            2. Boxed
            3. Jarred
            ''')
# [END inputting]


# [START removing]
def removeFoodItem(bank, desc, quantity):
    with foodBank.context():
        query = FoodItem.query(FoodItem.bankName == bank.upper(), FoodItem.foodDesc == desc.lower())
        item = query.get()
        item.itemCount -= quantity

        item.put()
    
    return item


def removeDonations():
    bank = input("Enter bank: ")
    desc = input("Enter desc: ")
    quantity = int(input("Enter number of item being removed: "))

    removedItem = removeFoodItem(bank, desc, quantity)
# [END removing]


# [START searching]
def fetchFoodByBank(bank):
    with foodBank.context():
        query = FoodItem.query(FoodItem.bankName == bank)
        items = [i.bankName + ' | ' + i.foodType + ' | ' + i.foodDesc + ' | ' + str(i.itemCount) for i in query]
    return items


def fetchFoodByType(fType):
    with foodBank.context():
        query = FoodItem.query(FoodItem.foodType == fType)
        items = [i.bankName + ' | ' + i.foodType + ' | ' + i.foodDesc + ' | ' + str(i.itemCount) for i in query]

    return items


def fetchFoodByDesc(desc):
    with foodBank.context():
        query = FoodItem.query(FoodItem.foodDesc == desc)
        items = [i.bankName + ' | ' + i.foodType + ' | ' + i.foodDesc + ' | ' + str(i.itemCount) for i in query]

    return items


def fetchFoodNeeded(bank):
    with foodBank.context():
        query = FoodItem.query(FoodItem.bankName == bank.upper(), FoodItem.itemCount <= 10)
        # items = [i.bankName + ' | ' + i.foodType + ' | ' + i.foodDesc + ' | ' + str(i.itemCount) for i in query]
        items = query.fetch()

    return items


def searchDonations():
    items = ""

    searchType = input('''Search donations by all or needed?
    ''')

    if searchType == "all":
        searchChoice = input(
        '''Would you like to search by:
        1. Bank
        2. Food Type
        3. Food Description
        ''')
        searchChoice = searchChoice.lower()

        if searchChoice == "bank":
            items = fetchFoodByBank(input("Enter bank you would like to search: ").upper())
        elif searchChoice == "food type" or searchChoice == "foodtype":
            items = fetchFoodByType(input("Enter type of food you would like to search: ").upper())
        elif searchChoice == "food description" or searchChoice == "fooddescription" or searchChoice == "food desc" or searchChoice == "fooddesc":
            items = fetchFoodByDesc(input("Enter description of food you would like to search: ").lower())
        else:
            print("Invalid choice")

        if items != "":
            print("Items found:")
            for i in items:
                print(i)
    elif searchType == "needed":
        items = fetchFoodNeeded(input("Enter bank you would like to search: ").upper())

        if items != "":
            print("Items Needed:")
            for i in items:
                print(i)
    else:
        print("Invalid choice")
# [END searching]

# [START tempMain]
def tempMain():
    print('''Here as a bank or personal user?
    1. Bank
    2. Personal
    ''')

    userType = input("Enter user type: ")

    if userType == 'Bank' or userType == 'bank' or userType == '1':
        inOrOut = input('''Input or remove donations?
        ''')
        if inOrOut == 'input' or inOrOut == 'Input':
            inputDonations()
        elif inOrOut == 'remove' or inOrOut == 'Remove':
            removeDonations()
        else:
            print("Invalid choice")
    elif userType == 'Personal' or userType == 'personal' or userType == '2':
        searchDonations()
    else:
        print("Invalid choice")
# [END tempMain]
