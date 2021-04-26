# File: Authentication.py
# Author: Matt Willis  
# Date: 4/17/21
# Description: Login, Logout, Change Password commands handled
#from passlib.hash import pbkdf2_sha256 # from the passlib library. download with "pip install passlib" in terminal
import datetime
import re
from Inputs import *

class Authentication:
    def __init__(self):
        self.dictionary = {} # dictionary to map usernames to accounts
        self.password_dict = {} # temporary non-security driven storage for passwords; will be changed upon further implementation
        self.active_user = 0 # 0 = no active user
    
    def first_admin(self,userID):
        username = self.check_username(userID)
        password = self.create_password() # still need to implement a hash/encryption method for storing passwords
        init_account = Inputs(username,password,self)
        self.password_dict[username] = password
        self.dictionary[username] = init_account
        self.dictionary[username].admin = True
        self.active_user = self.dictionary[username]
        self.dictionary[username].log_entry(str(datetime.datetime.now()) + ", AU, " + self.active_user.username)
        self.dictionary[username].log_entry(str(datetime.datetime.now()) + ", L1, " + username)
        self.dictionary[username].log_entry(str(datetime.datetime.now()) + ", LS, " + username)
        print("Welcome, " + self.active_user.username + " is now logged in.\n")
        data = open('permissions.csv', 'w')
        info = ""
        info += username + "," + password + "\n"
        data.write(info)
        data.close()

        
    def first_login(self,username):
        print("\nThis is the first time this account is being used. You must create a new password.\n")
        password = self.create_password()
        full_account = Inputs(username, password, self) # update the definition of the user to include the password associated with the userID to be stored
        self.dictionary[username] = full_account
        self.password_dict[username] = password
        self.active_user = self.dictionary[username]
        print("Active user now is : " + username + "\n")
        self.dictionary[username].log_entry(str(datetime.datetime.now()) + ", L1, " + username)
        self.dictionary[username].log_entry(str(datetime.datetime.now()) + ", LS, " + username)


    def login(self, username):
        # check if there is an active user
        if self.active_user != 0:
            print("\nAn account is currently active; logout before proceeding.\n")
        elif username not in self.password_dict:
            self.first_login(username)
        else:
            password = input("\nEnter your password: ")
            if not self.validate_creds(username,password):
                print("\nInvalid credentials.\n")
                if username in self.dictionary:
                    self.dictionary[username].log_entry(str(datetime.datetime.now()) + ", LF, " + username)
            else:
                self.active_user = self.dictionary[username]
                self.dictionary[username].log_entry(str(datetime.datetime.now()) + ", LS, " + self.active_user.username)
                print("\nOK\n")
    
    def logout(self):
        if self.active_user == 0:
            print("\nThere is currently no active login session.\n")
        else:
            print("\nOK\n")
            self.dictionary[self.active_user.username].log_entry(str(datetime.datetime.now()) + ", LO, " + self.active_user.username)
            self.active_user = 0
            print("Logout successful. See you next time!\n")
    

    def change_password(self, old_password):
        # check that the user knows the password before changing it
            if self.active_user == 0:
                print("\nThere is currently no active login session.\n")
            elif self.password_dict[self.active_user.username] !=  old_password:
                print("\nInvalid credentials.\n")
                self.dictionary[self.active_user.username].log_entry(str(datetime.datetime.now()) + ", FPC, " + self.active_user.username)
            else:
                print("\nCreate a new password.")
                new_password = self.create_password()
                if new_password == old_password:
                    print("New password must be different from previous password.\n")
                    new_password = self.create_password()
                self.password_dict[self.active_user.username] = new_password
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
        if username in self.dictionary:
            if self.password_dict[username] == password:
                return self.password_dict[username]
        else:
            return False
    

    def add_user(self, username):
        if len(self.dictionary) == 8:
            print("\nMaximum amount of users reached. You cannot any add more users until at least one is deleted\n")
        elif type(self.active_user) == Inputs and self.active_user.admin:
            username = self.check_username(username)
            init_account = Inputs(username, None, self)
            self.dictionary[username] = init_account
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