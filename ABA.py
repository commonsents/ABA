# File: ABA.py
# Author: Karston Kelly  
# Date: 
# Description: Implementation of Address Book Appliance
import sys
import csv
import pickle 
import os.path
from os import path
from Account_Entry import *
from Authentication import *

version_Num = "1.1"
command_List = {"HLP": 1, "LIN": 2, "LOU": 3, "EXT": 4, "IMD": 5, "CHP": 6, "ADU": 7, "DEU": 8, "LSU": 9, "DAL": 10, "ADR": 11, "DER": 12, "EDR": 13, "RER": 14, "EXD": 15}
address_book_file = "testDB.csv"


#Admin of 0 means that a user is not logged into an administrator account. 
#This is default and resets at the start of the program
admin = "0"

#Format = recordID:Data, ...
compiled_addr_book = []


#Command that chooses which response to take based on input received from user. 
def chooseResponse(userInput):
    #userInput is split by word, userInput[0] represents the command while 
    #userInput[1] or more represents any arguments required for the command

    if(command_List.get(userInput[0]) == 1):
        #HLP Command
        if len(userInput)>1:
            help(userInput[1])
        else:
            help()

    elif(command_List.get(userInput[0]) == 2):
        #Login Command
        #LIN(userID)

        #if len(userInput)> 1:
        #   LIN(userInput[1])
        if len(userInput) > 1:
            authenticate.login(userInput[1])
        else:
            print("\nPlease specify userID.\n")
            ABA()

    elif(command_List.get(userInput[0]) == 3):
        #Logout Command
        #LOU()
        if len(userInput) == 1:
            authenticate.logout()
        else:
            print("\nInvalid format. See 'HLP' command for required inputs for the 'CHP' command.\n")
        #print("LO")

    elif(command_List.get(userInput[0]) == 4):
        #EXT Command
        print("Thank you for using ABA.")
        quit()

    elif(command_List.get(userInput[0]) == 5):
        #IMD command
        #Need to check for length on document
        if len(userInput)>1:
            IMD(userInput[1])
        else:
            print("No Input_File specified.")

    elif(command_List.get(userInput[0]) == 6):
        #CHP()
        if len(userInput) == 2:
            authenticate.change_password(userInput[1])
        else:
            print("\nInvalid format. See 'HLP' command for required inputs for the 'CHP' command.\n")

    elif(command_List.get(userInput[0]) == 7):
        #ADU()
        if len(userInput) == 2:
            authenticate.add_user(userInput[1])
        else:
            print("\nInvalid format. See 'HLP' command for required inputs for the 'ADU' command.\n")
        
    elif(command_List.get(userInput[0]) == 8):
        #DEU()
        if len(userInput) == 2:
            authenticate.delete_user(userInput[1])
        else:
            print("\nInvalid format. See 'HLP' command for required inputs for the 'DEU' command.\n")

    elif(command_List.get(userInput[0]) == 9):
        #LSU()
        quit()

    elif(command_List.get(userInput[0]) == 10):
        #DAL
        quit()

    elif(command_List.get(userInput[0]) == 11):
        #ADR
        #Addrecord function
        ADR(userInput)

    elif(command_List.get(userInput[0]) == 12):
        #DER
        DER(userInput)
        
    elif(command_List.get(userInput[0]) == 13):
        #EDR
        EDR(userInput)

    elif(command_List.get(userInput[0]) == 14):
        #RER
        quit()

    elif(command_List.get(userInput[0]) == 15):
        #EXD
        if len(userInput)>1:
            EXD(userInput)
        else:
            print("No Input_file specified")

    else:
        print("Command not found. Type \"HLP\" for a list of commands.")



