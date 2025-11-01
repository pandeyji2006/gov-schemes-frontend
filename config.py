"""
Configuration file for Flask Chatbot Application

This file contains all configuration values for the Flask app and MySQL database.
IMPORTANT: Keep this file secure and do not commit sensitive credentials to version control.
"""

# Flask Configuration
# SECRET_KEY is used for session encryption and security
# IMPORTANT: Change this to a long random string in production!
# You can generate one with: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY = 'your-secret-key-here-change-in-production'

# MySQL Database Configuration
# Update these values to match your MySQL server setup

# The hostname or IP address of your MySQL server (default: localhost)
MYSQL_HOST = 'localhost'

# The MySQL username (change 'root' to your MySQL user)
MYSQL_USER = 'root'

# The MySQL password for the above user (SET THIS before running the app)
MYSQL_PASSWORD = ''

# The name of the database to use (default: chatbot_db)
# This database will be created when you run schema.sql
MYSQL_DB = 'chatbot_db'

# The port MySQL is running on (default: 3306)
MYSQL_PORT = 3306
