## ***Cities***

### Overview

An application that provides some basic information about chosen cities worldwide,
including their coordinates, current date and time, weather conditions.

The program is built using object-oriented programming principles, 
utilizing classes to organize the functionality for fetching, processing,
and displaying city data.

### Usage:

The app's main functionality is handled by two classes:

- CityApi class communicates with external free APIs (Wikipedia, GeoNames, OpenMeteo) to fetch and store data in JSON format. 
- City class organizes the raw data and returns it as a dictionary, providing easy access via class attributes to the city's key information.

This dictionary is then used to construct an ASCII table, which the user can view in the console or optionally save to a .txt file.

Notes:

Please keep in mind that the APIs used in this project are keyless and free, so some limitations may apply.