def help(cmd = ""):
    if cmd == "":
        print("Login: LIN <userID>\n"
              "Logout: LOU\n"
              "Change Password: CHP <old password>\n"
              "Add User: ADU <userID>\n"
              "Delete User: DEU <userID>\n"
              "List Users: LSU \n"
              "Display Audit Log: DAL [<userID>]\n"
              "Add Record: ADR <recordID> [<field1=value1> <field2=value2> ...]\n"
              "Delete Record: DER <recordID>\n"
              "Edit Record: EDR <recordID> <field1=value1> [<field2=value2> ...]\n"
              "Read Record: RER [<recordID>] [<fieldname> ...]\n"
              "Import Database: IMD <Input_File>\n"
              "Export Database: EXD <Output_file>\n"
              "Help: HLP [<command name>]\n"
              "Exit: EXT\n")
    elif cmd == "LIN":
        print("Login: LIN <userID>\n")
    elif cmd == "LOU":
        print("Logout: LOU\n")
    elif cmd == "CHP":
        print("Change Password: CHP <old password>\n")
    elif cmd == "ADU":
        print("Add User: ADU <userID\n")
    elif cmd == "DEU":
        print("Delete User: DEU <userID>\n")
    elif cmd == "ADR":
        print("Add Record: ADR <recordID> [<field1=value1> <field2=value2> ...\n")
    elif cmd == "DER":
        print("Delete Record: DER <recordID>\n")
    elif cmd == "EDR":
        print("Edit Record: EDR <recordID> <field1=value1> [<field2=value2> ...]\n")
    elif cmd == "RED":
        print("Read Record: RER [<recordID>] [<fieldname> ...]\n")
    elif cmd == "IMD":
        print("Import Database: IMD <Input_File>\n")
    elif cmd == "EXD":
        print("Export Database: EXD <Output_file>\n")
    elif cmd == "HLP":
        print("Help: HLP [<command name>]\n")
    elif cmd == "EXT":
        print("Exit: EXT\n")
    else:
        print("no such instructions exists.")



def IMD(filename):
    #Reads in input from specified .csv file. Currently seperates by commas. 
    with open(filename,'rt') as f:
        data = csv.reader(f)
        for row in data:
            new_entry = Account_Entry(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11])
            compiled_addr_book.append(new_entry)
    print("Address Book Import Complete.")


def ADR(userInput):
    val = {"SN": 1, "GN":2,"PEM":3, "WEM":4,"PPH":5,"WPH":6, "SA":7, "CITY":8, "STP": 9, "CTY":10, "PC":11}
    account_items = [userInput[1],"","","","","","","","","","",""]
    for x in range(2,len(userInput)):
        #Should have strings in format value=newval
        nextVal = userInput[x].split("=")
        if nextVal[0] in val:
            account_items[val.get(nextVal[0])] = nextVal[1]
    new_entry = Account_Entry(account_items[0],account_items[1],account_items[2],account_items[3],account_items[4],account_items[5],account_items[6],account_items[7],account_items[8],account_items[9],account_items[10],account_items[11])
    compiled_addr_book.append(new_entry)
    print("OK")
    return()


def DER(userInput):
    for x in range(len(compiled_addr_book)):
        if userInput[1] == compiled_addr_book[x].recordID:
            compiled_addr_book.remove(compiled_addr_book[x])
            print("OK")
            return()

def EDR(userInput):
    val = {"SN": 1, "GN":2,"PEM":3, "WEM":4,"PPH":5,"WPH":6, "SA":7, "CITY":8, "STP": 9, "CTY":10, "PC":11}
    for x in range(len(compiled_addr_book)):
        if userInput[1] == compiled_addr_book[x].recordID:
            for y in range(2, len(userInput)):
                nextVal = userInput[y].split("=")
                if nextVal[0] in val:
                    print(nextVal[0] + " " + nextVal[1])
                    print(compiled_addr_book[x].GN)
                    setattr(compiled_addr_book[x], nextVal[0], nextVal[1])
                    print(compiled_addr_book[x].GN)
                    print("OK")
                    return()



def EXD(userInput):
    f = open(userInput[1]+ ".csv", "w+")
    outString = ""
    for x in compiled_addr_book:
        outString += x.recordID + "," + x.SN + "," + x.GN + "," + x.PEM + "," \
            + x.WEM + "," + x.PPH + "," + x.WPH + "," + x.SA + "," + x.CITY + "," + x.STP + "," + x.CTY + "," + x.PC + ",\n"
        f.write(outString)
        outString = ""
    print("OK")
    return()



def ABA():
    print("Address Book Application, version ", version_Num, ". Type \"HLP\" for a list of commands.")
    while(True):
        input1 = str(input())
        if(input1 != ""):
            input1 = str.split(input1)
            chooseResponse(input1)
        else:
            print("\nPlease enter a command.\n")


if __name__ == "__main__":
    authenticate = Authentication()
    if path.isfile('DatabaseStorage') == True:
        try:
            storageFile = open('DatabaseStorage', 'rb')
            authenticate = pickle.load(storageFile)
        except pickle.PickleError:
            None
    if type(authenticate) != Authentication:
        authenticate = Authentication()
    if len(authenticate.dictionary) == 0:
        print("You need to create an admin account to use the ABA.")
        print("\nCreate a unique userID. ID may contain 1-16 upper- or lower-case letters or numbers.\n")
        username = input("Choose a username for the admin account: ")
        authenticate.first_admin(username)
    
    ABA()