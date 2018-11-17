import sys
import struct

"""
Compares two files to each other, and writes differences to a file.
"""

try:
    infile1 = sys.argv[1]
    infile2 = sys.argv[2]
except Exception as er:
    raise RuntimeException("Not Enough Arguments")

print(infile1 + " comparing to " + infile2)

outfile = open("outfile.txt", "w")

with open(infile1, "rb") as f:
    data1 = f.read()

with open(infile2, "rb") as g:
    data2 = g.read()

if len(data1) < len(data2):
    shorter_file_len = len(data1)
else:
    shorter_file_len = len(data2)

for i in range(0, shorter_file_len):
    val1 = data1[i]
    val2 = data2[i]
    if val1 != val2:
        outfile.write("Difference at offset:" + str(hex(i)) + " of " + str(hex(data1[i])) + " vs " + str(hex(data2[i])) + "\n") 
        outfile.flush()

