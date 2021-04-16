# File: Account_Entry.py
# Author: Karston Kelly  
# Date: 4/15/21
# Description: Account_Entry Class for Database

class Account_Entry:
    #Class representing data found within each account
    def __init__(self,recordID, SN, GN, PEM, WEM, PPH, WPH, SA, CITY, STP, CTY, PC):
        self.recordID = recordID
        self.SN = SN
        self.GN = GN
        self.PEM = PEM
        self.WEM = WEM
        self.PPH = PPH
        self.WPH = WPH
        self.SA = SA
        self.CITY = CITY
        self.STP = STP
        self.CTY = CTY
        self.PC = PC

    def __str__(self):
        finalString = ""
        if self.recordID != "":
            finalString += self.recordID + " "
        if self.SN != "":
            finalString += "SN=" + self.SN + " "
        if self.GN != "":
            finalString += "GN=" + self.GN + " "
        if self.PEM != "":
            finalString += "PEM=" + self.PEM + " "
        if self.WEM != "":
            finalString += "WEM=" + self.WEM + " "
        if self.PPH != "":
            finalString += "PPH=" + self.PPH + " "
        if self.WPH != "":
            finalString += "WPH=" + self.WPH + " "
        if self.SA != "":
            finalString += "SA=" + self.SA + " "
        if self.CITY != "":
            finalString += "CITY=" + self.CITY + " "
        if self.STP != "":
            finalString += "STP=" + self.STP + " "
        if self.CTY != "":
            finalString += "CTY=" + self.CTY + " "
        if self.PC != "":
            finalString += "PC=" + self.PC
        return finalString