# SDLC: Python Web Forecast Flask API

---

## Table of contents

- [QuickStart](#quickstart)
- [Initial Setup & Usage](#initial-setup---usage)
  * [Flask Endpoint](#flask-endpoint)
    + [flask-api images](#flask-api-images)
  * [GUI](#gui)
    + [tkinter gui images](#tkinter-gui-images)
  * [Jupyter](#jupyter)
    + [jupyter notebook images](#jupyter-notebook-images)
- [Modules Used](#modules-used)
  * [flask_api](#flask-api)
  * [tkinter_gui](#tkinter-gui)
  * [jupyter_code](#jupyter-code)
- [Testing](#testing)
  * [test run images](#test-run-images)
- [References](#references)
- [Link To Relevant Work Items and Reference Models](#link-to-relevant-work-items-and-reference-models)

---

## QuickStart

- To quick start working on the weather app, Open the [all.exe](/src/exe_file/all.exe) and run the app, with required permissions, That's it!!. Enjoy the app without any other installations on the go.

> - Note: Have the files db.sqlite3, config.ini and weather.png in parallel to all.exe file or else default settings will be getting utilized.
> - create the db.sqlite3 using the [user_addition.py](/src/flask_api/user_addition.py) with required user and apikey.

---

## Initial Setup & Usage

### Flask Endpoint

- Install the required libraries and dependencies from the requirements.txt
- Open and run the file app.py from the src/flask which has the flask api for the weather fetch and then use it for the data fetch.
- the config.ini file has to be placed in parallel to the run app.py file in which consists of the following syntax.

```ini
[settings]
port = 45000
db_path = "db.sqlite3"
```

- use the user_addition.py form arc/flask_api for the user table/ db.sqlite3 creation or to create a new api key key and the user name.
- the default initial data is user =  'admin' and api-key = '123'.
- the creatd db path can be configured from the config.ini file.
- then run the api_analysis_notebook.ipynb from the src/jupyter_code to check the usage and the fuctionalities of the api or just open the main.py from the src/tkinter_gui to run the gui version of the app.
- several error message are been provided for differrent types of errors and hence they can be utilized  and accessed by the user in the returned json file under the parameter name 'reason' and a status parameter with true and false with different fetch data.

> the zipcode can also be entered in name inputs, in both gui and notebook interfaces.

#### flask-api images

- Initialization
![Flask API Initiation](/docs/images/flask_api.png)

- Fetch result display
![Flask API Fetch Result](/docs/images/flask_api_fetch_result.png)

### GUI

- the usage of the GUI has the place entry filel where the data of place or the zipcode or the name of any famous place(eg. tajmahal, effiel tower etc.) can be typed and searched.
- the proper error mesaages are displayed in case of any errors in red color.
- the temperature and other weather parameters are fetched from the api and shown in the gui.
- the empty search lead to the fetch of the weather report from the server ip address location of the access point.
- the recent searces are present in the dropdon of the name-search tab from which the recent search places can be accessed.

#### tkinter gui images

- Tkinter Name_search
![Tkinter Name_search](/docs/images/tkinter_name_search.png)

- Tkinter Lat/Lon_search
![Tkinter Lat/Lon_search](/docs/images/tkinter_lat-lon_search.png)

### Jupyter

- the setup of the jupyter notebook has been shown and utilized for the purpose fo the match utilization.
- follow the instruction that are present in the markdown of the jupyter file and proceed for the further testing of the api-endpoints.

#### jupyter notebook images

- Jupyter Fetch Results
![Jupyter Fetch Results](/docs/images/jupyter_fetch_results.png)

- Jupyter Plot Results
![Jupyter Plot Results](/docs/images/jupyter_plot_results.png)

- Jupyter Plot
![Jupyter Plot](/docs/images/jupyter_plot.png)

---

## Modules Used

### flask_api

- check_dictionary:

```
function to check the dictionary for all the parameters

Args:
    dictionary (dict): a dictionary of the weather data accessign json file

Returns:
    boolean: true if errors present in the dictionary
```

- prepare_dictionary:

```
a function to prepare a dictionary of required parameters from the api returned object

Args:
    forecast (pywttr object): return object of the weather data
    dictionary (a dictionary of get json data): json data send from user in form of dictionary

Returns:
    dictionary: prepared dictionary
```

- home

```
basic function call for flask api endpoint

Returns:
    json: the prepared json with weather data is sent
```

### tkinter_gui

- maintain_aspect_ratio

```
Event handler to override root window resize events to maintain the
specified width to height aspect ratio.
```

- align_string

```
align the received parameters strings with equal spacings

Args:
    s (string): output strings

Returns:
    string: equally spaced string with equal lengths
```

- output_string_creator

```
convert the dictionary of paramerts into string with newline characters

Args:
    dictionary (dict): weather dictionary

Returns:
    string: output display string
```

- weather_call_1

```
weather call function for the first tab and display the fetched output with alignments

Returns:
    boolean: returns an error if any
```

- weather_call_2

```
weather call function for the second tab and display the fetched output with alignments

Returns:
    boolean: returns an error if any
```

### jupyter_code

- weather_call

```
weather api call to request json data from the flask end point

Args:
    place (string): the palce entered by the user for the weather loation detection

Returns:
    dictionary:  the response data in form of dictionary from the request fetch
```

- get_place

```
the function gets the place from the user in the form of name or in the latitude and the longitude format.
Raises:
    TypeError: incase of input other than the specified one in entered

Returns:
    string: the user entered location or coordinates
```

---

## Testing

- the testing was done using the `pytest` library.
- seperate tests were conducted for the flask and tkinter gui.
- the [testing_plan](/test/testing%20plan.xlsx) can be seen to have a brienf idea on the testing plan and the tests performed on the api and gui.

### test run images

- All Test run results
![All Test run results](/docs/images/all%20test%20run.png)

- Specific Test run results
![Specific Test run results](/docs/images/specific%20test%20run.png)

---

## References

- [Final app(exe file)](/src/exe_file/)

- [Documentation](/docs/)

- [Source Code](/src)
  - [Flask API Code](/src/flask_api)
  - [Tkinter GUI Code](/src/jupyter_code)
  - [Jupyter Notebook Code](/src/jupyter_code)

- [User manual](/README.md)
- [Tests](/test/)

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
