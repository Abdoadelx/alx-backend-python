#!/usr/bin/python3
"""
This module provides a memory-efficient way to calculate the average age
of users by streaming data from a database using a generator.
"""
import mysql.connector
import os

# --- Database Credentials ---
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', '')
DB_NAME = 'ALX_prodev'

def stream_user_ages():
    """
    Connects to the database and yields the age of each user one by one.
    """
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        cursor = connection.cursor()
        
        # Select only the 'age' column to be efficient
        cursor.execute("SELECT age FROM user_data;")
        
        # This loop iterates over the cursor, fetching rows one by one
        for (age,) in cursor:
            yield age
            
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        # Ensure resources are always freed
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    total_age = 0.0
    user_count = 0
    
    # Get the generator that will stream ages
    age_generator = stream_user_ages()
    
    # This loop consumes the generator, updating totals with each yielded age
    for age in age_generator:
        total_age += age
        user_count += 1
        
    if user_count > 0:
        average_age = total_age / user_count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users found to calculate an average age.")
