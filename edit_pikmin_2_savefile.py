import struct
import sys
import binascii
from calc_pik2_checksum import calc_checksum
from pik2_savefile_constants import OFFSET

try:
    infile = sys.argv[1]
except Exception as er:
    raise RuntimeException("Not enough arguments: {0}".format(sys.argv))

f = open(infile, "rb+")
data = f.read()

save_file = input("type in the save file that you want to have overwritten: ")
save_file = int(save_file) - 1

offset = data.find(b"PlVa0003" + bytes([save_file]))

f.seek(offset)

print("Save file starting at " + hex(offset))

checksum = (calc_checksum(infile, offset))

checksum[0] = checksum[0][2:]
checksum[1] = checksum[1][2:]

while len(checksum[0]) < 4:
    checksum[0] = "0" + checksum[0]

while len(checksum[1]) < 4:
    checksum[1] = "0" + checksum[1]
    
checksum = checksum[0] + checksum[1] 
checksum = bytearray.fromhex(checksum)
print(checksum)

f.seek(offset + 0xC000 - 4)
print(binascii.hexlify(f.read(4)))

