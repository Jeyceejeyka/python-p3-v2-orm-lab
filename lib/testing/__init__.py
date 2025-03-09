import sqlite3

# Establish a connection to the database
CONN = sqlite3.connect('test_database.db')  # Adjust the database name as needed
CURSOR = CONN.cursor()
