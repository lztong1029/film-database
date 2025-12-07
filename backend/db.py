#!/usr/bin/env python3
"""
Database Connection Module
MPCS 53001 Database Final Project - Step 3

This module handles all MySQL database connections and query execution.
Uses mysql-connector-python for database connectivity.
"""

import mysql.connector
from mysql.connector import Error
from typing import List, Tuple, Optional, Any

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "mysqlpass166"          # e.g. "mypassword" if you set one
DB_NAME = "filmdb"


# ============================================================================
# CONNECTION MANAGEMENT
# ============================================================================

def get_connection():
    """
    Create and return a new MySQL database connection.

    Returns:
        mysql.connector.connection.MySQLConnection: Active database connection
        None: If connection fails
    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )

        if connection.is_connected():
            # db_info = connection.get_server_info()
            # print(f"Successfully connected to MySQL Server version {db_info}")
            return connection
        else:
            print("Failed to connect to MySQL Server")
            return None

    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


# ============================================================================
# QUERY EXECUTION FUNCTIONS
# ============================================================================

def run_select_query(sql: str, params: Optional[Tuple] = None) -> Tuple[List[Tuple], List[str]]:
    """
    Execute a SELECT query and return results with column names.

    Args:
        sql (str): SQL SELECT query with optional %s placeholders
        params (tuple, optional): Parameters for parameterized query

    Returns:
        tuple: (rows, column_names)
            rows (list of tuples): Query results
            column_names (list of str): Column names from cursor.description
    """
    connection = None
    cursor = None
    rows: List[Tuple] = []
    column_names: List[str] = []

    try:
        connection = get_connection()
        if connection is None:
            print("Failed to get database connection")
            return rows, column_names

        cursor = connection.cursor()

        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        rows = cursor.fetchall()

        if cursor.description:
            column_names = [desc[0] for desc in cursor.description]

        # print(f"Query executed successfully. Retrieved {len(rows)} row(s)")
        return rows, column_names

    except Error as e:
        print(f"Error executing SELECT query: {e}")
        print(f"SQL: {sql}")
        if params:
            print(f"Params: {params}")
        return [], []

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            # print("MySQL connection closed")


def run_insert_query(sql: str, params: Optional[Tuple] = None) -> int:
    """
    Execute an INSERT, UPDATE, or DELETE query and commit the transaction.

    Args:
        sql (str): SQL INSERT/UPDATE/DELETE query with optional %s placeholders
        params (tuple, optional): Parameters for parameterized query

    Returns:
        int: Number of affected rows (rowcount), 0 if query fails
    """
    connection = None
    cursor = None
    affected_rows = 0

    try:
        connection = get_connection()
        if connection is None:
            print("Failed to get database connection")
            return 0

        cursor = connection.cursor()

        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        connection.commit()
        affected_rows = cursor.rowcount

        # print(f"Query executed successfully. {affected_rows} row(s) affected")
        return affected_rows

    except Error as e:
        print(f"Error executing INSERT/UPDATE/DELETE query: {e}")
        print(f"SQL: {sql}")
        if params:
            print(f"Params: {params}")
        if connection:
            connection.rollback()
            print("Transaction rolled back")
        return 0

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            # print("MySQL connection closed")


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def test_connection() -> bool:
    """
    Test the database connection and print server information.

    Returns:
        bool: True if connection successful, False otherwise
    """
    connection = None
    try:
        connection = get_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"MySQL Database Version: {version[0]}")

            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()
            print(f"Current Database: {db_name[0]}")

            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"\nTables in '{DB_NAME}':")
            if tables:
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print("  (No tables found)")

            cursor.close()
            return True

        else:
            print("Connection test failed")
            return False

    except Error as e:
        print(f"Error during connection test: {e}")
        return False

    finally:
        if connection and connection.is_connected():
            connection.close()
            print("\nConnection test completed. Connection closed.")


def execute_script(sql_script: str) -> bool:
    """
    Execute a multi-statement SQL script (e.g., schema creation).

    Args:
        sql_script (str): SQL script containing multiple statements

    Returns:
        bool: True if all statements executed successfully, False otherwise
    """
    connection = None
    cursor = None

    try:
        connection = get_connection()
        if connection is None:
            print("Failed to get database connection")
            return False

        cursor = connection.cursor()

        for result in cursor.execute(sql_script, multi=True):
            if result.with_rows:
                print(f"Statement produced {result.rowcount} rows")
            else:
                print(f"Statement executed: {result.rowcount} rows affected")

        connection.commit()
        print("SQL script executed successfully")
        return True

    except Error as e:
        print(f"Error executing SQL script: {e}")
        if connection:
            connection.rollback()
            print("Transaction rolled back")
        return False

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection closed")


if __name__ == "__main__":
    print("=" * 70)
    print("Testing Database Connection Module")
    print("=" * 70)

    print("\n1. Testing connection...")
    if test_connection():
        print("\n✓ Connection test passed!")
    else:
        print("\n✗ Connection test failed!")
        print("\nPlease check:")
        print("  - MySQL server is running")
        print("  - DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME are correct")
        print("  - Database exists and user has appropriate permissions")
        print("  - mysql-connector-python is installed: pip install mysql-connector-python")

    print("\n" + "=" * 70)
    print("Test completed")
    print("=" * 70)
