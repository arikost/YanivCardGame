import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'arik',
    passwd = 'abcdef',
    database = 'mydb',
)
cursor = mydb.cursor(buffered=True)
# cursor.execute("INSERT INTO users VALUES(%s, %s, %s, %s, %s)", (
#     1, "alona", "1234", 0, 0 
# ))
# cursor.execute("INSERT INTO users VALUES(%s, %s, %s, %s, %s)", (
#     2, "arik", "1234", 0, 0 
# ))
cursor.execute("SELECT * FROM users")
print(cursor.fetchall())
# mydb.commit()
cursor.close()
mydb.close()
