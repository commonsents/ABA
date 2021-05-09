# File: Authentication.py
# Author: Matt Willis  
# Date: 4/17/21
# Description: Login, Logout, Change Password commands handled
#from passlib.hash import pbkdf2_sha256 # from the passlib library. download with "pip install passlib" in terminal
import datetime
import re
import csv
import os.path
from os import path
from csv import writer
from AuditRecord import *
from ABA import cur_audit_log
from Inputs import *

class Authentication:
    def __init__(self):
        self.dictionary = {} # dictionary to map usernames to accounts
        self.saved_data = {} # data from previous sessions loaded in to this dictionary upon start of program
        #self.password_dict = {} # temporary non-security driven storage for passwords; will be changed upon further implementation
        self.active_user = 0 # 0 = no active user
        self.cur_user = ""
    
    def first_admin(self,userID,cur_audit_log):
        username = self.check_username(userID)
        self.cur_user = username
        password = self.create_password() # still need to implement a hash/encryption method for storing passwords
        init_account = Inputs(username,password,self)
        self.saved_data[username] = password
        self.dictionary[username] = init_account
        self.dictionary[username].admin = True
        self.active_user = self.dictionary[username]
        AddAuditRecord(cur_audit_log,"AU", self.cur_user)
        AddAuditRecord(cur_audit_log,"L1", self.cur_user)
        AddAuditRecord(cur_audit_log,"LS", self.cur_user)
        SaveAuditLogs(cur_audit_log)
        if path.exists("permissions.csv"):
            with open("permissions.csv",'rt') as f:
                data = csv.reader(f)
                info = ""
                info += username + "," + password + "," + "admin" + "\n"
                data.write(info)
                data.close()
        else:
            with open("permissions.csv", "w") as fp:
                pass
            fp.close()

        
    def first_login(self,username,cur_audit_log):
        password = self.create_password()
        full_account = Inputs(username, password, self) # update the definition of the user to include the password associated with the userID to be stored
        self.dictionary[username] = full_account
        self.saved_data[username] = password
        self.active_user = self.dictionary[username]
        updated_user_file = []
        with open('permissions.csv', 'r+') as readFile:
            reader = csv.reader(readFile)
            for row in reader:
                updated_user_file.append(row)
                for field in row:
                    if field == self.active_user.username:
                        updated_user_file.remove(row)
        if self.active_user.admin:
            new_info = [self.active_user.username, password,'admin']
        else:
            new_info = [self.active_user.username, password,'user']
        with open('permissions.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(updated_user_file)
            writer.writerow(new_info)
        self.cur_user = username
        print("\nOK\n")
        AddAuditRecord(cur_audit_log,"L1", self.cur_user)
        AddAuditRecord(cur_audit_log,"LS", self.cur_user)
        SaveAuditLogs(cur_audit_log)

    def login(self, username,cur_audit_log):
        # check if there is an active user
        if self.active_user != 0:
            print("\nAn account is currently active; logout before proceeding.\n")
        elif username in self.saved_data:
            if self.saved_data[username] == 'temp':
                self.first_login(username,cur_audit_log)
            else:
                password = input("\nEnter your password: ")
                if not self.validate_creds(username,password):
                    print("\nInvalid credentials.\n")
                    if username in self.dictionary:
                        AddAuditRecord(cur_audit_log,"LF", username)
                        SaveAuditLogs(cur_audit_log)
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
                    print("\nOK\n")
                    AddAuditRecord(cur_audit_log,"LS", self.cur_user)
                    SaveAuditLogs(cur_audit_log)
        else:
            print("\nInvalid credentials.\n")

    def logout(self,cur_audit_log):
        if self.active_user == 0:
            print("\nThere is currently no active login session.\n")
        else:
            print("\nOK\n")
            self.active_user = 0
            AddAuditRecord(cur_audit_log, "LO", self.cur_user)
            SaveAuditLogs(cur_audit_log)
            self.cur_user = ""
    

    def change_password(self, old_password,cur_audit_log):
        # check that the user knows the password before changing it
            if self.active_user == 0:
                print("\nThere is currently no active login session.\n")
            elif self.saved_data[self.active_user.username] !=  old_password:
                print("\nInvalid credentials.\n")
                AddAuditRecord(cur_audit_log,"FPC", self.cur_user)
                SaveAuditLogs(cur_audit_log)
            else:
                print("\nCreate a new password. Passwords may contain up to 24 upper- or lower-case letters or numbers. Choose an uncommon password that would be difficult to guess.\n")
                new_password = self.create_password()
                if new_password == old_password:
                    print("Password is too easy to guess.\n")
                    new_password = self.create_password()
                    AddAuditRecord(cur_audit_log,"FPC", self.cur_user)
                    SaveAuditLogs(cur_audit_log)
                self.saved_data[self.active_user.username] = new_password
                updated_user_file = []
                with open('permissions.csv', 'r+') as readFile:
                    reader = csv.reader(readFile)
                    for row in reader:
                        updated_user_file.append(row)
                        for field in row:
                            if field == self.active_user.username:
                                updated_user_file.remove(row)
                if self.active_user.admin:
                    new_info = [self.active_user.username, new_password,'admin']
                else:
                    new_info = [self.active_user.username, new_password,'user']
                with open('permissions.csv', 'w') as writeFile:
                    writer = csv.writer(writeFile)
                    writer.writerows(updated_user_file)
                    writer.writerow(new_info)
                AddAuditRecord(cur_audit_log,"SPC", self.cur_user)
                SaveAuditLogs(cur_audit_log)
                print("\nOK\n")
    

    def check_username(self,entry):
        username = ""
        while username == "":
            if len(entry) > 16 or len(entry) < 1:
                print("\nUserID contains invalid number of characters.")
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
        print("\nThis is the first time the account is being used. You must create a new password. Passwords may contain 8-24 upper- or lower-case letters or numbers. Choose an uncommon password that would be difficult to guess.\n")
        password = ""
        while password == "":
            password = input("Please enter a valid password: ")
            if len(password) > 24 or len(password) < 8:
                print("\nPassword contains invalid number of characters.")
                password = ""
            else:
                mat = re.fullmatch('[A-Za-z0-9]+', password)
                if mat:
                    password1 = input("\nReenter the same password: ")
                    if (password == password1):
                        print("\nOK\n")
                        return password
                    else:
                        print("\nPasswords do not match.")
                        password = ""
                else:
                    print("\nPassword contains illegal characters.")
                    password = ""
                        


    def validate_creds(self,username,password):
        # verify userID is in the dictionary and return index if true and -1 if not found
        if username in self.saved_data:
            if password == self.saved_data[username]:
                return self.saved_data[username]
        else:
            return False
    

    def add_user(self, username,cur_audit_log):
        if len(self.saved_data) == 8:
            print("\nMaximum amount of users reached. You cannot any add more users until at least one is deleted.")
        elif type(self.active_user) == Inputs and self.active_user.admin:
            username = self.check_username(username)
            init_account = Inputs(username, None, self)
            self.dictionary[username] = init_account
            self.cur_user = username
            self.saved_data[username] = 'temp'      # saved as 'temp' as to trigger first_login call upon the first login of the new user
            temp_list = [username, 'temp','user']   # create a temporary password & define as user
            with open('permissions.csv', 'a') as user:
                    update = writer(user)
                    update.writerow(temp_list)
            print("\nOK")
            AddAuditRecord(cur_audit_log, "AU", self.cur_user)
            SaveAuditLogs(cur_audit_log)
        else:
            print("\nAdmin account must be active")

    # Only admin can delete user accounts
    def delete_user(self, username,cur_audit_log):
        if self.active_user == 0:
            print("\nAdmin account must be active")
        elif not self.active_user.admin:
            print("\nAdmin account must be active")
        elif username in self.saved_data:
            if self.active_user.username == username:
                print("\nAn admin account cannot delete itself")
            else:
                del self.saved_data[username]
                deleted_user_file = []
                with open('permissions.csv', 'r+') as readFile:
                    reader = csv.reader(readFile)
                    for row in reader:
                        deleted_user_file.append(row)
                        for field in row:
                            if field == username:
                                deleted_user_file.remove(row)
                with open('permissions.csv', 'w') as writeFile:
                    writer = csv.writer(writeFile)
                    writer.writerows(deleted_user_file)
                AddAuditRecord(cur_audit_log, "DU", username)
                SaveAuditLogs(cur_audit_log)
                print("\nOK\n")

        else:
            print("\nAccount does not exist")

    def list_users(self):
        if self.active_user == 0:
            print("\nThere is currently no active login session.")
        elif not self.active_user.admin:
            print("\nAdmin account must be active\n")
        else:
            print("\n")
            with open('permissions.csv', 'r') as users:
                contents = csv.reader(users)
                for row in contents:
                    print(row[0] + "\n")

