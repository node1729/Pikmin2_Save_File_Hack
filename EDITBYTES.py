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
    current_value = int.from_bytes(f.read(byte_len), "big")
    base_edit = 0
    while base_edit != 2 and base_edit != 8 and base_edit != 10 and base_edit != 16:
        base_edit = input("input the base you want to edit the value to (2, 8, 10, 16): ")
        base_edit = int(base_edit)
    
    if base_edit == 2:
        outstr = bin(current_value)
    elif base_edit == 8:
        outstr = oct(current_value)
    elif base_edit == 10:
        outstr = str(current_value)
    elif base_edit == 16:
        outstr = hex(current_value)

    edit_byte = input("This value is " + outstr + " insert value to change it to (in base " + str(base_edit) + "): ")
    
    edit_byte = int(edit_byte, base_edit)
    
    edit_byte = edit_byte.to_bytes(byte_len, "big")
    #ensure the string is long enough
    """while len(edit_byte) < byte_len * 2:
        edit_byte = "0" + edit_byte
    edit_byte = bytearray.fromhex(edit_byte)"""
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
