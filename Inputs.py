# File: Inputs.py
# Author: Karston Kelly  
# Date: 4/17/21
# Description: Inputs for defining a user and adding to an audit log

class Inputs:
    def __init__(self,username,password,database):
        self.username = username
        self.password = password
        self.database = database
        self.admin = False
        self.log = []

    def log_entry(self,logentry):
        if len(self.log) == 512:
            del self.log[0]
            self.log.append(logentry)
        else:
            self.log.append(logentry)