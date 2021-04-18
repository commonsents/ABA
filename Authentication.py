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
        self.active_user == 0 # 0 = no active user
    
    def first_admin(self):
        username = self.check_username()
        password = self.create_password() # still need to implement a hash/encryption method for storing passwords
        init_account = Inputs(username,password,self)
        self.password_dict[username] = password
        self.dictionary[username] = init_account
        self.dictionary[username].admin = True
        self.active_user = self.dictionary[username]
        self.dictionary[username].add_log(str(datetime.datetime.now()) + ", AU, " + self.active_user.username)
        self.dictionary[username].add_log(str(datetime.datetime.now()) + ", L1, " + username)
        self.dictionary[username].add_log(str(datetime.datetime.now()) + ", LS, " + username)


    def login(self, username, password):
        # check if there is an active user
        if self.active_user != 0:
            print("An account is currently active; logout before proceeding.\n")
        else:
            if not self.validate_creds(username,password):
                print("Invalid credentials.\n")
                if username in self.dictionary:
                    self.dictionary[username].add_log(str(datetime.datetime.now()) + ", LF, " + username)
            else:
                self.active_user = self.dictionary[username]
                self.dictionary[username].add_log(str(datetime.datetime.now()) + ", LS, " + self.active_user.username)
                print("OK")
    
    def check_username(self):
        print("Create a unique userID containing 1-16 characters composed of upper- or -lowercase letters, or numbers.\n")
        username = ""
        while username == "":
            username = input("Enter valid userID: ")
            if len(username) > 16 or len(username) < 1:
                print("UserID contains invalid number of characters.\n")
                self.check_username()
            else:
                reg = "[A-Za-z0-9*]"
                pat = re.compile(reg)
                mat = re.search(pat,username)
                if mat:
                    for account in self.dictionary:
                        if account == username:
                            print("This userID is already taken.\n")
                            self.check_username()
        return username


    def create_password(self):
        # call this function when a new user account is created to verify their password input
        print("This is the first time the account is being used. You must create a new password. Passwords may contain 1-24 upper- or lower-case letters or numbers. Choose an uncommon password that would be difficult to guess.\n")
        password = ""
        while password == "":
            password = input("Please enter a valid password: ")
            if len(password) > 24 or len(password) < 1:
                print("Password contains invalid number of characters.\n")
                self.create_password()
            #checking password validation
            reg = "[A-Za-z0-9*]"
            pat = re.compile(reg)
            mat = re.search(pat,password)
            if mat:
                password1 = input("Reenter the same password: ")
                if (password == password1):
                    print("OK")
                    return password
                else:
                    print("Passwords do not match\n")
                    self.create_password()
            else:
                print("Password contains illegal characters\n")
                self.create_password()
                    


    def validate_creds(self,username,password):
        # verify userID is in the dictionary and return index if true and -1 if not found
        if username in self.dictionary:
            return self.password_dict[self.dictionary[username]]
        else:
            return False