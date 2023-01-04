from MySQLdb import *
from time import sleep

PSWRD = "Ballav@123"
PIN = 9024


# display

def display():
    print("\t\t\t----------------------------------------------------------------")
    print("\t\t\t----------------------WELCOME TO BK'S BANK----------------------")
    print("\t\t\t----------------------------------------------------------------")
    print("\n")
    print("\t\t\t---------------------------USER AREA:---------------------------")
    print("\t\t\t\tGIVE THE NUMERIC INPUT TO SELECT THE OPTION:")
    print("\t\t\t\t\t1. CREATE A BANK ACCOUNT")
    print("\t\t\t\t\t2. LOGIN USER")
    print("\t\t\t----------------------------------------------------------------")
    num = int(input("\t\t\tGIVE INPUT: "))

    if num == PIN:
        print("\t\t\t----------------------------------------------------------------")
        print("\n")
        print("\t\t\t--------------------------ADMIN AREA:---------------------------")
        if input("\t\t\t\t\tGIVE THE PASSWORD: ") == PSWRD:
            sleep(2)
            print("\t\t\t\t\t1. SHOW ALL THE ACCOUNT HOLDER DETAILS")
            print("\t\t\t\t\t2. PENALIZE A ACCOUNT")
            print("\t\t\t\t\t3. RESTRICT A ACCOUNT")
            print("\t\t\t----------------------------------------------------------------")
            n = int(input("\t\t\t\t\tPROVIDE THE INPUT: "))

            if n == 1:
                print("\t\t\t----------------------------------------------------------------")
                alldetails()
            elif n == 2:
                print("\t\t\t----------------------------------------------------------------")
                fine()
            elif n == 2:
                print("\t\t\t----------------------------------------------------------------")
                delete()
            else:
                print("\t\t\t----------------------------------------------------------------")
                print("\t\t\t\tWRONG INPUT PRESS 'Y' TO TRY AGAIN FROM START!!!")
        else:
            print("\t\t\t\t\tWRONG USER PASSWORD")
    elif num == 1:
        user_details()
    elif num == 2:
        login()
    else:
        print("\t\t\t\tERROR INPUT PLEASE TRY AGAIN!!!!")


# create account

def user_details():
    print("\t\t\t----------------------------------------------------------------")
    print("\t\t\t\tACCOUNT CREATION")
    sleep(2)
    fname = input("\t\t\t\t⁕ GIVE THE USER FIRST NAME:")
    sleep(2)
    lname = input("\t\t\t\t⁕ GIVE THE USER LAST NAME:")
    sleep(2)
    phno = int(input("\t\t\t\t⁕ GIVE THE USER PHONE NUMBER:"))
    sleep(2)
    adres = input("\t\t\t\t⁕ GIVE THE USER ADDRESS:")

    conn = connect(host="localhost", database="bitu", user="root", password="Ballav@123")
    cur = conn.cursor()

    import random

    rand = random.randint(0, 99999999999)

    arg = (fname, lname, phno, adres, rand)

    print("\n\t\t\t\tPROCESSING.........\n")
    try:
        cur.execute(f"insert into userdetails(FNAME, LNAME, PHONE_NO, ADDRESS, ACCOUNT_NO) values{arg}")
        conn.commit()
        sleep(4)
        print("ACCOUNT OPENED!")
    except:
        conn.rollback()
        print("COULDN'T OPEN ACCOUNT")
    finally:
        print(print("\t\t\t----------------------------------------------------------------"))
        cur.close()
        conn.close()

    bankdetails(rand)


# PIN GENERATION

