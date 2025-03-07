import time
import sys
import os

if len(sys.argv) < 2:
    print("No file specified")
    sys.exit()
fileName=sys.argv[1]

try:
    data=open(fileName, "r")
except:
    print("Error can't open file")
    sys.exit()

os.system("touch cnf.txt")
os.system("touch glucoseResult.txt")
print("generando representacion cnf")
os.system(f'python3 jsonToCNF.py {fileName} > cnf.txt')
print("ejecutando glucose sobre cnf generado")
os.system("./glucose-syrup-4.1/simp/glucose_static cnf.txt glucoseResult.txt")
os.system(f'python3 cnfToICS.py {fileName}')
os.system("rm glucoseResult.txt")