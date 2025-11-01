"""
Flask Chatbot Application - Main Entry Point

This is the main Flask application that serves the chatbot web interface.

Routes:
- GET /          : Serve the main chat interface (index.html)
- POST /chat     : Handle user messages and return bot responses
- GET /history   : Retrieve chat history for the current session
- POST /clear-history : Clear chat history for the current session

The app uses Flask sessions to maintain unique session IDs for each user.
All chat messages are stored in MySQL database for history persistence.
"""

from flask import Flask, render_template, request, jsonify, session
import uuid
import config
from database import save_message, get_session_history, clear_session_history
from chatbot_logic import get_bot_response

# Initialize Flask application
app = Flask(__name__)

# Load configuration from config.py
app.config.from_object('config')


@app.route('/')
def index():
    """
    Serve the main chat interface.

    This route renders the index.html template and manages session IDs.
    If the user doesn't have a session_id, a new UUID is generated and stored.

    Returns:
        Rendered HTML template with session_id passed to frontend
    """
    # Check if session_id exists, if not create a new one
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())

    # Pass session_id to template for JavaScript to use
    return render_template('index.html', session_id=session['session_id'])


@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle incoming user messages and return bot responses.

    This route:
    1. Receives user message from frontend (JSON)
    2. Saves user message to database
    3. Generates bot response using chatbot_logic
    4. Saves bot response to database
    5. Returns bot response to frontend (JSON)

    Request Body (JSON):
        {
            "message": "user's message text"
        }

    Response (JSON):
        {
            "response": "bot's response text",
            "status": "success"
        }

    Error Response (JSON):
        {
            "error": "error message"
        }

    Returns:
        JSON response with bot's reply or error message
    """
    try:
        # Get message from request
        data = request.get_json()
        user_message = data.get('message', '').strip()

        # Validate that message is not empty
        if not user_message:
            return jsonify({'error': 'Message required'}), 400

        # Get session_id from Flask session
        session_id = session.get('session_id')
        if not session_id:
            # If no session_id exists (shouldn't happen), create one
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id

        # Save user message to database
        # Note: We don't stop execution if this fails (for better UX)
        save_message(session_id, 'user', user_message)

        # Generate bot response using chatbot logic
        bot_response = get_bot_response(user_message)

        # Save bot response to database
        save_message(session_id, 'bot', bot_response)

        # Return bot response to frontend
        return jsonify({
            'response': bot_response,
            'status': 'success'
        })

    except Exception as e:
        # Log error but don't expose details to user
        print(f"Error in /chat route: {e}")
        return jsonify({'error': 'An error occurred'}), 500


@app.route('/history', methods=['GET'])
def history():
    """
    Retrieve chat history for the current session.

    This route fetches the last 20 messages for the current session from
    the database and returns them in chronological order (oldest first).

    Returns:
        JSON array of message objects
        Each object contains: sender, message, timestamp

    Response (JSON):
        {
            "messages": [
                {
                    "sender": "user",
                    "message": "Hello",
                    "timestamp": "2025-01-15 10:30:45"
                },
                {
                    "sender": "bot",
                    "message": "Hi there!",
                    "timestamp": "2025-01-15 10:30:46"
                }
            ]
        }
    """
    try:
        # Get session_id from Flask session
        session_id = session.get('session_id')
        if not session_id:
            # No session yet, return empty history
            return jsonify({'messages': []})

        # Retrieve last 20 messages from database
        messages = get_session_history(session_id, limit=20)

        # Return messages in JSON format
        return jsonify({'messages': messages})

    except Exception as e:
        # Log error and return empty history
        print(f"Error in /history route: {e}")
        return jsonify({'messages': []})


@app.route('/clear-history', methods=['POST'])
def clear_history():
    """
    Clear all chat history for the current session.

    This route deletes all messages associated with the current session
    from the database. This is useful when users want to start fresh.

    Returns:
        JSON response indicating success or failure

    Response (JSON):
        {
            "status": "success",
            "message": "Chat history cleared"
        }

    Error Response (JSON):
        {
            "status": "error",
            "message": "Failed to clear history"
        }
    """
    try:
        # Get session_id from Flask session
        session_id = session.get('session_id')
        if not session_id:
            return jsonify({
                'status': 'error',
                'message': 'No session found'
            }), 400

        # Clear history from database
        success = clear_session_history(session_id)

        if success:
            return jsonify({
                'status': 'success',
                'message': 'Chat history cleared'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to clear history'
            }), 500

    except Exception as e:
        # Log error and return error response
        print(f"Error in /clear-history route: {e}")
        return jsonify({
            'status': 'error',
            'message': 'An error occurred'
        }), 500


# Run the Flask application
if __name__ == '__main__':
    # Debug mode enabled for development
    # host='0.0.0.0' allows external connections
    # port=5000 is the default Flask port
    app.run(debug=True, host='0.0.0.0', port=5000)
