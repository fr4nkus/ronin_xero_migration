import sqlite3


conn = sqlite3.connect('file_list.db')
c = conn.cursor()
# Report duplicates
dups = "SELECT md5, COUNT(1) AS tally FROM file GROUP BY md5 HAVING tally >1"
c1 = conn.cursor()
c.execute(dups)
count=0
while True:
    row = c.fetchone()
    if row == None:
        break
    count = count+1
    print( row[0] )
    for g in c1.execute("SELECT path FROM file WHERE md5 = ?", (row[0],) ):
        filepath = g[0].replace('\\','/')
        print( "{}".format( filepath ))
        if "/Clifford Thames2/" in filepath:
            print( "{}".format( filepath ))
            #os.remove(filepath)
 
print( count )
conn.close()  