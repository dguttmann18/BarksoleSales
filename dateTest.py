import sqlite3

conn = sqlite3.connect("BarksoleDockets.db")

c = conn.cursor()

#c.execute("""CREATE TABLE statements (
#            id integer,
#            statementName text,
#            openingBalance real
#        )""")

#c.execute("""CREATE TABLE payments (
#            id integer,
#            statement int,
#            date text,
#            amount real
#        )""")

c.execute("""SELECT SUBSTR(DateOfDocket, 3, 6) as Month, SUM(Shoes) + SUM(Keys) +SUM(Products) + SUM(Engraving)  + SUM(Plates) + SUM(Cleaning) + SUM(CallOuts) + SUM(Other) AS tot
                FROM Dockets
                WHERE LENGTH(DateOfDocket) = 8 AND SUBSTR(DateOfDocket, 5) LIKE "2021" OR SUBSTR(DateOfDocket, 5) LIKE "2022"
                GROUP BY SUBSTR(DateOfDocket, 3, 6)
                ORDER BY SUBSTR(DateOfDocket, 5), SUBSTR(DateOfDocket, 3, 2)""")
d = c.fetchall()

year1 = {}

x = ("2021", "2022")

for y in x:
    for i in range(12):
        s = str(i+1) + y

        if i < 9:
            s = "0" + s
        
        year1[s] = 0.0

for j in d:
    year1[j[0]] = j[1]

print(str(year1))

conn.commit()
conn.close()