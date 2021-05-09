#Generates the random input to be piped into the program.
import random

def fuzzer(max_length=1000, char_start=32, char_range=32):
    """A string of up to `max_length` characters
       in the range [`char_start`, `char_start` + `char_range`]"""
    string_length = random.randrange(0, max_length + 1)
    out = ""
    for i in range(0, string_length):
        out += chr(random.randrange(char_start, char_start + char_range))
    return out
    
if __name__ == "__main__":
    inputs = ["LIN h", "hhhhhhhh"]
    x = 0
    while x < 1000:
        inputs.append(fuzzer())
        x += 1
    x = 0
    while x < 100:
        inputs.append("IMD " + fuzzer())
        x +=1
    x = 0
    while x < 100:
        inputs.append("CHP " + fuzzer())
        x +=1
    x = 0
    while x < 100:
        inputs.append("DLU " + fuzzer())
        x +=1
    x = 0
    while x < 100:
        inputs.append("EDR " + fuzzer())
        x +=1
    x = 0
    while x < 100:
        inputs.append("ADR " + fuzzer())
        x +=1
    x = 0
    while x < 100:
        inputs.append("DEU " + fuzzer())
        x +=1
    x = 0
    while x < 100:
        inputs.append("LSU " + fuzzer())
        x +=1
    x = 0
    while x < 100:
        inputs.append("DAL " + fuzzer())
        x +=1
    x = 0
    while x < 100:
        inputs.append("DER " + fuzzer())
        x +=1
    x = 0
    while x < 100:
        inputs.append("RER " + fuzzer())
        x +=1
    x = 0
    while x < 100:
        inputs.append("HLP " + fuzzer())
        x +=1
    for y in inputs:
        print(y)
    print("EXT")