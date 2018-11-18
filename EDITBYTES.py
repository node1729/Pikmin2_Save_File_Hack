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


#Find magic number location and seek to it
while True:
    offset = data.find(b"PlVa0003" + bytes([save_file]))
    f.seek(offset)
    print("Save file " + str(save_file + 1) + " starting at " + hex(offset))

    byte_to_modify = input("input the offset that you want to modify: 0x")
    byte_to_modify = int(byte_to_modify, 16)

    byte_len = input("input the length of the offset in bytes you want to modify: 0x")
    byte_len = int(byte_len, 16)

    f.seek(offset + byte_to_modify)
    edit_byte = input("This byte is: 0x" + str(binascii.hexlify(f.read(byte_len)))[2:-1] + " insert value to change it to: 0x")

    #ensure the string is long enough
    while len(edit_byte) < byte_len * 2:
        edit_byte = "0" + edit_byte
    edit_byte = bytearray.fromhex(edit_byte)
    # go back to the position that the byte starts at
    f.seek(0 - byte_len, 1)

    # write to file and close
    f.write(edit_byte)
    f.flush()
    f.close()

    # reopen file for checksum calculations
    f = open(infile, "rb+")
    data = f.read()

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

    #write checksum
    f.seek(offset + 0xC000 - 4)
    f.write(checksum)
    f.flush()
    f.seek(-4, 1)
    print(binascii.hexlify(f.read(4)))
    f.close()
    f = open(infile, "rb+")
    data = f.read()
