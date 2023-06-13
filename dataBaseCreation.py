import sqlite3
from telnetlib import RCP
from SalesRecord import SalesRecord

conn = sqlite3.connect("BarksoleDockets.db")

c = conn.cursor()

'''c.execute("""CREATE TABLE dockets (
            dateOfDocket text,
            Shoes real,   
            Keys real,
            Products real,
            Engraving real,
            Plates real,
            Cleaning real,
            CallOuts real,
            Other real
        )""")'''

c.execute("UPDATE dockets SET dateOfDocket = replace(dateOfDocket, '\"', '')")
print(c.fetchall())

'''f = open("Dockets.txt", "r")


for x in f:
    record = x.split(";")

    #while record[1].find('"') > -1:
    #    record[1].replace('"',"")

    for i in range(11):
        if i in (0, 1):
            record.pop(i)
    
    #record[0] = record[0].replace('"', "")
    record[8] = record[8].replace("\n", "")

    #for j in range(1, 9):
        #record[j] = float(record[j])
    
    c.execute("INSERT INTO dockets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8]))

f.close()'''

conn.commit()
conn.close()