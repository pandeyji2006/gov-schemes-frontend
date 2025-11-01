"""
Database module for Flask Chatbot Application

This module handles all MySQL database operations including:
- Connection management
- Saving messages to database
- Retrieving chat history
- Clearing chat history

All database operations include error handling to prevent app crashes.
"""

import mysql.connector
from mysql.connector import Error
import config


def get_db_connection():
    """
    Create and return a MySQL database connection.

    Returns:
        connection object if successful, None if connection fails

    Uses configuration values from config.py to establish connection.
    """
    try:
        connection = mysql.connector.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB,
            port=config.MYSQL_PORT
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None


def save_message(session_id, sender, message):
    """
    Save a chat message to the database.

    Parameters:
        session_id (str): Unique session identifier (UUID)
        sender (str): Either 'user' or 'bot'
        message (str): The message content to save

    Returns:
        bool: True if successful, False if error occurred

    This function uses parameterized queries to prevent SQL injection.
    """
    connection = get_db_connection()
    if connection is None:
        print("Failed to save message: No database connection")
        return False

    try:
        cursor = connection.cursor()
        query = "INSERT INTO messages (session_id, sender, message) VALUES (%s, %s, %s)"
        cursor.execute(query, (session_id, sender, message))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"Error saving message to database: {e}")
        return False


def get_session_history(session_id, limit=20):
    """
    Retrieve chat history for a specific session.

    Parameters:
        session_id (str): Unique session identifier (UUID)
        limit (int): Maximum number of messages to retrieve (default: 20)

    Returns:
        list: List of dictionaries containing message data
              Each dict has keys: sender, message, timestamp
              Returns empty list if error or no messages found

    Messages are returned in chronological order (oldest first).
    """
    connection = get_db_connection()
    if connection is None:
        print("Failed to retrieve history: No database connection")
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT sender, message, timestamp
            FROM messages
            WHERE session_id = %s
            ORDER BY timestamp DESC
            LIMIT %s
        """
        cursor.execute(query, (session_id, limit))
        results = cursor.fetchall()
        cursor.close()
        connection.close()

        # Reverse the list so oldest messages are first
        results.reverse()
        return results
    except Error as e:
        print(f"Error retrieving session history: {e}")
        return []


def clear_session_history(session_id):
    """
    Delete all messages for a specific session.

    Parameters:
        session_id (str): Unique session identifier (UUID)

    Returns:
        bool: True if successful, False if error occurred

    This is used when user wants to clear their chat history.
    """
    connection = get_db_connection()
    if connection is None:
        print("Failed to clear history: No database connection")
        return False

    try:
        cursor = connection.cursor()
        query = "DELETE FROM messages WHERE session_id = %s"
        cursor.execute(query, (session_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print(f"Error clearing session history: {e}")
        return False
