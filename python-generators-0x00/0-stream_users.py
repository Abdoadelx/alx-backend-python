#!/usr/bin/python3
"""
This module contains a generator function to stream user data from a database.
"""
import mysql.connector
import os

# --- Database Credentials ---
# Best practice is to use environment variables for sensitive data.
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', '')
DB_NAME = 'ALX_prodev'

def stream_users():
    """
    Connects to the user_data table and yields rows one by one.
    This function uses a generator to efficiently stream data without
    loading the entire table into memory.
    """
    connection = None
    cursor = None
    try:
        # Establish a connection to the specific database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        
        # Using dictionary=True makes the cursor return rows as dictionaries
        cursor = connection.cursor(dictionary=True)
        
        # Execute the query to fetch all users
        cursor.execute("SELECT * FROM user_data;")
        
        # This single loop iterates over the cursor,
        # which fetches rows one by one from the database.
        for row in cursor:
            yield row
            
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        # Ensure the cursor and connection are closed to free up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
