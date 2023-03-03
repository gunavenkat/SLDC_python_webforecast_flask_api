# Challenge Documentation

## Challenges faced and their solutions that are implemented

### flask_api

- The initial challenge was faced at the creation of flask Api in recognizing its requests access type in get and post requests, and hence the Json format has been utilized for this purpose.  

- the authentication has been provided by using the user and Api key embedded into the Json file which are then verified and called the weather Api.

- the next hardship was faced when deciding the requirement parameters in the flask app endpoint access and hence the place, user and the Api-key are decided as the basic parameters for the access.

- the storing of data for multiple users requires the access of the memory type which is non-volatile and hence the database of db.sqlite3 has been utilized for the user data storage

- the search of a weather Api was also a tedious task and after several searches the wttr.in has been selected for the utilization of the Api call.

- the filtering of the data from the Api was in a hardcoded format and hence the app with multiple for loops is utilized to overcome this problem.

- the Json data fetched from the user must be verified, which often throws errors, and hence a separate function has been used for the Json checks, then data has been for the further processing.

- then the Json file's creation must be done in python, hence the Json library was used, and Json was created and sent to the user.

### tkinter_gui

- the creation of the proper Gui for the tkinter was a perplexing task since it required many complex actions and hence to make it simple separate tabs has been utilized for both places and latitude/longitude searches.

- the user input must be verified each time, hence separate check functions have been used for filtering purposes.

- the output put data must be filtered and the required parameters displayed, hence the parameters like temperature, humidity, wind measurements have been used.

- the indication of the errors also must be done and to simplify that the background color has been used for this purpose.

- the alignment of the output data was also a tedious task and hence the usage of the align function was created for proper alignment as much as possible

### jupyter_code

- the jupyter code must accept data of latitude/ longitude and the places at the same time and hence the usage of separate function called get_place() has been utilized for this purpose.

- the inputs then having to be converted and hence the Json library has been used for the Json data creation and hence utilized.

- for the sake of plotting purposes, the usage of the favorite places dictionary of storing the recent searches has been utilized to make it simpler for potting.

- filtering and grouping of the data were a tedious task and hence the utilization of the pandas library for the dataframe creation and it is then stored and utilized for the plotting.
