#!/usr/bin/python3
"""
This module provides a generator for lazy pagination of user data.
"""
import mysql.connector
import os

# --- Database Credentials ---
# Best practice is to use environment variables for sensitive data.
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', '')
DB_NAME = 'ALX_prodev'

def connect_to_prodev():
    """Connects to the ALX_prodev database in MySQL."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database '{DB_NAME}': {err}")
        return None

def paginate_users(page_size, offset):
    """
    Fetches a single page of users from the database.

    Args:
        page_size (int): The number of users to fetch.
        offset (int): The starting point from which to fetch users.

    Returns:
        list: A list of user dictionaries for the requested page.
    """
    connection = connect_to_prodev()
    if not connection:
        return []
        
    rows = []
    try:
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Database query error: {err}")
    finally:
        if connection.is_connected():
            connection.close()
    return rows

def lazy_pagination(page_size):
    """
    A generator that lazily fetches pages of users from the database.
    It only queries for the next page when it is needed.

    Args:
        page_size (int): The number of users per page.

    Yields:
        list: A page (list of user dictionaries).
    """
    offset = 0
    # This single loop continues as long as pages with data are returned.
    while True:
        # Fetch the next page of users from the database.
        page = paginate_users(page_size=page_size, offset=offset)
        
        # If the returned page is empty, there's no more data to fetch.
        if not page:
            break
            
        # Yield the current page to the caller.
        yield page
        
        # Increment the offset to prepare for the next page request.
        offset += page_size
