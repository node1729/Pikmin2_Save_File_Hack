import struct
import sys
"""
Extract Pikmin 2 save in dolphin as .gci, open gci in a hex editor 
and search for string "PlVa" which signals the start of a save file. 
Starting with the first symbol of the string, select 0xC000 bytes 
and copy it into a separate file. Use this script with that file.
"""

def calc_checksum(infile, offset=0):
    with open(infile, "rb") as f:
        data = f.read()

    c1 = c2 = 0
    for i in range(offset, offset + 0xC000-4, 2): 
        val1 = data[i]
        val2 = data[i+1]

        val = (val1 << 8) + val2

        if True:
            c1 = (c1 + val) & 0xFFFF
            c2 = (c2 + (val ^ 0xFFFF)) & 0xFFFF

    if c1 == 0xFFFF: c1 = 0
    if c2 == 0xFFFF: c2 = 0

    # These two values together form the checksum for the save data. 
    # Replace the checksum in the save data with these.
    print(hex(c1), hex(c2))
    return [hex(c1), hex(c2)]


