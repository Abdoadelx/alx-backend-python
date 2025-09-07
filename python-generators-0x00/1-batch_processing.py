#!/usr/bin/python3
"""
This module provides functions to fetch and process user data in batches.
"""
import mysql.connector
import os

# --- Database Credentials ---
# Best practice is to use environment variables for sensitive data.
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', '')
DB_NAME = 'ALX_prodev'

def stream_users_in_batches(batch_size=100):
    """
    Connects to the database and yields user data in batches.

    Args:
        batch_size (int): The number of rows to fetch in each batch.

    Yields:
        list: A list of user dictionaries, representing a batch.
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
        
        # Loop indefinitely to fetch batches until the result set is exhausted
        while True:
            # fetchmany() retrieves a specific number of rows
            batch = cursor.fetchmany(batch_size)
            # If the batch is empty, we've processed all rows
            if not batch:
                break
            # Yield the current batch to the caller
            yield batch
            
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        # Ensure the cursor and connection are closed to free up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def batch_processing(batch_size):
    """
    Processes batches of users to filter those over the age of 25.

    Args:
        batch_size (int): The size of batches to retrieve and process.
    """
    # Get the generator that streams batches of users
    user_batch_generator = stream_users_in_batches(batch_size)
    
    # Loop through each batch provided by the generator
    for batch in user_batch_generator:
        # Loop through each user in the current batch
        for user in batch:
            # Process the user: filter by age
            if user['age'] > 25:
                # Print the processed user record
                print(user)
