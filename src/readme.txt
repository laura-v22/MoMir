====================
    GENERAL INFO
====================
- The application is split in pages.
- Each page is split in tabs, if necessary.
- Each page loads its data as global variables.
- IDs for callbacks need to go through utils.utils.id_factory to disambiguate them.


===========================
    DIRECTORY STRUCTURE
===========================
src/
|-- app.py
|-- data/
|   |-- baptistery/
|   |-- square/
|   |-- tower/
|   |-- ...
|-- pages/
|   |-- home.py
|   |-- baptistery/
|   |   |-- baptistery.py
|   |   |-- baptistery_data.py
|   |   |-- functions.py
|   |-- square/
|   |   |-- ...
|   |-- tower/
|   |   |-- ...
|   |-- ...
|-- utils/
|   |-- styles.py
|   |-- utils.py


==========================
    NAMING CONVENTIONS
==========================
- Variables have lowercase names with underscores:
    example_variable
- Functions have camelCase names:
    def exampleFunction(...)
- Callback function names begin with 'call'. Following that, they contain information about the type of object they update, and finally about the data. For example, a callback function which updates a Div with images of crack plots is called:
    def callDivCrackPlots(...)
