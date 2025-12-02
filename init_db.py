import mysql.connector
from mysql.connector import errorcode

DB_NAME = "filmdb"
SCHEMA_FILE = "schema.sql"

config = {
    "user": "root",
    "password": "",   # ← Guys, change it to your password if you have one:)
    "host": "localhost",
    "port": 3306
}


def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8mb4'")
        print(f"✔ Database '{DB_NAME}' ready.")
    except mysql.connector.Error as err:
        print(f"❌ Failed creating database: {err}")
        exit(1)


def execute_schema(cursor):
    print("Reading schema.sql ...")
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        sql_commands = f.read()

    # MySQL does not support executing multiple statements at once
    # We need to manually split
    commands = sql_commands.split(";")

    print("Executing schema commands...")
    for command in commands:
        cmd = command.strip()
        if cmd == "":
            continue
        try:
            cursor.execute(cmd)
        except mysql.connector.Error as err:
            print(f"❌ Error executing: {cmd}\nError: {err}")
            exit(1)

    print("✔ Schema executed successfully.")


def main():
    # connect to MySQL, without specifying a database
    print("Connecting to MySQL...")
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # create database
    create_database(cursor)

    cnx.database = DB_NAME

    # execute schema.sql
    execute_schema(cursor)

    cursor.close()
    cnx.close()
    print("Database initialized successfully!")


if __name__ == "__main__":
    main()