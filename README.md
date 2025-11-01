# Flask Chatbot Web Application

A clean and modern chatbot web application built with Flask backend and vanilla JavaScript frontend. Features a rule-based chatbot with MySQL database integration for persistent chat history.

## Features

- Clean, centered chat interface with modern design
- Real-time messaging with instant bot responses
- Rule-based pattern matching for bot logic
- MySQL database integration for chat history
- Session-based conversation tracking
- Persistent chat history across page refreshes
- Mobile-friendly responsive design
- Easy-to-customize chatbot patterns

## Prerequisites

Before running this application, ensure you have the following installed:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **MySQL 5.7 or higher** - [Download MySQL](https://dev.mysql.com/downloads/)
- **pip** - Python package manager (included with Python)

## Installation Steps

### 1. Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd gov-schemes-frontend

# Or download and extract the project files
```

### 2. Create a Virtual Environment

Creating a virtual environment keeps your project dependencies isolated.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask 3.0.0 (web framework)
- mysql-connector-python 8.2.0 (MySQL database connectivity)

## Database Setup

### 1. Start MySQL Server

Ensure your MySQL server is running. The method depends on your installation:

**Windows:** MySQL should be running as a service
**macOS:** `mysql.server start`
**Linux:** `sudo systemctl start mysql` or `sudo service mysql start`

### 2. Run the Database Schema

Execute the SQL script to create the database and table:

```bash
mysql -u root -p < schema.sql
```

You'll be prompted for your MySQL root password. This will:
- Create a database named `chatbot_db`
- Create a `messages` table with appropriate columns and indexes

### 3. Configure Database Credentials

Open `config.py` and update the following values:

```python
MYSQL_USER = 'root'           # Change to your MySQL username
MYSQL_PASSWORD = 'yourpass'    # Set your MySQL password
MYSQL_HOST = 'localhost'       # Change if MySQL is on another server
MYSQL_PORT = 3306              # Change if using non-default port
```

**Important:** Keep your `config.py` file secure and do not commit it with passwords to version control.

## Configuration

### Flask Secret Key

For production deployments, change the `SECRET_KEY` in `config.py`:

```python
SECRET_KEY = 'your-secret-key-here-change-in-production'
```

Generate a secure random key with:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### MySQL Settings

If your MySQL server is on a different host or port, update `config.py`:

```python
MYSQL_HOST = '192.168.1.100'  # Remote server IP
MYSQL_PORT = 3307              # Custom port
```

## Running the Application

### 1. Activate Virtual Environment (if not already active)

**Windows:** `venv\Scripts\activate`
**macOS/Linux:** `source venv/bin/activate`

### 2. Run the Flask Application

```bash
python app.py
```

You should see output similar to:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### 3. Open in Browser

Navigate to: **http://localhost:5000**

### 4. Start Chatting!

Type a message in the input field and press Enter or click Send. The bot will respond instantly.

## Usage Instructions

### Basic Chat

- **Type a message** in the input field at the bottom
- **Press Enter** or **click Send** to send the message
- The bot will respond automatically based on pattern matching
- Messages appear in the chat area with user messages on the right (gray) and bot messages on the left (light gray)

### Chat History

- Your last 20 messages are automatically loaded when you open the page
- Chat history persists across page refreshes
- Each browser session maintains its own separate conversation
- Clear your browser cookies to start a completely new session

### Sample Conversations

Try these messages to see the bot in action:

- "Hello" → Greeting response
- "What can you do?" → Capability information
- "Thanks" → Acknowledgment
- "Who are you?" → Bot introduction
- "Goodbye" → Farewell message

## Customizing the Chatbot

### Adding New Response Patterns

The chatbot's personality and responses are easily customizable. Open `chatbot_logic.py` and edit the `PATTERNS` dictionary.

#### Pattern Structure

Each pattern has:
- **keywords:** List of words/phrases that trigger this pattern
- **responses:** List of possible responses (randomly selected)

#### Example: Adding Weather Pattern

```python
'weather': {
    'keywords': ['weather', 'temperature', 'forecast', 'rain', 'sunny'],
    'responses': [
        'I can\'t check the weather, but I hope it\'s nice outside!',
        'I don\'t have access to weather data, sorry!',
        'Try checking a weather website for accurate forecasts!'
    ]
}
```

#### Steps to Add a Pattern

1. Open `chatbot_logic.py`
2. Add your new pattern to the `PATTERNS` dictionary
3. Save the file
4. Restart the Flask application (`python app.py`)
5. Test your new pattern in the chat interface

### Changing the UI Colors

Edit `static/css/style.css` to customize the color scheme:

```css
/* Main colors to customize */
body {
    background-color: #f5f5f5;  /* Page background */
}

.chat-container {
    background-color: #ffffff;   /* Chat container */
    border: 2px solid #999999;   /* Container border */
}

.chat-header {
    background-color: #e0e0e0;   /* Header background */
}

.message.user .message-bubble {
    background-color: #e0e0e0;   /* User message bubble */
}

.message.bot .message-bubble {
    background-color: #f5f5f5;   /* Bot message bubble */
}
```

## Project Structure

```
gov-schemes-frontend/
│
├── app.py                      # Main Flask application with routes
├── chatbot_logic.py            # Chatbot pattern matching and response logic
├── database.py                 # Database connection and operations
├── config.py                   # Configuration (Flask secret, MySQL credentials)
├── requirements.txt            # Python dependencies
├── schema.sql                  # SQL script to create database and table
├── README.md                   # This file - setup and usage instructions
│
├── templates/
│   └── index.html              # Main chat interface HTML
│
└── static/
    ├── css/
    │   └── style.css           # Chat interface styling
    └── js/
        └── chat.js             # Frontend JavaScript for chat functionality
```

### File Descriptions

- **app.py:** Contains all Flask routes (/, /chat, /history, /clear-history) and session management
- **chatbot_logic.py:** Pattern matching algorithm and response generation
- **database.py:** MySQL connection handling and CRUD operations for messages
- **config.py:** Configuration values for Flask and MySQL (keep secure!)
- **templates/index.html:** HTML structure for the chat interface
- **static/css/style.css:** All styling for the chat UI
- **static/js/chat.js:** Frontend JavaScript for sending/receiving messages and UI updates
- **schema.sql:** Database initialization script

## Troubleshooting

### MySQL Connection Errors

**Problem:** `Error connecting to MySQL database: Access denied for user...`

**Solution:**
- Check that `MYSQL_USER` and `MYSQL_PASSWORD` in `config.py` are correct
- Ensure MySQL server is running
- Verify the user has permissions to access `chatbot_db`

**Problem:** `Error connecting to MySQL database: Unknown database 'chatbot_db'`

**Solution:**
- Run the schema.sql script: `mysql -u root -p < schema.sql`
- Or manually create the database: `CREATE DATABASE chatbot_db;`

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
- Ensure your virtual environment is activated
- Run `pip install -r requirements.txt`
- Verify installation: `pip list | grep Flask`

### Port Already in Use

**Problem:** `OSError: [Errno 48] Address already in use`

**Solution:**
- Another process is using port 5000
- Change the port in `app.py`: `app.run(debug=True, host='0.0.0.0', port=5001)`
- Or kill the process using port 5000

**On macOS/Linux:**
```bash
lsof -ti:5000 | xargs kill
```

**On Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Messages Not Saving to Database

**Problem:** Messages display but don't persist after refresh

**Solution:**
- Check MySQL connection in `config.py`
- Verify `messages` table exists: `mysql -u root -p -e "USE chatbot_db; SHOW TABLES;"`
- Check Flask console for error messages
- Ensure database user has INSERT/SELECT permissions

### Session Issues

**Problem:** Chat history loads from previous user or doesn't load at all

**Solution:**
- Clear browser cookies for localhost
- Verify `SECRET_KEY` is set in `config.py`
- Check browser console for JavaScript errors

## Future Enhancements

This chatbot is designed to be modular and extensible. Here are some ideas for future improvements:

### Authentication System
- Add user registration and login
- Associate chat history with user accounts
- Implement Flask-Login for session management

### AI-Powered Responses
- Integrate OpenAI GPT API for intelligent responses
- Use natural language processing (NLP) libraries
- Implement intent recognition instead of keyword matching

### Advanced Features
- File upload support (images, documents)
- Export chat history to PDF or text file
- Real-time updates using WebSockets (Socket.IO)
- Multi-language support
- Voice input/output
- Typing indicators
- Read receipts

### UI Improvements
- Dark mode toggle
- Custom themes
- Emoji picker
- Message editing and deletion
- Search chat history
- User avatars

### Admin Panel
- View all conversations
- Analytics dashboard (message counts, popular queries)
- Manage chatbot patterns without editing code
- User management

## Security Considerations

- **Secret Key:** Always change `SECRET_KEY` in production
- **Database Credentials:** Never commit `config.py` with real passwords to version control
- **SQL Injection:** Parameterized queries are used throughout to prevent SQL injection
- **Input Validation:** User inputs are validated before processing
- **HTTPS:** Use HTTPS in production (not implemented in this basic version)
- **Rate Limiting:** Consider adding rate limiting for production (Flask-Limiter)

## License

This project is open source and available for educational and commercial use.

## Support

If you encounter issues or have questions:

1. Check the Troubleshooting section above
2. Review the code comments in each file
3. Ensure all prerequisites are installed correctly
4. Verify MySQL is running and credentials are correct

## Credits

Built with:
- Flask 3.0.0
- MySQL
- Vanilla JavaScript (no frameworks)
- Modern CSS (Flexbox layout)

Enjoy your Flask chatbot! Feel free to extend and customize it for your needs.
