from flask import Flask, request
from aiopywttr import Wttr
from json import dumps, loads
from configparser import ConfigParser
from werkzeug.security import check_password_hash
import asyncio
import sqlite3
import os

PORT = 45000
PATH = 'db.sqlite3'
app = Flask(__name__)
configur = ConfigParser()
try:
    # print(configur.read("config.ini"))
    configur.read("config.ini")
    PORT = configur.get("settings", "port")
    path = configur.get("settings", "db_path")
    if os.path.isfile(path):
        PATH = path
    else:
        print('Using default path for db')
        pass
except Exception as e:
    print("Exception during config file opening:-", e)
    print("Using default settings")
finally:
    print(f"The selected port number is: {PORT}")
    print(f"The given path for db is: {PATH}")

connection = sqlite3.connect(PATH, check_same_thread=False)
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
    User varchar(255),
    Password varchar(255)
);""")
connection.commit()


async def check_dictionary(dictionary):
    result = True
    if 'user' not in dictionary.keys():
        return(result, "no parameter 'user' in given json file")
    if 'api-key' not in dictionary.keys():
        return(result, "no parameter 'api-key' in given json file")
    
    cursor.execute("SELECT * from Users WHERE User = ?",(dictionary['user'],))
    user=cursor.fetchone()

    print('user= ',user)
    # print('user dict',dictionary['user'])
    # print('api-key dict',dictionary['api-key'])
    
    if user==None:
        return(result, "user not found")
    if not(check_password_hash(user[1], dictionary['api-key'])):
        return(result, "check your api-key")
    # if not check_password_hash(user[2], dictionary['api-key']):
    #     return(result, "check your api-key")

    if 'place' not in dictionary.keys():
        return(result, "no parameter 'place' in given json file")
    return (False, 'No error with json checks')

async def prepare_dictionary(forecast, dictionary):
    for i, j in forecast.nearest_area[0]:
        if i in ["area_name", "country", "region"]:
            dictionary[i] = j[0].value
            continue
        if isinstance(j, str):
            dictionary[i] = j

    for i, j in forecast.current_condition[0]:
        if i in ["weather_desc"]:
            dictionary[i] = j[0].value
            continue
        if isinstance(j, str):
            dictionary[i] = j
    return dictionary


# Home page
@app.route("/")
async def home():
    print("Flask End-point access called...")
    dictionary = {"status": "false"}
    if request.is_json:
        request_data = request.get_json()
        print("found json ->", request_data)
        dictionary.update(loads(request_data))
        
        result, reason = await check_dictionary(dictionary)
        if result:
            print(reason)
            dictionary["reason"] = reason
            return dumps(dictionary)    
        print(reason)
        
        try:
            wttr = Wttr(dictionary["place"])
            forecast = await wttr.en()
        except:
            print("Unable to find the given location weather")
            dictionary["reason"] = "Unable to find the given location weather"
            return dumps(dictionary)
        # print('return data from wttr: ')
        # print(forecast)

        dictionary = await prepare_dictionary(forecast, dictionary)

        dictionary["status"] = "true"
        print("The generated data is--")
        print(dictionary)
        
        return dumps(dictionary)
    else:
        dictionary["reason"] = "no json data found"
        return dumps(dictionary)


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = PORT, threaded = True)