def bankdetails(accno):
    print("\t\t\t----------------------------------------------------------------")
    print("\t\t\t\tPIN GENERATION:")
    num = int(input(f"\t\t\t\tGIVE THE 6 DIGIT PIN FOR YOUR BANK ACCOUNT NO {accno}: "))
    num1 = int(input("\t\t\t\tRE-ENTER THE PIN: "))
    if num == num1:
        print("\t\t\t----------------------------------------------------------------")
        print("\t\t\t\tPIN GENERATED!")
        print("\t\t\t----------------------------------------------------------------")
        bal = int(input("\t\t\t\tGIVE THE AMOUNT YOU WANT TO SAVE IN YOUR ACCOUNT"))

        conn = connect(host="localhost", database="bitu", user="root", password="Ballav@123")
        cur = conn.cursor()

        arg = (accno, bal, num)

        try:
            cur.execute(f"insert into bankdetail(ACCOUNT_NO, BALANCE, PIN) values{arg}")
            conn.commit()
        except:
            conn.rollback()
            print("TERMINATION ERROR!")
        finally:
            print(print("\t\t\t----------------------------------------------------------------"))
            cur.close()
            conn.close()

    else:
        inp = input("\t\t\t\tWRONG PIN INPUT, PRESS 'Y' TO TRY AGAIN: ")
        if inp == "Y" or inp == "y":
            bankdetails(accno)
        else:
            return


# login

def login():
    print("\t\t\t----------------------------------------------------------------")
    print("\t\t\t\tUSER LOGIN")
    print("\t\t\t----------------------------------------------------------------")
    name = input("\t\t\t\tGIVE THE USER NAME: ")

    conn = connect(host="localhost", database="bitu", user="root", password="Ballav@123")
    cur = conn.cursor()

    try:
        cur.execute(
            f"select pin from bankdetail where ACCOUNT_NO in (select ACCOUNT_NO from userdetails where FNAME = '{name}')")
        row = cur.fetchone()
        pin = row[0]
    except:
        conn.rollback()
        print("\t\t\t\tUNKNOWN USER!!")
    finally:
        print("\t\t\t----------------------------------------------------------------")
        cur.close()
        conn.close()

    pin1 = int(input("\t\t\t\tGIVE THE USER PIN: "))

    if pin1 == pin:
        sleep(2)
        changes(name)
    else:
        sleep(2)
        inp = input("\t\t\t\tINCORRECT PIN PRESS 'Y' TO TRY AGAIN: ")
        if inp == "Y" or inp == "y":
            login()
        else:
            return


def changes(name):
    print("\t\t\t----------------------------------------------------------------")
    print(f"\t\t\t-------------------WELCOME USER {name}--------------------------")
    print("\t\t\t----------------------------------------------------------------")
    sleep(3)
    print("\t\t\tSELECT THE INPUT YOU WANT: ")
    sleep(1)
    print("\t\t\t\t\t1. CREDIT AMOUNT")
    print("\t\t\t\t\t2. DEBIT AMOUNT")
    print("\t\t\t\t\t3. BALANCE INQUIRY")
    sleep(1)
    num = int(input("\t\t\t\tGIVE THE INPUT: "))
    if num == 1:
        credit(name)
    elif num == 2:
        debit(name)
    elif num == 3:
        balance(name)
    elif num == 4:
        transfer(name)
    else:
        sleep(2)
        inp = input("\t\t\t\tINCORRECT USER SELECTION! PRESS 'Y' TO TRY AGAIN: ")
        if inp == "Y" or inp == "y":
            changes(name)
        else:
            return


# debiting money
def debit(name):
    conn = connect(host="localhost", database="bitu", user="root", password="Ballav@123")
    cur = conn.cursor()

    cur.execute(
        f"select balance from bankdetail where ACCOUNT_NO in (select ACCOUNT_NO from userdetails where FNAME = '{name}')")

    row = cur.fetchone()
    bal = row[0]
    print("\t\t\t----------------------------------------------------------------")
    sleep(2)
    amm = int(input("\t\t\t\tHOW MUCH MONEY YOU WANT TO WITHDRAW: "))
    if amm > bal:
        sleep(2)
        print("\t\t\t\tINSUFFICIENT BALANCE!!")
    else:
        sleep(2)
        bal = bal - amm

        cur.execute(f"update bankdetail set balance = {bal} where account_no in (select account_no from userdetails "
                    f"where fname = '{name}') ")
        conn.commit()

        print(f"\t\t\t\t{amm} AMOUNT WAS WITHDRAWN AND YOUR NEW BALANCE IS {bal}")

    cur.close()
    conn.close()


