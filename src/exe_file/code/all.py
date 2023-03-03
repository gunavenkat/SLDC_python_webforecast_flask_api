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


def tkinter_call():
    """tkinter weather app call function"""
    # import all the required libraries
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.font as font
    import tkinter as tk
    from tkinter import messagebox
    import requests
    import json

    WIDTH, HEIGHT = 640, 360  # Defines aspect ratio of window.
    # defines a dictionary to store the wigets reference in dict
    TKINTER_WIDGETS = {}

    # currently the below function is not being used in our application
    def maintain_aspect_ratio(event, aspect_ratio):
        """Event handler to override root window resize events to maintain the
        specified width to height aspect ratio.
        """
        if event.widget.master:  # Not root window?
            return  # Ignore.

        # <Configure> events contain the widget's new width and height in pixels.
        new_aspect_ratio = event.width / event.height

        # Decide which dimension controls.
        if new_aspect_ratio > aspect_ratio:
            # Use width as the controlling dimension.
            desired_width = event.width
            desired_height = int(event.width / aspect_ratio)
        else:
            # Use height as the controlling dimension.
            desired_height = event.height
            desired_width = int(event.height * aspect_ratio)

        # Override if necessary.
        if event.width != desired_width or event.height != desired_height:
            # Manually give it the proper dimensions.
            event.widget.geometry(f"{desired_width}x{desired_height}")
            return "break"  # Block further processing of this event.

    try:
        # create a tkinter window
        win = tk.Tk()
        win.title("VGS weather app")
        # define its geomentry
        win.geometry(f"{WIDTH}x{HEIGHT}")

        try:
            # get the icon upload
            photo = tk.PhotoImage(file="weather.png")
            win.iconphoto(False, photo)
        except:
            pass

        # initialize the font parameters
        MY_FONT = font.Font(family="Helvetica", size=20)

        # create a frame for user and api inputs
        pane = tk.Frame(win)
        pane.pack(fill=tk.BOTH, expand=True)
        # label for user
        label_user = tk.Label(
            pane,
            text="User:",
            font=MY_FONT,
            justify="right",
            background="#FF8C00",
            fg="white",
            height=1,
        )
        label_user.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(10, 0), pady=10)
        # entry for user name input
        entry_user = tk.Entry(pane, font=MY_FONT, justify="center")
        entry_user.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10), pady=10)
        # label for api-key
        label_api = tk.Label(
            pane,
            text="Api-key:",
            font=MY_FONT,
            justify="right",
            background="#FF8C00",
            fg="white",
            height=1,
        )
        label_api.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(10, 0), pady=10)
        # entry for api key
        entry_api = tk.Entry(pane, font=MY_FONT, show="*", justify="center")
        entry_api.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10), pady=10)

        s = ttk.Style()
        s.theme_create(
            "MyStyle",
            parent="alt",
            settings={
                "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
                "TNotebook.Tab": {
                    "configure": {
                        "padding": [100, 10],
                        "font": ("URW Gothic L", "15", "bold"),
                    },
                },
            },
        )
        s.theme_use("MyStyle")

        # use ttk to create a notebook of seperate tabs
        my_notebook = ttk.Notebook(win)
        my_notebook.pack(expand=1, fill=tk.BOTH)
        # create a frame for name search
        tab1 = ttk.Frame(my_notebook)
        my_notebook.add(tab1, text="Name-search")
        # create a frame for latitude/longitude
        tab2 = ttk.Frame(my_notebook)
        my_notebook.add(tab2, text="Lat/Lon-search")

        # create a grid of parameters
        for i in range(4):
            tk.Grid.columnconfigure(tab1, i, weight=1)
            tk.Grid.columnconfigure(tab2, i, weight=1)
        for i in range(5):
            tk.Grid.rowconfigure(tab1, i, weight=1)
            tk.Grid.rowconfigure(tab2, i, weight=1)

        def align_string(s):
            """align the received parameters strings with equal spacings

            Args:
                s (string): output strings

            Returns:
                string: equally spaced string with equal lengths
            """
            x = s.split(":")
            if len(x[0]) < 14:
                x[0] += " " * (14 - len(x[0]))
            # print(len(x[0]))
            # uncomment for center alignment in output label
            # if len(x[0]) == len(x[1]):
            #     return s
            # if len(x[0]) > len(x[1]):
            #     x[1] = " " * (len(x[0]) - len(x[1])) + x[1]
            # else:
            #     x[0] += " " * (len(x[1]) - len(x[0]))

            return f"{x[0]}:{x[1]}"

        def output_string_creator(dictionary):
            """convert the dictionary of paramerts into string with newline characters

            Args:
                dictionary (dict): weather dictionary

            Returns:
                string: output display string
            """
            # display the output string
            output_string = []
            # direction arrows for the wind symbol
            direction_arrow = "↑↖←↙↓↘→↗"
            output_string.append(
                f"Weather report : {dictionary['area_name']}, {dictionary['region']}, {dictionary['country']} ✔\n"
            )
            output_string.append(f"Weather : {dictionary['weather_desc']}")
            output_string.append(
                f"Temperature : {dictionary['temp_c']}({dictionary['feels_like_c']}) °C"
            )
            output_string.append(f"Humidity : {dictionary['humidity']}")
            output_string.append(
                f"Wind : {(direction_arrow[int((float(dictionary['winddir_degree'])+22.5)//45)%8])} {dictionary['windspeed_kmph']}kmph"
            )
            output_string.append(
                f"Latitude, Longitude : {dictionary['latitude']}, {dictionary['longitude']}"
            )
            output_string_1 = []
            # aligning the string
            for i in output_string:
                output_string_1.append(align_string(i))
            output_string[0] += "\n"
            return "\n".join(output_string_1)

        # list and dictionary to store the fetched data and prepare the list of favourite places
        place_list = {}
        place_list_items = []

        # --------------------for tab1

        def weather_call_1():
            """weather call function for the first tab and display the fetched output with alignments

            Returns:
                boolean: returns an error if any
            """
            # get the combo box value
            k = combo_favourite.get()
            # check if value is present else go for the entry box
            if k != "":
                place = k
                combo_favourite.set("")
            else:
                place = entry_place.get()
            # clear the entry
            entry_place.delete(0, tk.END)
            entry_place.insert(0, "Please Wait!!")
            # display the entered place
            label_place_1.configure(text="Entered place: " + place)
            label_output_1.configure(text="")
            # fetch the user name and api key
            USER = entry_user.get()
            API_KEY = entry_api.get()
            # create a json for fetch
            data = json.dumps({"user": USER, "api-key": API_KEY, "place": place})
            try:
                response = requests.get("http://127.0.0.1:45000/", json=data)
            except Exception as e:
                print("Unable to connect to flask api")
                label_output_1.configure(text="Unable to connect to flask api")
                entry_place.delete(0, tk.END)
                label_place_1.configure(background="#FF0000")
                messagebox.showerror("Error", "Unable to connect to flask api")
                return False
            # if the response is received
            if response.ok:
                # get the json from response
                dictionary = response.json()

                if dictionary["status"] == "false":
                    print(dictionary["reason"])
                    label_output_1.configure(text=str(dictionary["reason"]))
                    entry_place.delete(0, tk.END)
                    label_place_1.configure(background="#FF0000")
                    messagebox.showwarning("Warning", str(dictionary["reason"]))
                    return False
                # add a parameter in case for ordering
                dictionary["s.no"] = len(place_list)
                place_list[dictionary["area_name"]] = dictionary

                print("Successfully fetched the data")
                label_output_1.configure(
                    text=output_string_creator(place_list[dictionary["area_name"]])
                )
                entry_place.delete(0, tk.END)
                # get the place items
                global place_list_items
                place_list_items = list(place_list.keys())
                combo_favourite.configure(values=place_list_items)
                label_place_1.configure(background="#00FF00")
                return {dictionary["area_name"]: dictionary}

            else:
                # return in case of error
                print("response not found")
                label_output_1.configure(text="response not found")
                label_place_1.configure(background="#FF0000")
                messagebox.showerror("Error", "response not found")
                entry_place.delete(0, tk.END)
                return False

        # creation of the label and widgets
        label_place_msg = tk.Label(
            tab1, font=MY_FONT, text="Enter Place:  ", height=1, justify="center"
        )
        label_place_msg.grid(
            row=0, column=0, rowspan=1, columnspan=1, sticky="E", padx=(10, 0), pady=10
        )

        label_place_msg = tk.Label(
            tab1, font=MY_FONT, text="(OR)", height=1, justify="center"
        )
        label_place_msg.grid(
            row=1, column=0, rowspan=1, columnspan=2, sticky="", padx=10, pady=10
        )
        label_favourite = tk.Label(
            tab1,
            font=MY_FONT,
            text="Favourite Places:  ",
            height=1,
            justify="center",
        )
        label_favourite.grid(
            row=2, column=0, rowspan=1, columnspan=1, sticky="E", padx=(10, 0), pady=10
        )
        entry_place = tk.Entry(tab1, font=MY_FONT, justify="center")
        entry_place.grid(
            row=0, column=1, columnspan=1, sticky="W", padx=(0, 10), pady=10
        )

        place_list_items = list(place_list.keys())
        combo_favourite = ttk.Combobox(
            tab1, values=list(place_list_items), font=MY_FONT, justify="center"
        )
        combo_favourite.grid(
            row=2, column=1, columnspan=1, sticky="W", padx=(0, 10), pady=10
        )

        label_output_1 = tk.Label(tab1, font=MY_FONT, height=30, justify="left")
        label_output_1.grid(
            row=0, column=2, rowspan=5, columnspan=2, sticky="NSEW", padx=10, pady=10
        )

        button_place_1 = tk.Button(
            tab1,
            text="Get Weather 🔍",
            font=MY_FONT,
            command=weather_call_1,
            justify="center",
            relief="raised",
            fg="#ffffff",
            background="#0052cc",
        )
        button_place_1.grid(row=3, column=0, columnspan=2, sticky="", padx=10, pady=10)

        label_place_1 = tk.Label(
            tab1, text="Hello, Start your weather search!!", font=MY_FONT
        )
        label_place_1.grid(
            row=4, column=0, columnspan=2, sticky="NSEW", padx=10, pady=10
        )

        # for tab 2----------------------------------
        def weather_call_2():
            """weather call function for the second tab and display the fetched output with alignments

            Returns:
                boolean: returns an error if any
            """
            # clear the label
            label_output_2.configure(text="")
            # check the input latitude
            try:
                place_latitude = float(entry_latitude.get())
                if not (-90 <= place_latitude and place_latitude <= 90):
                    raise TypeError("Enter a valid latitude value..")
            except TypeError as e:
                print(e)
                label_output_2.configure(text=e)
                messagebox.showwarning("Warning", str(e))
                return False
            except:
                entry_latitude.delete(0, tk.END)
                print("Invalid Input in latitude, Try Again..")
                label_output_2.configure(text="Invalid Input in latitude, Try Again..")
                messagebox.showwarning(
                    "Warning", str("Invalid Input in latitude, Try Again..")
                )
                return False
            # check the input longitude
            try:
                place_longitude = float(entry_longitude.get())
                if not (-180 <= place_longitude and place_longitude < 180):
                    raise TypeError("Enter a valid longitude value..")
            except TypeError as e:
                print(e)
                label_output_2.configure(text=e)
                messagebox.showwarning("Warning", str(e))
                return False
            except:
                entry_longitude.delete(0, tk.END)
                print("Invalid Input in longitude, Try Again..")
                label_output_2.configure(text="Invalid Input in longitude, Try Again..")
                messagebox.showwarning(
                    "Warning", str("Invalid Input in longitude, Try Again..")
                )
                return False
            # clear the latitude and longitude entry boxes
            entry_latitude.delete(0, tk.END)
            entry_latitude.insert(0, "Please Wait!!")
            entry_longitude.delete(0, tk.END)
            entry_longitude.insert(0, "Please Wait!!")
            # prepare the place string
            place = f"{str(place_latitude)},{str(place_longitude)}"

            label_place_2.configure(text="Entered place: " + place)
            # fetch the user name and api key
            USER = entry_user.get()
            API_KEY = entry_api.get()
            # create a json for fetch

            data = json.dumps({"user": USER, "api-key": API_KEY, "place": place})
            try:
                response = requests.get("http://127.0.0.1:45000/", json=data)
            except Exception as e:
                print("Unable to connect to flask api")
                label_output_2.configure(text="Unable to connect to flask api")
                entry_latitude.delete(0, tk.END)
                entry_longitude.delete(0, tk.END)
                label_place_2.configure(background="#FF0000")
                messagebox.showerror("Error", "Unable to connect to flask api")
                return False

            # if the response is received
            if response.ok:
                # get the json from response
                dictionary = response.json()
                if dictionary["status"] == "false":
                    print(dictionary["reason"])
                    label_output_2.configure(text=str(dictionary["reason"]))
                    entry_latitude.delete(0, tk.END)
                    entry_longitude.delete(0, tk.END)
                    label_place_2.configure(background="#FF0000")
                    messagebox.showwarning("Warning", str(dictionary["reason"]))
                    return False
                # add a parameter in case for ordering
                dictionary["s.no"] = len(place_list)
                place_list[dictionary["area_name"]] = dictionary

                print("Successfully fetched the data")
                label_output_2.configure(
                    text=output_string_creator(place_list[dictionary["area_name"]])
                )
                entry_latitude.delete(0, tk.END)
                entry_longitude.delete(0, tk.END)
                # get the place items
                global place_list_items
                place_list_items = list(place_list.keys())
                combo_favourite.configure(values=place_list_items)
                label_place_2.configure(background="#00FF00")
                return {dictionary["area_name"]: dictionary}

            else:
                # return in case of error
                print("response not found")
                label_output_2.configure(text="response not found")
                label_place_2.configure(background="#FF0000")
                messagebox.showerror("Error", "response not found")
                entry_latitude.delete(0, tk.END)
                entry_longitude.delete(0, tk.END)
                return False

        # creation of the label and widgets
        label_latitude = tk.Label(
            tab2, font=MY_FONT, text="Enter Latitude", height=1, justify="center"
        )
        label_latitude.grid(
            row=0, column=0, rowspan=1, columnspan=1, sticky="ES", padx=(10, 0), pady=10
        )

        label_longitude = tk.Label(
            tab2, font=MY_FONT, text="Enter Longitude", height=1, justify="center"
        )
        label_longitude.grid(
            row=1, column=0, rowspan=1, columnspan=1, sticky="NE", padx=(10, 0), pady=10
        )

        entry_latitude = tk.Entry(tab2, font=MY_FONT, justify="center")
        entry_latitude.grid(
            row=0, column=1, columnspan=1, sticky="WS", padx=(0, 10), pady=10
        )

        entry_longitude = tk.Entry(tab2, font=MY_FONT, justify="center")
        entry_longitude.grid(
            row=1, column=1, columnspan=1, sticky="NW", padx=(0, 10), pady=10
        )

        label_output_2 = tk.Label(tab2, font=MY_FONT, height=30, justify="left")
        label_output_2.grid(
            row=0, column=2, rowspan=5, columnspan=2, sticky="NSEW", padx=10, pady=10
        )

        button_place_2 = tk.Button(
            tab2,
            text="Get Weather 🔍",
            font=MY_FONT,
            command=weather_call_2,
            justify="center",
            relief="raised",
            fg="#ffffff",
            background="#0052cc",
        )
        button_place_2.grid(row=3, column=0, columnspan=2, sticky="", padx=10, pady=10)

        label_place_2 = tk.Label(
            tab2, text="Hello, Start your weather search!!", font=MY_FONT
        )
        label_place_2.grid(
            row=4, column=0, columnspan=2, sticky="NSEW", padx=10, pady=10
        )

        # ----------------window setup
        # bind the required parameters to the win and perform
        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                from signal import SIGINT
                os.kill(os.getpid(), SIGINT)

        win.protocol("WM_DELETE_WINDOW", on_closing)
        win.bind(
            "<Configure>", lambda event: maintain_aspect_ratio(event, WIDTH / HEIGHT)
        )
        win.state("zoomed")
        win.mainloop()
    # incase of any unknown future errors
    except Exception as e:
        print(e)
        pass


if __name__ == "__main__":
    import threading

    # starting a thread to make tkinter work independently
    t = threading.Thread(target=tkinter_call)
    t.start()
    # intialize the ports and the debug mode in flask api
    app.run(debug=False, host="0.0.0.0", port=PORT, threaded=True)
