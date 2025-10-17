import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # 🔹 your MySQL username
            password="deepak123",  # 🔹 your MySQL password
            database="Student_DB"
        )

        if connection.is_connected():
            # print("Connection to MySQL DB was successful!")
            return connection

    except Error as e:
        print("Error while connecting to MySQL:", e)

# if __name__ == "__main__":
#     conn = get_connection()
#     if conn:
#         print("Connection object:", conn)
#         conn.close()
