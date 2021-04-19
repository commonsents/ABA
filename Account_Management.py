# File: Account_Management.py
# Author: Andres Mallea  
# Date: 4/18/21
# Description: Add User, Delete User, and List Users commands handled
#from passlib.hash import pbkdf2_sha256 # from the passlib library. download with "pip install passlib" in terminal
import datetime
import re
from Inputs import *


class Account_Management:

    # Only admin can add user accounts
    def add_user(self, username):
        if len(self.dictionary) == 8:
            print("Maximum amount of users reached. You cannot any add more users until at least one is deleted")
        elif type(self.active_user) == Account and self.active_user.admin:
            username = self.choose_name(username)
            password = self.choose_password()
            passwordHash = pbkdf2_sha256.hash(password)     #storing a salted hash of the password
            new_account = Account(username, passwordHash, self)
            self.dictionary[username] = new_account
            self.active_user = self.dictionary[username]  # user is logged in
            print("Active user now is : " + username)
            self.dictionary[username].add_log(str(datetime.datetime.now()) + ", AU, " + self.active_user.username)
            self.dictionary[username].add_log(str(datetime.datetime.now()) + ", L1, " + username)
            self.dictionary[username].add_log(str(datetime.datetime.now()) + ", LS, " + username)
        else:
            print("Admin account must be active")

    # Only admin can delete user accounts
    def delete_user(self, username):
        if self.active_user == 0:
            print("Admin account must be active")
        elif not self.active_user.admin:
            print("Admin account must be active")
        elif username in self.dictionary and type(self.active_user) == Account and self.active_user.admin:
            if self.active_user.username == username:
                print("An admin account cannot delete itself")
            else:
                del self.dictionary[username]
                self.active_user.add_log(str(datetime.datetime.now()) + ", DU, " + self.active_user.username)
                print("OK")
        else:
            print("User " + username + " does not exist")

    def list_users(self):
        #still need to figure out a way to access the database we are using in order to list all usernames