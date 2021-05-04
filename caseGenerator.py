#Generates the random input to be piped into the program.
import random

def fuzzer(max_length=100, char_start=32, char_range=32):
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
    while x < 3:
        inputs.append(fuzzer())
        x += 1
    for y in inputs:
        print(y)
    print("EXT")