# File: Authentication.py
# Author: Matt Willis  
# Date: 4/17/21
# Description: Login, Logout, Change Password commands handled
#from passlib.hash import pbkdf2_sha256 # from the passlib library. download with "pip install passlib" in terminal
import datetime
import re
import csv
from csv import writer
from Inputs import *

class Authentication:
    def __init__(self):
        self.dictionary = {} # dictionary to map usernames to accounts
        self.saved_data = {} # data from previous sessions loaded in to this dictionary upon start of program
        #self.password_dict = {} # temporary non-security driven storage for passwords; will be changed upon further implementation
        self.active_user = 0 # 0 = no active user
        self.cur_user = ""
    
    def first_admin(self,userID):
        username = self.check_username(userID)
        self.cur_user = username
        password = self.create_password() # still need to implement a hash/encryption method for storing passwords
        init_account = Inputs(username,password,self)
        self.saved_data[username] = password
        self.dictionary[username] = init_account
        self.dictionary[username].admin = True
        self.active_user = self.dictionary[username]
        self.dictionary[username].log_entry(str(datetime.datetime.now()) + ", AU, " + self.active_user.username)
        self.dictionary[username].log_entry(str(datetime.datetime.now()) + ", L1, " + username)
        self.dictionary[username].log_entry(str(datetime.datetime.now()) + ", LS, " + username)
        print("Welcome, " + self.active_user.username + " is now logged in.\n")
        data = open('permissions.csv', 'w')
        info = ""
        info += username + "," + password + "," + "admin" + "\n"
        data.write(info)
        data.close()

        
    def first_login(self,username):
        print("\nThis is the first time this account is being used. You must create a new password.\n")
        password = self.create_password()
        full_account = Inputs(username, password, self) # update the definition of the user to include the password associated with the userID to be stored
        self.dictionary[username] = full_account
        self.saved_data[username] = password
        self.active_user = self.dictionary[username]
        updated_list = []
        with open('permissions.csv', 'r') as b:
            update = csv.reader(b)
            updated_list.extend(update)
        updated_line = {self.active_user.username:password}
        with open('permissions.csv', 'w') as b:
            writer = csv.writer(b)
            for line, row in enumerate(updated_list):
                data = updated_line.get(line, row)
                print(data)
                writer.writerow(data)
        self.cur_user = username
        print("Active user now is : " + username + "\n")
        self.dictionary[username].log_entry(str(datetime.datetime.now()) + ", L1, " + username)
        self.dictionary[username].log_entry(str(datetime.datetime.now()) + ", LS, " + username)

    def login(self, username):
        # check if there is an active user
        if self.active_user != 0:
            print("\nAn account is currently active; logout before proceeding.\n")
        elif username in self.saved_data:
            if self.saved_data[username] == 'temp':
                self.first_login(username)
            else:
                password = input("\nEnter your password: ")
                if not self.validate_creds(username,password):
                    print("\nInvalid credentials.\n")
                    if username in self.dictionary:
                        self.dictionary[username].log_entry(str(datetime.datetime.now()) + ", LF, " + username)
                else:
                    init_account = Inputs(username,password,self)
                    self.dictionary[username] = init_account
                    with open('permissions.csv','r') as f:
                        admin_check = csv.reader(f)
                        for line in admin_check:
                            if line[2] == "admin":
                                self.dictionary[username].admin = True
                                break
                    self.active_user = self.dictionary[username]
                    self.cur_user = username
                    self.dictionary[username].log_entry(str(datetime.datetime.now()) + ", LS, " + self.active_user.username)
                    print("\nOK\n")
        else:
            print("\nCredentials not found.\n")

    def logout(self):
        if self.active_user == 0:
            print("\nThere is currently no active login session.\n")
        else:
            print("\nOK\n")
            self.dictionary[self.active_user.username].log_entry(str(datetime.datetime.now()) + ", LO, " + self.active_user.username)
            self.active_user = 0
            self.cur_user = ""
            print("Logout successful. See you next time!\n")
    

    def change_password(self, old_password):
        # check that the user knows the password before changing it
            if self.active_user == 0:
                print("\nThere is currently no active login session.\n")
            elif self.saved_data[self.active_user.username] !=  old_password:
                print("\nInvalid credentials.\n")
                self.dictionary[self.active_user.username].log_entry(str(datetime.datetime.now()) + ", FPC, " + self.active_user.username)
            else:
                print("\nCreate a new password.")
                new_password = self.create_password()
                if new_password == old_password:
                    print("New password must be different from previous password.\n")
                    new_password = self.create_password()
                self.saved_data[self.active_user.username] = new_password
                updated_list = []
                with open('permissions.csv', 'r') as b:
                    update = csv.reader(b)
                    updated_list.extend(update)
                updated_line = {self.active_user.username:new_password}
                with open('permissions.csv', 'w') as b:
                    writer = csv.writer(b)
                    for line, row in enumerate(updated_list):
                        data = updated_line.get(line, row)
                        print(data)
                        writer.writerow(data)
                self.dictionary[self.active_user.username].log_entry(str(datetime.datetime.now()) + ", SPC, " + self.active_user.username)
                print("Password successfully changed.\n")
    

    def check_username(self,entry):
        username = ""
        while username == "":
            if len(entry) > 16 or len(entry) < 1:
                print("\nUserID contains invalid number of characters.\n")
                entry = input("\nPlease enter a new userID: ")
                username = ""
            else:
                mat = re.fullmatch('[A-Za-z0-9]*', entry)
                if mat:
                    username = entry
                    for account in self.dictionary:
                        if account == entry:
                            print("\nThis userID is already taken.")
                            entry = input("\nPlease enter a new userID: ")
                            username = ""
                else:
                    print("\nUserID contains illegal characters.")
                    entry = input("\nPlease enter a new userID: ")
                    username = ""
        return username


    def create_password(self):
        # call this function when a new user account is created to verify their password input
        print("\nPasswords may contain 8-24 upper- or lower-case letters or numbers. Choose an uncommon password that would be difficult to guess.\n")
        password = ""
        while password == "":
            password = input("Please enter a valid password: ")
            if len(password) > 24 or len(password) < 8:
                print("\nPassword contains invalid number of characters.\n")
                password = ""
            else:
                mat = re.fullmatch('[A-Za-z0-9]+', password)
                if mat:
                    password1 = input("\nReenter the same password: ")
                    if (password == password1):
                        print("\nOK\n")
                        return password
                    else:
                        print("\nPasswords do not match.\n")
                        password = ""
                else:
                    print("\nPassword contains illegal characters.\n")
                    password = ""
                        


    def validate_creds(self,username,password):
        # verify userID is in the dictionary and return index if true and -1 if not found
        if username in self.saved_data:
            if password == self.saved_data[username]:
                return self.saved_data[username]
        else:
            return False
    

    def add_user(self, username):
        if len(self.dictionary) == 8:
            print("\nMaximum amount of users reached. You cannot any add more users until at least one is deleted\n")
        elif type(self.active_user) == Inputs and self.active_user.admin:
            username = self.check_username(username)
            init_account = Inputs(username, None, self)
            self.dictionary[username] = init_account
            self.saved_data[username] = 'temp'      # saved as 'temp' as to trigger first_login call upon the first login of the new user
            temp_list = [username, 'temp','user']   # create a temporary password & define as user
            with open('permissions.csv', 'a') as user:
                    update = writer(user)
                    update.writerow(temp_list)
            print("\nOK\n")
            self.dictionary[username].log_entry(str(datetime.datetime.now()) + ", AU, " + self.active_user.username)
        else:
            print("\nAdmin account must be active\n")

    # Only admin can delete user accounts
    def delete_user(self, username):
        if self.active_user == 0:
            print("\nAdmin account must be active\n")
        elif not self.active_user.admin:
            print("\nAdmin account must be active\n")
        elif username in self.dictionary and type(self.active_user) == Inputs and self.active_user.admin:
            if self.active_user.username == username:
                print("\nAn admin account cannot delete itself\n")
            else:
                del self.dictionary[username]
                deleted_user_file = []
                with open('permissions.csv', 'r') as readFile:
                    reader = csv.reader(readFile)
                    for row in reader:
                        deleted_user_file.append(row)
                        for field in row:
                            if field == username:
                                deleted_user_file.remove(row)
                with open('permissions.csv', 'w') as writeFile:
                    writer = csv.writer(writeFile)
                    writer.writerows(deleted_user_file)
                self.active_user.log_entry(str(datetime.datetime.now()) + ", DU, " + self.active_user.username)
                print("\nOK, user successfully deleted\n")

        else:
            print("\nUser " + username + " does not exist\n")

    def list_users(self):
        if self.active_user == 0:
            print("\nThere is currently no active login session.\n")
        elif not self.active_user.admin:
            print("\nAdmin account must be active\n")
        else:
            print("\nOK\n")
            for i in self.dictionary:
                print(self.dictionary.keys() +"\n")
                print(self.dictionary.keys(i) +"\n")

