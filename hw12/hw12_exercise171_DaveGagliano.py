## Dave Gagliano
## CIS 2532 NET01
## Professor Shamsuddin
## 14 May 2022

## this program is exercise 17.1 in Chapter 17 
## from the book "Intro to Python for Computer Science and Data Science 
## by Paul Deitel and Harvey Deitel


## 17.1 Books Database

import sqlite3
import pandas as pd

# connects to a database and create a connection object
connection = sqlite3.connect('ch17/books.db')

# return the table names
print(pd.read_sql_query("""SELECT name 
                  FROM sqlite_master 
                  WHERE TYPE= 'table'
                  """, connection), '\n')
                  


# a) Select all authors' last names from the authors table in descending order

# I used two different ways to sort, one with pandas (a way that I knew) 
# and the new way with SQL to compare the two 

# use SQL query to return a dataframe with the query's results 
# and sort in descending order by last name using pandas
df_authors = pd.read_sql('SELECT * FROM authors', connection)
df_authors_sorted = df_authors.sort_values('last', ascending=False)
print('Sorting using pandas')
print(df_authors_sorted, '\n')


print('Sorting using SQL')
print(pd.read_sql("""
            SELECT * 
            FROM authors
            ORDER BY last DESC
            """, connection),'\n')
        
            
        
# b) Select all book titles from the titles table in ascending order

# I used two different ways to sort, one with pandas (a way that I knew) 
# and the new way with SQL to compare

# use SQL query to retrun a dataframe with the query's results 
# and sort in ascending order with pandas
df_titles = pd.read_sql('SELECT * FROM titles', connection)
df_titles_sorted = df_titles.sort_values('title')
print(df_titles_sorted, '\n')


# use SQL query to retrun a dataframe with the query's results 
# and sort in ascending order with SQL
print(pd.read_sql("""
            SELECT * FROM titles
            ORDER BY title ASC
            """, connection), '\n')
            
            
            
# c) use an INNER JOIN to select all the books from a specific author. 
#    Include the title, copyright year, and ISBN. 
#    Order the information alphabetically by title.

# use SQL query to retrun a dataframe with the query's results
firstname= 'Paul'
lastname = 'Deitel'

# this was just to test my code
# print(pd.read_sql("""
#             SELECT * 
            
#             FROM authors 

#             WHERE first LIKE 'Paul' AND  last LIKE 'Deitel'
#             """, connection))


# use SQL query to retrun a dataframe with the query's results
firstname= 'Paul'
lastname = 'Deitel'

def select_all_books_author(firstname, lastname):
    
    return pd.read_sql(f"""
                        SELECT 
                        authors.first, 
                        authors.last, 
                        titles.title, 
                        titles.copyright, 
                        titles.isbn
           
                        FROM authors
                
                        INNER JOIN author_ISBN
                            ON authors.id = author_ISBN.id
            
                        INNER JOIN titles
                            ON author_ISBN.isbn = titles.isbn
                
                        WHERE authors.first LIKE '{firstname}' AND  
                        authors.last LIKE '{lastname}'
                
                        ORDER BY title ASC
                        """, connection)
                        
# display output in program
print(select_all_books_author(firstname, lastname), '\n')     


# d) Insert a new author into the authors table

# create a cursor object 
cursor = connection.cursor()

# add a new author to the table
cursor = cursor.execute("""
                        INSERT INTO authors (first, last)
                        VALUES('Al', 'Sweigart')
                        """)
                        
print(pd.read_sql("""
            SELECT * FROM authors
            """, connection),'\n')
            


# e) Insert a new title for an author. 
#    Remember that the book must have an entry in the author_ISBN table 
#    and an entry in the titles table

# return the table names
print(pd.read_sql_query("""
                  SELECT name 
                  FROM sqlite_master 
                  WHERE TYPE= 'table'
                  """, connection), '\n')

firstname = 'Al'
lastname = 'Sweigart'
title = "Automate the Boring Stuff"
book_copyright = '2015'
edition = '1'
isbn_book = '1593275994'


author_id_series = pd.read_sql(f"""
                               SELECT authors.id FROM authors
           
                                WHERE authors.first LIKE '{firstname}' 
                                AND authors.last LIKE '{lastname}'
                                """, connection)

# get author id from authors table
author_id = author_id_series.iloc[0].values[0]
# print(author_id)


# insert new value into author_ISBN book
cursor = cursor.execute(f"""
                        INSERT INTO author_ISBN (id, isbn)
                        VALUES('{author_id}', '{isbn_book}')
                        """)

# delete if necessary
# cursor = cursor.execute(f"""
#                             DELETE FROM author_ISBN 
#                             WHERE isbn='{isbn_book}'
#                          """)


# read the last 5 contents of the author_ISBN table to see new entry
print(pd.read_sql("""
            SELECT* from author_ISBN
            """, connection).tail(), '\n')
            
            
# insert new entry into titles table
cursor = cursor.execute(f"""
                        INSERT INTO titles(isbn, title, edition, copyright)
                        VALUES('{isbn_book}', 
                               '{title}', 
                               '{edition}', 
                               '{book_copyright}')
                        """)
                        
print(pd.read_sql(f"""
            SELECT * FROM titles
            WHERE isbn LIKE '{isbn_book}'
            """, connection),'\n')
            

# display output in program
print(select_all_books_author(firstname, lastname))  

# close connection with database
connection.close()