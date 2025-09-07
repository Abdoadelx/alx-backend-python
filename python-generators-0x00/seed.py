#!/usr/bin/python3
"""
This module provides functions to set up and seed the ALX_prodev database.
"""
import mysql.connector
import os
import csv
import uuid

# --- Database Credentials ---
# Best practice is to use environment variables for sensitive data.
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', '')
DB_NAME = 'ALX_prodev'

def connect_db():
    """Connects to the MySQL database server."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_database(connection):
    """Creates the ALX_prodev database if it doesn't already exist."""
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

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

def create_table(connection):
    """Creates the user_data table if it doesn't already exist."""
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3, 0) NOT NULL
        );
        """
        cursor.execute(create_table_query)
        print("Table user_data created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

def insert_data(connection, data_file):
    """Inserts data from a CSV file into the database, avoiding duplicates."""
    try:
        cursor = connection.cursor()
        
        # Using INSERT IGNORE is an efficient way to skip rows with duplicate primary keys.
        insert_query = """
        INSERT IGNORE INTO user_data (user_id, name, email, age)
        VALUES (%s, %s, %s, %s)
        """
        
        with open(data_file, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            header = next(csv_reader)  # Skip the header row
            
            # Prepare data for executemany, generating a UUID for each row
            data_to_insert = [(str(uuid.uuid4()), row[0], row[1], row[2]) for row in csv_reader]

            if data_to_insert:
                cursor.executemany(insert_query, data_to_insert)
                connection.commit()
                print(f"Data from {data_file} inserted successfully.")
            else:
                print("No new data to insert.")

        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    except FileNotFoundError:
        print(f"Error: The file {data_file} was not found.")
