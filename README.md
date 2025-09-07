# Python Database Seeding Project

This project provides a Python script to set up a MySQL database named `ALX_prodev`, create a `user_data` table, and populate it with data from a CSV file. This serves as a foundation for building a data streaming generator.

---

## Requirements
* Python 3.x
* MySQL Server
* `mysql-connector-python` library

---

## Setup
1.  **Clone the Repository:**
    ```bash
    git clone <your-repo-url>
    cd python-generators-0x00
    ```

2.  **Install the Python Library:**
    ```bash
    pip install mysql-connector-python
    ```

3.  **Ensure MySQL Server is Running.**

4.  **Set Environment Variables:**
    The script uses environment variables for your database credentials. Set them in your terminal before running the script:
    ```bash
    export DB_HOST='localhost'
    export DB_USER='your_mysql_user'
    export DB_PASS='your_mysql_password'
    ```
    If these variables are not set, the script will default to `localhost`, `root`, and an empty password.

5.  **Create the Data File:**
    Create a file named `user_data.csv` in the same directory and paste the provided user data into it.

---

## Usage
Run the `0-main.py` script to set up the database and insert the data.

```bash
./0-main.py
