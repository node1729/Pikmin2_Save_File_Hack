import struct
import sys
import binascii
from calc_pik2_checksum import calc_checksum
from pik2_savefile_constants import *
import json

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

def edit_poko_count(underground=False):
    if not underground:
        f.seek(offset + OFFSET.POKO_COUNT)
        pokos = f.read(4)
        newpokos = input("the current poko count is " + str(int.from_bytes(pokos, "big")) + " input what you want to change it to (in decimal): ")
        newpokos = int(newpokos)
        newpokos = newpokos.to_bytes(4, "big")

        #write to locations
        f.seek(offset + OFFSET.POKO_COUNT)
        f.write(newpokos)
        f.seek(offset + OFFSET.SF_POKO_COUNT)
        f.write(newpokos)
        f.flush()
    else:
        f.seek(offset + OFFSET.UNDERGROUND_POKO_COUNT)
        pokos = f.read(4)
        newpokos = input("the current underground poko count is " + str(int.from_bytes(pokos, "big")) + " input what you want to change it to (in decimal): ")
        newpokos = int(newpokos)
        newpokos = newpokos.to_bytes(4, "big")

        #write to location
        f.seek(offset + OFFSET.UNDERGROUND_POKO_COUNT)
        f.write(newpokos)
        f.flush()

def edit_exploration_kit():
    #get string of ek treasures and their bitmask value
    outstr = ""
    for item in EXPLORATION_KIT.EK_TREASURE_NAME:
        outstr += item + ": " + str(EXPLORATION_KIT.EK_TREASURE_NAME[item]) + ", "
    print(outstr)

    #seek to location and get current bitmask
    f.seek(offset + OFFSET.EXPLORATION_KIT)
    ek = f.read(2)
    newek = input("The current sum of these is " + str(int.from_bytes(ek, "big")) + " input what you want to change it to: ")
    newek = int(newek)

    #write to location
    newek = newek.to_bytes(2, "big")
    f.seek(offset + OFFSET.EXPLORATION_KIT)
    f.write(newek)
    f.flush()

def edit_pikmin_onion():

    isdone = False
    while not isdone:
        pik_color = "null"
        while pik_color.upper() not in OFFSET.PIKMIN_ONION and not isdone:
            pik_color = input("Input a pikmin color (Blue, Red, Yellow, Purple, White) (input \"done\" to finish): ")
            pik_color = pik_color.upper()
            if pik_color == "DONE":
                isdone = True
        pik_type = "null"
        while pik_type.upper() not in OFFSET.PIKMIN_SUB_OFFSET and not isdone:
            pik_type = input("Input a pikmin type (Leaf, Bud, Flower): ")
            pik_type = pik_type.upper()
        if not isdone:
            f.seek(offset + OFFSET.PIKMIN_ONION[pik_color] + OFFSET.PIKMIN_SUB_OFFSET[pik_type])
            current_piks = f.read(4)
            print(hex(OFFSET.PIKMIN_ONION[pik_color] + OFFSET.PIKMIN_SUB_OFFSET[pik_type]))
            newpiks = input("The Current pikmin in this Onion is " + str(int.from_bytes(current_piks, "big")) + " input what you want to change it to: ")
            newpiks = int(newpiks)

            #write to location
            newpiks = newpiks.to_bytes(4, "big")
            f.seek(offset + OFFSET.PIKMIN_ONION[pik_color] + OFFSET.PIKMIN_SUB_OFFSET[pik_type])
            f.write(newpiks)
            f.flush()

def edit_fall_pikmin():
    isdone = False
    while not isdone:
        pik_color = "null"
        while pik_color.upper() not in OFFSET.PIKMIN_FALL and not isdone:
            pik_color = input("Input a pikmin color (Blue, Red, Yellow, Purple, White, Bulbmin, PikPik) (input \"done\" to finish): ")
            pik_color = pik_color.upper()
            if pik_color == "DONE":
                isdone = True
        pik_type = "null"
        while pik_type.upper() not in OFFSET.PIKMIN_SUB_OFFSET and not isdone:
            pik_type = input("Input a pikmin type (Leaf, Bud, Flower): ")
            pik_type = pik_type.upper()
        if not isdone:
            f.seek(offset + OFFSET.PIKMIN_FALL[pik_color] + OFFSET.PIKMIN_SUB_OFFSET[pik_type])
            current_piks = f.read(4)
            print(hex(OFFSET.PIKMIN_FALL[pik_color] + OFFSET.PIKMIN_SUB_OFFSET[pik_type]))
            newpiks = input("The Current pikmin in this Onion is " + str(int.from_bytes(current_piks, "big")) + " input what you want to change it to: ")
            newpiks = int(newpiks)

            #write to location
            newpiks = newpiks.to_bytes(4, "big")
            f.seek(offset + OFFSET.PIKMIN_FALL[pik_color] + OFFSET.PIKMIN_SUB_OFFSET[pik_type])
            f.write(newpiks)
            f.flush()

def edit_collected_treasures(ek=False):
    if not ek:
        treasurefile = open("treasure.json")
        seek_to_treasure = OFFSET.TREASURE_START
    else:
        treasurefile = open("ektreasure.json")
        seek_to_treasure = OFFSET.EK_TREASURE_START

    treasure_dict = json.load(treasurefile)
    treasure_dict = {int(key):value for key,value in treasure_dict.items()}
    max_treasure_key = max(treasure_dict)
    isdone = False
    while not isdone:
        treasure_to_change = input("Input the treasure ID you wish to change (in decimal), values between 0 and " + str(max_treasure_key) + " or type \"done\" to finish: ")
        if treasure_to_change.upper() == "DONE":
            isdone = True
        if not isdone:
            f.seek(offset + seek_to_treasure + int(treasure_to_change))
            print("You have selected \"" + treasure_dict[int(treasure_to_change)] + "\" the current value of which is " + str(int.from_bytes(f.read(1), "big")))
            treasure_modify = input("Input what you want to change this value to: ")
            treasure_modify = int(treasure_modify)

            #write to location
            f.seek(offset + seek_to_treasure + int(treasure_to_change))
            f.write(treasure_modify.to_bytes(1, "big"))
            f.flush()


edit_collected_treasures(True)
edit_collected_treasures()
edit_pikmin_onion()
edit_exploration_kit()
edit_day_counter()
write_checksum(infile)
