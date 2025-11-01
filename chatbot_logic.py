"""
Chatbot Logic Module

This module contains the rule-based pattern matching logic for the chatbot.
The bot responds based on keyword patterns found in user messages.

HOW TO ADD NEW PATTERNS:
1. Add a new pattern category to the PATTERNS dictionary below
2. Specify keywords that trigger this pattern
3. Provide one or more response variations
4. The bot will randomly select from available responses

Example:
    'weather': {
        'keywords': ['weather', 'temperature', 'forecast'],
        'responses': [
            'I can\'t check the weather, but I hope it\'s nice!',
            'I don\'t have weather info, sorry!'
        ]
    }
"""

import random


# Pattern dictionary: maps pattern categories to keywords and responses
PATTERNS = {
    'greetings': {
        'keywords': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening'],
        'responses': [
            'Hello! How can I help you today?',
            'Hi there! What can I do for you?',
            'Hey! How may I assist you?',
            'Greetings! What brings you here today?'
        ]
    },
    'farewell': {
        'keywords': ['bye', 'goodbye', 'see you', 'later', 'farewell', 'take care'],
        'responses': [
            'Goodbye! Have a great day!',
            'See you later!',
            'Take care!',
            'Farewell! Come back anytime!'
        ]
    },
    'help': {
        'keywords': ['help', 'what can you do', 'how do you work', 'assist', 'support'],
        'responses': [
            'I can chat with you! Try saying hello, asking for help, or just chatting.',
            'I\'m a simple chatbot. I can respond to greetings, farewells, and basic questions!',
            'I\'m here to chat! Ask me about what I can do, say hello, or just talk to me.'
        ]
    },
    'thanks': {
        'keywords': ['thank', 'thanks', 'appreciate', 'grateful'],
        'responses': [
            'You\'re welcome!',
            'Happy to help!',
            'My pleasure!',
            'Anytime!',
            'Glad I could help!'
        ]
    },
    'name': {
        'keywords': ['your name', 'who are you', 'what are you', 'introduce yourself'],
        'responses': [
            'I\'m a friendly chatbot built with Flask!',
            'I\'m a chatbot here to assist you!',
            'I\'m your virtual assistant, built to chat with you!'
        ]
    }
}

# Default response when no pattern matches
DEFAULT_RESPONSE = "I'm not sure I understand. Can you rephrase that, or type 'help' for guidance?"


def get_bot_response(message):
    """
    Generate a bot response based on pattern matching.

    This function analyzes the user's message and returns an appropriate response
    by checking for keyword patterns. If multiple patterns match, the first match
    is used. If no patterns match, a default response is returned.

    Parameters:
        message (str): The user's input message

    Returns:
        str: The bot's response message

    Algorithm:
        1. Convert message to lowercase for case-insensitive matching
        2. Loop through all pattern categories
        3. Check if any keyword from the pattern appears in the message
        4. If match found, randomly select and return a response from that pattern
        5. If no match found, return default response
    """
    # Convert message to lowercase for case-insensitive matching
    message_lower = message.lower()

    # Check each pattern category
    for pattern_name, pattern_data in PATTERNS.items():
        keywords = pattern_data['keywords']
        responses = pattern_data['responses']

        # Check if any keyword appears in the user's message
        for keyword in keywords:
            if keyword in message_lower:
                # Match found! Return a random response from this pattern
                return random.choice(responses)

    # No pattern matched, return default response
    return DEFAULT_RESPONSE
