import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",  # Or the correct IP address/hostname
        port=3306,         # Or the correct port
        user="root",
        password="Métronome",
        database="your_database"
    )
    if connection.is_connected():
        print("Connected to MySQL database")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("MySQL connection closed")