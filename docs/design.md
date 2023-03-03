# Design Documentation

## Table Of Contents
* [Project Statement](#project-statement)
* [Link To Relevant Work Items and Reference Models](#link-to-relevant-work-items-and-reference-models)
* [Implementation / Design](#implementation---design)
    + [`Flask`](#-flask-)
    + [`tkinter`](#-tkinter-)
    + [`jupyter`](#-jupyter-)
* [Alternative Implementations / Designs](#alternative-implementations---designs)
* [Future Updates](#future-updates)
* [Open Issues](#open-issues)


---

## Project Statement

The objective is to develop a Weather Forecast Web/Data App using Flask. The app should allow users to get the latest weather information from different locations. Users should be able to search for weather information based on location, and the app should display detailed weather information about the searched location in JSON format when used via Browser.

---

## Link To Relevant Work Items and Reference Models

- Python Web framework for Endpoint API - [Flask](https://flask.palletsprojects.com/en/2.2.x/)

- Weather API - [pywttr](https://pypi.org/project/pywttr/)

- Whether Website-Example- [wttr](https://wttr.in/)

- Python GUI - [tkinter](https://docs.python.org/3/library/tkinter.html)

- Python Graph viewer - [Jupyter Notebook] (<https://jupyter.org/>)  

- Libraries Used -

    - [Flask](https://pypi.org/project/Flask/)

    - [pywttr](https://pypi.org/project/pywttr/)

    - [tkinter](https://docs.python.org/3/library/tkinter.html#module-tkinter)

    - [requests](https://pypi.org/project/requests/)

    - [Json](https://docs.python.org/3/library/json.html)

    - [jupyter](https://pypi.org/project/jupyter/)

---

## Implementation / Design

- the three codependent file systems must made, and they are:

  - Web endpoint [Flask]

  - GUI interface [tkinter]

  - Graph analyzer [jupyter]

### `Flask`  

- to create a flask app as an endpoint which accepts Json data, fetches the weather report, and resends the data in Json form to the fetcher.

- a config.ini file has been created and placed parallel for the adjustment of the settings of the flask interface.

- the config.ini consists of the following parameters of `port` and `db_path`

> `port` - flask port number, `db_path` - path for the db file with user data

- the `db_path` is checked if there is any file exists and used, else the default file path is used which is pwd of flask app.

- the flask app must check the incoming Json data based on various parameters present and return it in case successful fetch or error message with proper information in Json format with status parameter as false.

- each and every user has diffrent user and api-key credentials which are maintained in `db.sqlite3` file.

- the **api-key** is **hashed** before storing in the database

- the place data in the Json file can be any location in the world including the names of famous well-known monuments.(e.g.- Taj mahal, Eiffel tower)

- the addition of authentication parameters in Json is must for the tkinter and jupyter interfaces for the successful authentication of the user.

- the data from the endpoint must be accurate and lively updated.

- whether parameters like (`temperature, Humidity, windspeed, visibility, pressure`)  

> Here are contents for the **config.ini** file
 ```ini
[settings]
# port number for flask api
port = 45000
# path for the database
db_path = "db.sqlite3"
```

### `tkinter`  

- to create an GUI interface with the help of tkinter library, get the values from user of two different

- a config.ini file has been created and placed parallel for the adjustment of the settings of the tkinter interface.

- the two columns for the search to be present with place name and latitude/longitude.

- the input data is verified before the creation of the Json file for the fetch.

- the output is shown with the labels of the temperature, humidity, etc.

- the table of previous fetched whether data is to be displayed

- the config.ini file can have the username and password.

- the port and the endpoint can also be configured through the config.ini file

- the Json file has been created for the weather data fetch.

- the data which was previously fetched can also be used instead of frequent fetch from the Api.

### `jupyter`  

- to create a jupyter notebook for the graphical data analysis of temperature.

- to create a list of favorited cities and display their cities vs temperature/humidity plot in jupyter notebook.

- a config.ini file has been created and placed parallel for the adjustment of the settings of the jupyter interface.  

- a graphical plot curve is displayed and can be updated regularly

- the pandas dataframe is used for the data process

- the plot for the various parameters can be done using notebook

- the user is asked for the favorite cities in the prompt

- the data is checked and verified before calling for the fetch and the output is displayed in case error messages

- the data inserted by the user can be modified in case of incorrect entry.

---

## Data Flow Diagram

### Overall flow
![Overall Flow](/docs/images/full%20data%20flow.png)

### Flask flow
![Flask flow](/docs/images/flask.png)

### Tkinter flow
![Tkinter flow](/docs/images/tkinter.png)

### Jupyter flow
![Jupyter flow](/docs/images/jupyter.png)

---

## Alternative Implementations / Designs  

To create a flask app with multiple endpoints for each type of fetch call.

- do the authorization and data fetch in two different steps

- usage of rest Api in flask and html/CSS GUI instead of tkinter

---

## Future Updates

- Addition of further whether parameters and hourly and daily updates

- addition of SQL, Json data for user creation and deletion  

- allocation different Api keys for each user

---

## Open Issues

- the weather report from latitude and longitude search for the unknown locations like the places in-between the oceans or such is not obtained from Api.
