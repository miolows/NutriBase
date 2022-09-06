# NutriBase
NutriBase is a Python language program that implements food data into a MySQL database.

## Introduction
NutriBase has three main features:
* providing full support for any REST API endpoint providing access to the [USDA food database](https://fdc.nal.usda.gov/api-guide.html),
* filtering of collected data,
* providing basic MySQL database functionality (creating a database and tables, defining relationships between tables, creating arbitrary sql queries) and specific ones to simplify interaction with the database directly related to this project.

## Setup
Project requirements are listed in the requirements.txt file:
```
pip install -r requirements.txt
```

## Current Issue
The USDA database provides a wide range of food products, but their practical use can be problematic. All of the product details are part of their name, making it very difficult to filter them out with a sql query. The naming system is not uniform, making it even more difficult to manually separate the details from the main product name. However, this may be unavoidable in further development of the project.

## Contact
Created by [@miolows](olowskimi@outlook.com) - feel free to contact me!