import mysql.connector
from datetime import datetime

try:
   db = mysql.connector.connect(
      host = 'localhost',
      user = 'root',
      passwd = 'Forager04',
      database = 'users'
   )
   sqlcursor = db.cursor()
   #sqlcursor.execute('CREATE database users')

   #sqlcursor.execute('CREATE database users')
   #sqlcursor.execute('CREATE TABLE mainTable (id int PRIMARY KEY NOT NULL AUTO_INCREMENT, nombre varchar(255), edad int, contrasenia varchar(255), email varchar(255), fecha datetime)')
   #db.commit()
   #sqlcursor.execute('INSERT INTO mainTable (nombre, edad, contrasenia, email, fecha) VALUES (%s, %s, %s, %s, %s)', ('Felipe', 17, "contr4", "email@gmail", datetime.now()))
   sqlcursor.execute('SELECT * FROM mainTable') 
    
   for x in sqlcursor:
      print(sqlcursor)
   
   if db.is_connected():
      print('conexion a database exitosa')
      info_db = db.get_server_info()
      print(info_db)

except Exception as ex:
   print(ex)