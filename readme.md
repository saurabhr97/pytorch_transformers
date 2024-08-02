# Chat Interface for LLM Models

## Description

This repository provides a chat interface for interacting with different LLM (Language Model) models. It includes a function calling chat template and a basic RAG system using JSON file-based storage.

## Features

- Chat Interface: Provides a user-friendly interface for interacting with different LLM models.
- Function Calling Chat Template: Allows users to call functions and retrieve results directly from the chat interface.
- Basic RAG System: Implements a simple RAG system using JSON file-based storage for managing requests and generating responses.

## Installation

1. Clone the repository
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`

## Usage

1. Start the application by running `python main.py` in the project directory.
2. Start chatting with the chat interface and interacting with the different LLM models.
3. If using the RAG chat:
3.1. Prompts starting with "store:" will result in fetching information from Wikipedia
3.2. Prompts starting with "norag:" will ignore the store values and simply query the LLM directly
4. The underlying LLM model used can be changed by modifying/uncommenting lines in main.py