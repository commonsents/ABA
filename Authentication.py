# File: Authentication.py
# Author: Matt Willis  
# Date: 
# Description: Login, Logout, Change Password commands handled
#from passlib.hash import pbkdf2_sha256 # from the passlib library. download with "pip install passlib" in terminal
import datetime
import re

class Authentication:
    def __init__(self):
        self.dictionary = {} # dictionary to map usernames to accounts
        self.password_dict = {} # temporary non-security driven storage for passwords; will be changed upon further implementation
        self.active_user == 0 # 0 = no active user
    
    #def add_user(self,username):
        

    def login(self, username, password):
        # check if there is an active user
        if self.active_user != 0:
            print("An account is currently active; logout before proceeding")
        else:
            if not self.validate_creds(username,password):
                print("Invalid credentials")
                if username in self.dictionary:
                    self.dictionary[username].add_log(str(datetime.datetime.now()) + ", LF, " + username)
            else:
                self.active_user = self.dictionary[username]
                self.dictionary[username].add_log(str(datetime.datetime.now()) + ", LS, " + self.active_user.username)
                print("OK")
    
    def check_password(self):
        # call this function when a new user account is created to verify their password input
        print("This is the first time the account is being used. You must create a new password. Passwords may contain 1-24 upper- or lower-case letters or numbers. Choose an uncommon password that would be difficult to guess.")
        password = ""
        while password == "":
            password = input("Please enter a valid password: ")
            if (len(password) > 24):
                print("Password contains too many characters")
                self.check_password()
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
                    print("Passwords do not match")
                    self.check_password()
            else:
                print("Password contains illegal characters")
                self.check_password()
                    


    def validate_creds(self,username,password):
        # verify userID is in the dictionary and return index if true and -1 if not found
        if username in self.dictionary:
            return self.password_dict[self.dictionary[username]]
        else:
            return False