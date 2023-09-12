from datetime import datetime
import itertools
import random
from enum import Enum

class Utilities(Enum):
    RENT = 'rent'
    ELETRICITY = 'eletricity'
    WATER = 'water'
    NET = 'net'
    OTHER = 'other'

class Receipt():
    
    new_id = itertools.count()

    def __init__(self, bill, user_id, owers = None) -> None:
        self.id = next(Receipt.new_id)
        self.bill = bill
        self.payed_by = user_id
        self.owers = owers


class Bill():
    
    new_id = itertools.count()

    def __init__(self, value,bill_type = Utilities.OTHER, payed = False, payed_by = None, timestamp = datetime.utcnow()) -> None:
        self.id = next(Bill.new_id)
        self.value = value
        self.bill_type = bill_type
        self.timestamp = datetime.utcnow()
        self.payed = payed
        self.payed_by = payed_by
        self.payed_on = None
        self.receipt = None
        self.timestamp = timestamp

    def set_receipt(self, receipt):
        self.receipt = receipt

    def __repr__(self) -> str:
        return ('Value: {}€ Type: {} at {}').format(str(self.value), self.bill_type.value,self.timestamp.strftime("%m/%d/%Y, %H:%M:%S"))
    
class Debt():
    
    new_id = itertools.count()

    def __init__(self, user_to_pay, value, payed = False) -> None:
        self.id = next(Debt.new_id)
        self.user_to_pay = user_to_pay
        self.value = value
        self.payed = payed

class User():

    new_id = itertools.count()

    def __init__(self, username) -> None:
        self.id = next(User.new_id)
        self.username = username
        self.balance = 0
        self.debts = []

    def add_debt(self, debt : Debt) -> None:
        if debt is not None:
            return self.debts.append(debt)
    
    def __repr__(self) -> str:
        return str(self.id) + ' ' + self.username


def create_users(n_users : int) -> None:
    return [User(username='user'+ str(user)) for user in range(n_users)]

def create_bills(n_bills : int) -> None:
    bills = [Bill(value = 575, bill_type= Utilities.RENT),
             Bill(value= 36.40, bill_type=Utilities.NET),
             Bill(value= 40.3, bill_type=Utilities.WATER),
             Bill(value= 76.9, bill_type=Utilities.ELETRICITY)]
    return  bills + [Bill(value= round(random.uniform(0,65), 2)) for bill in range(n_bills)] 
    
def pay_single(user : User, bill : Bill) -> bool:
    return _pay(user, bill)

def pay_group(user : User, users: [], bill: Bill) -> bool:
    if len(users) == 0 or users is None:
        return False
    for group_member in users:
        if not group_member.id == user.id:
            value_to_pay = bill.value / len(users)
            group_member.add_debt(Debt(value= value_to_pay,user_to_pay= user.id))
            group_member.balance -= value_to_pay
    _pay(user, bill)

            
        

    
    
def _pay(user : User, bill : Bill):
    if user is None:
        return False
    if bill.payed or bill.payed_on is not None or bill.payed_by is not None:
        return False
    else:
        ##receipt = Receipt(bill= bill, user_id=user.id)
        bill.payed = True
        bill.payed_by = user.id
        bill.payed_on = datetime.utcnow()
        user.balance -= bill.value
        return True

if __name__ == "__main__":
    print('Start\n')
    N_USERS = 4
    N_BILLS = 2
    users = create_users(N_USERS)
    bills = create_bills(N_BILLS)
    user = User('admin')
    bill = Bill(value=150)
    pay_single(user, bill)
    print(user.balance)
    pay_group(user, users, bill)
    for u in users:
        print()
