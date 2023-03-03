# import all the required libraries
from flask import Flask, request

# library for the weather api
from aiopywttr import Wttr
from json import dumps, loads

# used to parse the congfig file
from configparser import ConfigParser
from werkzeug.security import check_password_hash
import asyncio

# library to access db.sqlite3
import sqlite3
import os

# declare the global variables
PORT = 45000
PATH = "db.sqlite3"
app = Flask(__name__)
# creatio of the config parser object
configur = ConfigParser()
try:
    # print(configur.read("config.ini"))
    configur.read("config.ini")
    # get the port number from the config file and path
    PORT = configur.get("settings", "port")
    path = configur.get("settings", "db_path")
    if os.path.isfile(path):
        PATH = path
    else:
        print("Using default path for db")
        pass
except Exception as e:
    # print the error message and use the default settings
    print("Exception during config file opening:-", e)
    print("Using default settings")
finally:
    print(f"The selected port number is: {PORT}")
    print(f"The given path for db is: {PATH}")

# establish the connectio with the sqlite file
connection = sqlite3.connect(PATH, check_same_thread=False)
cursor = connection.cursor()
# create a table if file not present
cursor.execute(
    """CREATE TABLE IF NOT EXISTS Users (
    User varchar(255),
    Password varchar(255)
);"""
)
connection.commit()


async def check_dictionary(dictionary):
    """function to check the dictionary for all the parameters

    Args:
        dictionary (dict): a dictionary of the weather data accessign json file

    Returns:
        boolean: true if errors present in the dictionary
    """
    result = True
    # checks if the user and the api-key key are present in the dictionary
    if "user" not in dictionary.keys():
        return (result, "no parameter 'user' in given json file")
    if "api-key" not in dictionary.keys():
        return (result, "no parameter 'api-key' in given json file")

    # search for the user parameter
    cursor.execute("SELECT * from Users WHERE User = ?", (dictionary["user"],))
    user = cursor.fetchone()

    print("user= ", user)
    # check if the user is present
    if user == None:
        return (result, "user name not found")
    # check if the api key is correct
    if not (check_password_hash(user[1], dictionary["api-key"])):
        return (result, "Invalid api-key")

    if "place" not in dictionary.keys():
        return (result, "no parameter 'place' in given json file")
    return (False, "No error with json checks")


async def prepare_dictionary(forecast, dictionary):
    """a function to prepare a dictionary of required parameters from the api returned object

    Args:
        forecast (pywttr object): return object of the weather data
        dictionary (a dictionary of get json data): json data send from user in form of dictionary

    Returns:
        dictionary: prepared dictionary
    """
    # pharse on the location parameters
    for i, j in forecast.nearest_area[0]:
        # use if for these special parameters
        if i in ["area_name", "country", "region"]:
            dictionary[i] = j[0].value
            continue
        if isinstance(j, str):
            dictionary[i] = j
    # pharse on the current condition parameters
    for i, j in forecast.current_condition[0]:
        # use if for these special parameters
        if i in ["weather_desc"]:
            dictionary[i] = j[0].value
            continue
        if isinstance(j, str):
            dictionary[i] = j
    return dictionary


# Home page
@app.route("/")
async def home():
    """basic function call for flask api endpoint

    Returns:
        json: the prepared json with weather data is sent
    """
    print("Flask End-point access called...")
    # creatio of the dictionary for the json preparation
    dictionary = {"status": "false"}
    # check if the request is answered
    if request.is_json:
        request_data = request.get_json()
        print("found json ->", request_data)
        # update the dictionary with the data parameters
        dictionary.update(loads(request_data))
        # check the result data and apped to the dictionary
        result, reason = await check_dictionary(dictionary)
        # if the result from the validation is success
        if result:
            print(reason)
            dictionary["reason"] = reason
            # return in case of failures of error checks
            return dumps(dictionary)
        # print the reason
        print(reason)
        # try calling the api
        try:
            wttr = Wttr(dictionary["place"])
            # get the result in english
            forecast = await wttr.en()
        except:
            # print in case of error and return the error message
            print("Unable to find the given location weather")
            dictionary["reason"] = "Unable to find the given location weather"
            return dumps(dictionary)
        # prepare the dictionary of various values
        dictionary = await prepare_dictionary(forecast, dictionary)
        # update the status to true
        dictionary["status"] = "true"
        print("The generated data is--")
        print(dictionary)

        return dumps(dictionary)
    else:
        # return an error in case of no json file present in the client request
        dictionary["reason"] = "no json data found"
        return dumps(dictionary)


if __name__ == "__main__":
    # intialize the ports and the debug mode in flask api
    app.run(debug=True, host="0.0.0.0", port=PORT, threaded=True)
