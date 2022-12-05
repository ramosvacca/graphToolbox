import sys

with open(sys.argv[1], "r") as drugs_toread:

    for line in drugs_toread:
        print(line.split(", "))
