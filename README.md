# TalkTracker

## Overview
The **TalkTracker** is a Django-based web application that analyzes chat conversations. It provides insights into humor, tone, relationship dynamics, and shared understanding using OpenAI's GPT API.

## Features
- Reverse chat conversation for better readability
- Analyze tone, humor, and relationship dynamics
- Extract self-reflection moments from conversations
- Simple UI for inputting and processing chat text
- Stores chat analysis results in a database

## Technologies Used
- Django (Python framework)
- OpenAI GPT API for chat analysis
- SQLite for database storage
- HTML, CSS for frontend
- Bootstrap for styling

## Installation
1) **Clone the repository:**  
   git clone https://github.com/zuuhaaib/TalkTracker.git
   cd TalkTracker
2) **Create and activate a virtual environment:** python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
3) **Run migrations:** python manage.py migrate
4) **Add your OpenAI API key in .env file:** OPENAI_API_KEY=your_openai_api_key
5) **Start the development server:** python manage.py runserver
6) **Open a browser and go to:** http://127.0.0.1:8000/
