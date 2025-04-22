# LangChain CLI Chat Tool

A command line interface for interacting with AI models (DeepSeek) using LangChain, with conversation history management.

## Features

- Interactive chat with conversation history
- Multiple session management
- SQLite database storage for chat history
- Simple configuration setup

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install langchain langchain-deepseek click
```

## Configuration

Before first use, you need to configure your API key:

```bash
python main.py init
```

Follow the prompts to enter:
- Model type (deepseek)
- Model name (deepseek-chat)
- Your API key
- Environment file path (.env)

## Usage

### One-time question (no history)
```bash
python main.py oask "Your question here"
```

### Interactive chat with history
```bash
python main.py ask
```
- Will show existing sessions
- Prompt to choose/create a session
- Type 'exit' or 'quit' to end conversation

### Manage chat history
List all sessions:
```bash
python main.py history -s
```

Delete a session:
```bash
python main.py history -d SESSION_ID
```

## Session Management

- Each chat session is identified by a unique session ID
- Conversation history is stored in SQLite database (chat_histories.db)
- You can have multiple independent conversations by using different session IDs

## Requirements

- Python 3.7+
- LangChain
- DeepSeek API key
- Click

## Project Structure

- `main.py`: CLI interface
- `ask_model.py`: Core AI interaction logic
- `database_history.py`: SQLite storage implementation
- `history_manager.py`: Session management
- `load_model.py`: Model configuration loader
- `format_output.py`: Display formatting utilities
