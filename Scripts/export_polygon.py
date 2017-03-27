import sys
import os.path


file = sys.argv[1]
with open(file,"r") as fin:
	   lines=fin.readlines()
with open(file,"w") as fin:  
	   [fin.write(line) for line in lines if line.strip() ]


with open(file, 'r') as fin:
	   data = fin.read().splitlines(True)
with open(file, 'w') as fin:
	   fin.writelines(data[:-1])


f = open(file, "r")
data = f.readlines()
f.close()
data.insert(0, "{\n \"type\": \"FeatureCollection\",\n \"features\": \n")


f = open(file, "w")
data = "".join(data)
polygon = ("},\n{\n \"type\":\n \"Feature\",\n \"geometry\": {\n \"type\": \"Polygon\",\n \"coordinates\": " + 
			  "[[[ -4.399991, 60.325 ], [ -4.3080609999999995, 60.319297 ],   [ -4.30, 60.28 ], " + 
			  "[ -4.48, 60.26], [ -4.399991, 60.325 ]]]},\n " + 
			  "\"properties\": {\"value\": \"query field\"} \n} \n]}")
f.write(data+polygon)
f.close()










