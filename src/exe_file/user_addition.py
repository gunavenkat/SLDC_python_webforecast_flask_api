import sqlite3
from werkzeug.security import generate_password_hash

connection = sqlite3.connect("db.sqlite3", check_same_thread=False)
cursor = connection.cursor()


# ------Uncomment to create the database table
# cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
#     User varchar(255),
#     Password varchar(255)
# );""")
# connection.commit()


# -----Uncomment to add user data and api key
# USER = 'admin' # Enter your user name
# API_KEY = '123' # Enter your api key
# cursor.execute('''INSERT INTO Users VALUES (?,?);''',(USER,generate_password_hash(API_KEY, method='sha256'),))
# connection.commit()
