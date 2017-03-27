import sys
import os.path



file = sys.argv[1]

with open(file, 'r') as fin:
    data = fin.read().splitlines(True)
with open(file, 'w') as fin:
    fin.writelines(data[5:-1])


f = open(file, "r")
data = f.readlines()
f.close()
data.insert(0, '[\n')

f = open(file, "w")
data = "".join(data)
f.write(data)
f.close()	


