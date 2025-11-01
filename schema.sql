-- Flask Chatbot Database Schema
-- This script creates the database and table needed for the chatbot application

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS chatbot_db;

-- Use the chatbot database
USE chatbot_db;

-- Create messages table to store all chat messages
-- This table stores both user and bot messages with timestamps
CREATE TABLE IF NOT EXISTS messages (
    -- Unique identifier for each message
    id INT AUTO_INCREMENT PRIMARY KEY,

    -- Session identifier to group messages by user session
    session_id VARCHAR(100) NOT NULL,

    -- Who sent the message: 'user' or 'bot'
    sender VARCHAR(10) NOT NULL,

    -- The actual message content
    message TEXT NOT NULL,

    -- When the message was sent (automatically set to current time)
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- Index on session_id for fast retrieval of conversation history
    INDEX idx_session_id (session_id)
);
