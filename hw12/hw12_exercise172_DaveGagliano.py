## Dave Gagliano
## CIS 2532 NET01
## Professor Shamsuddin
## 14 May 2022

## this program is an exercise taken from section 17.2 in Chapter 17 
## from the book "Intro to Python for Computer Science and Data Science 
## by Paul Deitel and Harvey Deitel


## this program will set up a database using SQLite

## 17.2 A Books Database

import sqlite3


# connects to a database and create a connection object
connection = sqlite3.connect('ch17/books.db')

# use an SQL query and pandas to view the contents
import pandas as pd

pd.options.display.max_columns = 10

# execute an SQL query and return a DataFrame containing the query's results
print(pd.read_sql('SELECT * FROM authors', connection, index_col=['id']))

print("")

# use an SQL query to view the titles table and its contents
print(pd.read_sql('SELECT* FROM titles', connection))

print("")

# use SQL and pandas to view the five rows from the author_ISBN table
df = pd.read_sql('SELECT * FROM author_ISBN', connection)
print(df.head())

print('')