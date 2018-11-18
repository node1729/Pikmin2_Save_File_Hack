import struct
import sys
import binascii
from calc_pik2_checksum import calc_checksum
from pik2_savefile_constants import OFFSET

try:
    infile = sys.argv[1]
except Exception as er:
    raise RuntimeException("Not enough arguments: {0}".format(sys.argv))

def locate_save_file(save_file, data):
    save_file = int(save_file) - 1
    offset = data.find(b"PlVa0003" + bytes([save_file]))
    return offset


f = open(infile, "rb+")
data = f.read()

save_file = input("type in the save file that you want to have overwritten: ")

offset = locate_save_file(save_file, data)

f.seek(offset)

print("Save file starting at " + hex(offset))

def write_checksum(infile):
    f = open(infile, "rb+")
    #calc checksum and find components
    checksum = calc_checksum(infile, offset)
    checksum[0] = checksum[0][2:]
    checksum[1] = checksum[1][2:]
    
    #ensure components are of proper length
    while len(checksum[0]) < 4:
        checksum[0] = "0" + checksum[0]

    while len(checksum[1]) < 4:
        checksum[1] = "0" + checksum[1]
    
    checksum = checksum[0] + checksum[1] 
    checksum = bytearray.fromhex(checksum)
    
    #write checksum
    f.seek(offset + OFFSET.CHECKSUM)
    f.write(checksum)
    f.flush()
    #print output of where it wrote the file to
    f.seek(offset + OFFSET.SAVE_FILE)
    written_to = str(int(binascii.hexlify(f.read(1))) + 1)
    print("wrote checksum for file " + written_to)

def edit_day_counter():
    #find day counter position and print what the day is
    f.seek(offset + OFFSET.DAY_COUNTER)
    day = f.read(4)
    # ask for day and convert into bytes
    new_day = input("current day is " + str(int.from_bytes(day, "big") + 1) + " input what you want to change it to (in decimal): ")
    ig_day = int(new_day) - 1 
    ig_day = ig_day.to_bytes(4, "big")
    sf_day = int(new_day)
    sf_day = sf_day.to_bytes(4, "big")

    #go back to the lword start and write bytes
    f.seek(offset + OFFSET.DAY_COUNTER)
    f.write(ig_day)
    f.seek(offset + OFFSET.SF_DAY_COUNTER)
    f.write(sf_day)
    f.flush()

edit_day_counter()
write_checksum(infile)
