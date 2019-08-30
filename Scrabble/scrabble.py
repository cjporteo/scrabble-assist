from dictdata import DictData
import output
from sys import argv
import time

wordlist_map = {"collins15": ("Collins 2015", "collins2015.txt"),
                "master": ("Master", "masterwords.txt")}

k = argv[1] if len(argv) > 1 else "collins15"  # chosen wordlist
t = int(argv[2]) if len(argv) > 2 else 45  # number of results displayed
rows = int(argv[3]) if len(argv) > 3 else 15  # number of rows displayed

print("\nInitializing data objects...")
dd = DictData(wordlist_map[k][1])
print("\nLoaded {} Word List".format(wordlist_map[k][0]))

time.sleep(0.5)

while 1:
    tiles = input("\nEnter tiles (? for blank, 0 to exit):\n")
    if tiles == '0':
        break
    output.results(tiles, dd, t, rows)
    time.sleep(1)
