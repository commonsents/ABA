#Input piping using the other 2 modules
from caseGenerator import fuzzer
import os

#These 2 are designed to check the output of the program according to specifications and generate a report if it does not match expected results
#You guys need to check the output of the program against the expected result at each section of the code.
def checkProgramOutput(programOutput):
    #Look through expected output of project in the project specs and if the program sees one of those codes, it will NOT generate a report 
    #If ok
    #   return()
    #else 
    #   generateReport()
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