# crediting money
def credit(name):
    conn = connect(host="localhost", database="bitu", user="root", password="Ballav@123")
    cur = conn.cursor()

    cur.execute(
        f"select balance from bankdetail where ACCOUNT_NO in (select ACCOUNT_NO from userdetails where FNAME = '{name}')")
    row = cur.fetchone()
    bal = row[0]
    print("\t\t\t----------------------------------------------------------------\n")
    sleep(2)
    amm = int(input("\t\t\t\tHOW MUCH MONEY YOU WANT TO DEPOSIT: "))
    bal = bal + amm

    cur.execute(f"update bankdetail set balance = {bal} where account_no in (select account_no from userdetails "
                f"where fname = '{name}') ")
    conn.commit()
    sleep(2)
    print(f"\t\t\t\t{amm} AMOUNT WAS ADDED AND YOUR NEW BALANCE IS {bal}")

    cur.close()
    conn.close()


# balance check
def balance(name):
    conn = connect(host="localhost", database="bitu", user="root", password="Ballav@123")
    cur = conn.cursor()

    cur.execute(
        f"select balance from bankdetail where ACCOUNT_NO in (select ACCOUNT_NO from userdetails where FNAME = '{name}')")
    row = cur.fetchone()
    bal = row[0]
    print("\t\t\t----------------------------------------------------------------")
    cur.close()
    conn.close()
    sleep(2)
    print(f"\t\t\t\tYOUR BALANCE IS {bal}")


# money transfer to another user in the same bank
def transfer(name):
    print(print("\t\t\t----------------------------------------------------------------"))
    sleep(2)
    nam1 = input("\t\t\t\tMONEY RECEIVER'S USER NAME: ")
    conn = connect(host="localhost", database="bitu", user="root", password="Ballav@123")
    cur = conn.cursor()

    cur.execute(
        f"select balance from bankdetail where ACCOUNT_NO in (select ACCOUNT_NO from userdetails where FNAME = '{nam1}')")
    row = cur.fetchone()
    if row is None:
        sleep(2)
        inp = input("\t\t\t\tINCORRECT USER!!PRESS 'Y' TO TRY AGAIN: ")
        if inp == "Y" or inp == "y":
            transfer()
        else:
            return

    else:
        sleep(2)
        bal1 = row[0]

        cur.execute(
            f"select balance from bankdetail where ACCOUNT_NO in (select ACCOUNT_NO from userdetails where FNAME = '{name}')")
        row = cur.fetchone()
        bal = row[0]
        sleep(1)
        amm = int(input("\t\t\t\tGIVE THE AMOUNT TO BE TRANSFERRED: "))
        if amm > bal:
            sleep(1)
            print("\t\t\t\tINSUFFICIENT BALANCE!!!!")
        else:
            bal = bal - amm
            sleep(1)
        try:
            cur.execute(
                f"update bankdetail set balance = {bal} where account_no in (select account_no from userdetails "
                f"where fname = '{name}') ")
            conn.commit()
            print("\t\t\t\tMONEY HAS BEEN PROCESSED!!")
            sleep(2)
            try:
                cur.execute(f"update bankdetail set balance = {bal1 + amm} where account_no in (select account_no "
                            f"from userdetails where fname = '{nam1}') ")
                conn.commit()
                print("\t\t\t\tMONEY HAS BEEN TRANSFERRED!!")
            except:
                conn.rollback()
                print("\t\t\t\tTRANSFER ISSUES DETECTED!!")
        except:
            conn.rollback()
            print("\t\t\t\tINTERNAL ISSUES DETECTED!!")
        finally:
            print(print("\t\t\t----------------------------------------------------------------"))
            cur.close()
            conn.close()


