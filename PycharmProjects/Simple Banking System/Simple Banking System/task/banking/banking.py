from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Text
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

import random

engine = create_engine('sqlite:///card.s3db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'card'
    id = Column(Integer, primary_key=True)
    number = Column(Text, default='default_value_number')
    pin = Column(Text, default='default_value_pin')
    balance = Column(Integer, default=0)

    def __repr__(self):
        return self.number


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Write your code here


def menu_log_in():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")


def menu_log_out():
    print("1. Balance")
    print("2. Add income")
    print("3. Do transfer")
    print("4. Close account")
    print("5. Log out")
    print("0. Exit")


def generate_number():
    beg_num = "400000"
    end_num = random.randint(1000000000, 9000000000)
    print("Your card number:")
    print(int(beg_num + str(end_num)))
    return int(beg_num + str(end_num))


def luhn_algotirhm(num):
    '''num comes in string'''
    tab_int = []
    for idx, digit in enumerate(num):
        if idx % 2 == 0:
            digit = int(digit) * 2
            if digit > 9:
                digit -= 9
        tab_int.append(int(digit))
    luhn_num = 0 if sum(tab_int) % 10 > 9 else 10 - sum(tab_int) % 10
    num += str(luhn_num)
    card_num = ""
    for digit in num:
        card_num += str(digit)
    return card_num


def luhn_check(num_card_to_check):
    #print("luhn_check working")
    num_card_to_check = str(num_card_to_check)
    parse = num_card_to_check[0:(len(num_card_to_check)-1)]
    parse = luhn_algotirhm(parse)
    if num_card_to_check[-1] == parse[-1]:
        return True
    else:
        return False


def generate_number_luhn():
    beg_num = "400000"
    middle_num = ""
    luhn_check = ""
    for digit in range(0, 9):
        middle_num += str(random.randint(0, 9))

    card_number = beg_num + middle_num

    card_number = luhn_algotirhm(card_number)
    print("Your card number:")
    print(card_number)
    return card_number


def generate_pin():
    tab = []
    for x in range(0, 4):
        tab.append(str(random.randint(0, 9)))
    pin = ""
    for i in tab:
        pin += i
    print("Your card PIN:")
    print(pin)
    return pin


def check_balance(number):
    rows = session.query(Table).filter(Table.number == number).all()
    #print("rows", rows)
    print("Balance:", rows[0].balance)
    return ""

#    rows = session.query(Table).filter(Table.deadline == today.date()).all()


def log_in():
    print("Enter your card number:")
    card_num_input = input()
    print("Enter your PIN:")
    pin_input = input()
    rows = session.query(Table).filter(Table.number == str(card_num_input)).all()
    #print("rows", rows)
    #print("rows.pin", rows[0].pin, "pin_input", pin_input)
    #print("rows.number", rows[0].number, "card_num_input", card_num_input)
    if len(rows) == 0:
        return False
    if str(rows[0].pin) == str(pin_input) and str(rows[0].number) == str(card_num_input):
        global card_num
        card_num = str(rows[0].number)
        return True


def update_database(card_num, pin, balance):
    new_row = Table(number=card_num, pin=pin, balance=balance)
    session.add(new_row)
    session.commit()


def create_data():
    print("Your card has been created")
    card_num = generate_number_luhn()
    pin = generate_pin()
    balance = 0
    update_database(card_num, pin, balance)
    return card_num, pin, balance


def add_income(number):
    print("Enter income:")
    money = int(input())
    rows = session.query(Table).filter(Table.number == number).all()
    rows[0].balance += money
    session.commit()
    print("Income was added!")


def do_transfer(send_from_num):
    print("Transfer")
    print("Enter card number:")
    transfer_acc = input()
    if not luhn_check(transfer_acc):
        print("do_transfer Luhn chek failed")
        print("Probably you made mistake in the card number. Please try again!")
        return False
    recipient = session.query(Table).filter(Table.number == str(transfer_acc)).all()
    if len(recipient) == 0:
        print("Such a card does not exist.")
        return False
    else:
        sender = session.query(Table).filter(Table.number == send_from_num).all()
        if sender[0].number == recipient[0].number:
            print("You can't transfer money to the same account!")
            return False
        print("Enter how much money you want to transfer:")
        amount_to_transfer = int(input())
        if sender[0].balance <= amount_to_transfer:
            print("Not enough money!")
            return False
        else:
            sender[0].balance -= amount_to_transfer
            session.commit()
            #print("sender[0].balance", sender[0].balance)
            recipient = session.query(Table).filter(Table.number == transfer_acc).all()
            recipient[0].balance += amount_to_transfer
            #print("recipient[0].balance", recipient[0].balance)
            session.commit()
            print("Success!")
            return True


def close_account(num_del):
    del_acc = session.query(Table).filter(Table.number == str(num_del)).all()
    session.delete(del_acc[0])
    session.commit()
#    rows = session.query(Table).filter(Table.deadline == today.date()).all()
#    rows = session.query(Table).filter(Table.deadline == (today + timedelta(days=x)).date()).all()

con = True
card_num = ""
pin = 0
while con:
    menu_log_in()
    user_choice = input()
    if user_choice == "1":
        x, pin, balance = create_data()
    elif user_choice == "2":
        if log_in():
            print("You have successfully logged in!", end="\n\n")
            while True:
                menu_log_out()
                user_choice2 = input()
                if user_choice2 == "1":
                    check_balance(card_num)
                elif user_choice2 == "2":
                    add_income(card_num)
                elif user_choice2 == "3":
                    if not do_transfer(card_num):
                        continue
                elif user_choice2 == "4":
                    close_account(card_num)
                    break
                elif user_choice2 == "5":
                    print("You have successfully logged out!")
                    break
                elif user_choice2 == "0":
                    con = False
                    print("Bye!")
                    break
                else:
                    print("wrong number, bye")
                    break
        # elif not luhn_check(card_num):
        #     print("Wrong card number or PIN!")
        #     continue
        else:
            print("Wrong card number or PIN!")
            continue
    elif user_choice == "3":
        rows = session.query(Table).all()
        for x in rows:
            print("rows", x)
            print("pin", x.pin)
            print("balance", x.balance)
    elif user_choice == "0":
        print("Bye!")
        break
    else:
        print("wrong number")
