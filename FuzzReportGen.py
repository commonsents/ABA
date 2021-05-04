#Input piping using the other 2 modules
from caseGenerator import fuzzer
import os

#These 2 are designed to check the output of the program according to specifications and generate a report if it does not match expected results
#You guys need to check the output of the program against the expected result at each section of the code.
def checkProgramOutput(programOutput):
    #Look through expected output of project in the project specs and if the program sees one of those codes, it will NOT generate a report 
    valid_outputs = []
    valid_outputs.append("An account is currently active; logout before proceeding")
    valid_outputs.append("Invalid credentials")
    valid_outputs.append("Enter your password:")
    valid_outputs.append("This is the first time the account is being used. You must create a new password. Passwords may contain 8-24 upper- or lower-case letters or numbers. Choose an uncommon password that would be difficult to guess.")
    valid_outputs.append("Reeneter the same password: ")
    valid_outputs.append("Passwords do not match")
    valid_outputs.append("Password contains illegal characters")
    valid_outputs.append("Passwords is too easy to guess")
    valid_outputs.append("OK")
    valid_outputs.append("No active login session")
    valid_outputs.append("Create a new password. Passwords may contain up to 24 upper- or lower-case letters or numbers. Choose an uncommon password that would be difficult to guess.")
    valid_outputs.append("Admin not active")
    valid_outputs.append("Invalid userID")
    valid_outputs.append("Account already exists")
    valid_outputs.append("Admin not authorized")
    valid_outputs.append("No recordID")
    valid_outputs.append("Invalid recordID")
    valid_outputs.append("One or more invalid record data fields")
    valid_outputs.append("Number of records exceeds maximum")
    valid_outputs.append("Duplicate recordID")
    valid_outputs.append("RecordID not found")
    valid_outputs.append("Invalid fieldname (s)")
    valid_outputs.append("No Input_file specified")
    valid_outputs.append("Can't open Input_file")
    valid_outputs.append("Input_file invalid format")
    valid_outputs.append("No Output_file specified")
    valid_outputs.append("Can't open Output_file")
    valid_outputs.append("Error writing Output_file")
    valid_outputs.append("Unrecognized command")
    valid_outputs.append("Choose a username for the admin account: ")
    valid_outputs.append("UserID contains invalid number of characters.")
    valid_outputs.append("Please enter a new userID: ")
    valid_outputs.append("This userID is already taken.")
    valid_outputs.append("UserID contains illegal characters.")
    valid_outputs.append("An admin account cannot delete itself")
    valid_outputs.append("Invalid format. See 'HLP' command for required inputs for the 'LSU' command.")
    valid_outputs.append("Please specify userID.")
    valid_outputs.append("Invalid format. See 'HLP' command for required inputs for the 'CHP' command.")
    valid_outputs.append("Command not found. Type \"HLP\" for a list of commands.")
    valid_outputs.append("Invalid format. See 'HLP' command for required inputs for the 'RER' command.")
    valid_outputs.append("Invalid format. See 'HLP' command for required inputs for the 'EDR' command.")
    valid_outputs.append("Invalid format. See 'HLP' command for required inputs for the 'DER' command.")
    valid_outputs.append("Invalid format. See 'HLP' command for required inputs for the 'ADR' command.")
    valid_outputs.append("Invalid format. See 'HLP' command for required inputs for the 'DAL' command.")
    valid_outputs.append("Invalid format. See 'HLP' command for required inputs for the 'ADU' command.")
    valid_outputs.append("Invalid format. See 'HLP' command for required inputs for the 'DEU' command.")
    valid_outputs.append("Address Book Import Complete.")
    valid_outputs.append("Thank you for using ABA.")
    valid_outputs.append("Invalid format. See 'HLP' command for required inputs for the 'LOU' command.")
    valid_outputs.append("")
    valid_outputs.append("")
    valid_outputs.append("")
    valid_outputs.append("Maximum amount of users reached. You cannot any add more users until at least one is deleted.")
    valid_outputs.append("Create a unique userID. ID may contain 1-16 upper- or lower-case letters or numbers.")
    valid_outputs.append("Address Book Application, version 1.1 . Type ""HLP"" for a list of commands.")
    
    if programOutput in valid_outputs:
        return()
    else: 
       generateReport(programOutput)
    quit()

    
def generateReport():
    #Generate a Report that will be piped to some specified filename
    #This should just be a series of print statements, since we will pipe the info via the CLI
    #print(Input Value: ...)
    #print(Error Received: ...)
    quit()


if __name__ == "__main__":
    input1 = input()
    while(input1 != ""):
        checkProgramOutput(input1)
    print(input1)