def alldetails():
    bankpswrd = "Rourkela@769012"
    pswrd = input("\t\t\t\tGIVE THE BANK ADMIN PASSWORD: ")
    if bankpswrd == pswrd:
        conn = connect(host="localhost", database="bitu", user="root", password="Ballav@123")
        cur = conn.cursor()

        cur.execute(
            f"select * from bankdetail, userdetails where userdetails.account_no =bankdetail.account_no ")
        row = cur.fetchall()
        sleep(2)
        print("\t\t\t----------------------------------------------------------------")
        print("{:<14}{:<12}{:<6}{:<12}{:<12}{:<15}{:<20}".format("ACCOUNT NO.", "BALANCE", "PIN", "FNAME", "LNAME",
                                                                 "PHONE NO.", "ADDRESS\n"))
        for i in row:
            sleep(1)
            print("{:<14}{:<12}{:<6}{:<12}{:<12}{:<15}{:<20}".format(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
        print("\t\t\t----------------------------------------------------------------")
        cur.close()
        conn.close()
    else:
        print("\t\t\t----------------------------------------------------------------")
        sleep(1)
        t = input("\t\t\t\tWRONG PASSWORD PRESS 'Y' TO TRY AGAIN: ")
        if t == 'Y' or t == 'y':
            alldetails()
        else:
            print("\t\t\t----------------------------------------------------------------")
            return


def fine():
    pswrd = input("\t\t\t\tGIVE THE BANK ADMIN PASSWORD: ")
    bankpswrd = "Rourkela@769012"
    if bankpswrd == pswrd:
        conn = connect(host="localhost", database="bitu", user="root", password="Ballav@123")
        cur = conn.cursor()

        nam = input("\t\t\t\tWHICH USER YOU WANT TO FINE: ")

        cur.execute(
            f"select balance from bankdetail where ACCOUNT_NO in (select ACCOUNT_NO from userdetails where FNAME = '{nam}')")
        row = cur.fetchone()
        if row is None:

            print("\t\t\t----------------------------------------------------------------")
            sleep(2)
            t = input("\t\t\t\tINCORRECT USER!! PRESS 'Y' TO TRY AGAIN: ")
            if t == 'Y' or t == 'y':
                fine()
            else:
                print("\t\t\t----------------------------------------------------------------")
                return
        else:
            sleep(2)
            amm = int(input("\t\t\t\tHOW MUCH AMOUNT YOU WANT TO FINE: "))
            sleep(1)
            pin = int(input("\t\t\t\tGIVE THE ADMIN PIN:"))
            if pin == PIN:
                cur.execute(
                    f"select balance from bankdetail where ACCOUNT_NO in (select ACCOUNT_NO from userdetails where "
                    f"FNAME = '{nam}')")
                row = cur.fetchone()
                bal = row[0]

                cur.execute(
                    f"update bankdetail set balance = {bal - amm} where account_no in (select account_no from "
                    f"userdetails where fname = '{nam}') ")
                conn.commit()
                sleep(1)
                print("\t\t\t----------------------------------------------------------------")
                sleep(1)
                print("\t\t\t\tMONEY HAS BEEN PENALIZED!!")
                print("\t\t\t----------------------------------------------------------------")
        cur.close()
        conn.close()


def delete():
    pswrd = input("\t\t\t\tGIVE THE BANK ADMIN PASSWORD: ")
    bankpswrd = "Rourkela@769012"
    if bankpswrd == pswrd:
        conn = connect(host="localhost", database="bitu", user="root", password="Ballav@123")
        cur = conn.cursor()

        nam = input("\t\t\t\tWHICH USER YOU WANT TO DELETE: ")
        sleep(2)
        try:
            cur.execute(f"delete from userdetails where FNAME = '{nam}')")
            print("\t\t\t----------------------------------------------------------------")
            sleep(1)
            print("\t\t\t\tACCOUNT REMOVED PERMANENTLY!!")
            print("\t\t\t----------------------------------------------------------------")
            conn.commit()
        except:
            sleep(1)
            conn.rollback()
            print("\t\t\t----------------------------------------------------------------")
            print("\t\t\t\tTERMINATION ERROR!!")
            print("\t\t\t----------------------------------------------------------------")

        cur.close()
        conn.close()
    else:
        print("\t\t\t----------------------------------------------------------------")
        sleep(1)
        inp = input("\t\t\t\tWRONG PASSWORD!! PRESS 'Y' TO TRY AGAIN: ")
        print("\t\t\t----------------------------------------------------------------")
        if inp == "Y" or inp == "y":
            delete()


if __name__ == "__main__":
    display()
