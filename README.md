Emotion Store - README

Overview

Welcome to the Emotion Store! This is a unique project where the products are emotions, and users can browse, add to cart, and purchase different feelings. Built with Python, FastAPI for the backend, and Streamlit for the UI, this project brings a creative twist to the concept of online stores.

Features

🛍️ Browse a catalog of emotions

🧠 Add emotions to your cart

❤️ Purchase and manage emotional states

🔐 User authentication and session management

Installation

Clone the repository:

git clone https://github.com/yourusername/emotion-store.git
cd emotion-store

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

docker-compose up -d --build


Running the Project

Start the FastAPI backend:

uvicorn main:app --reload

Run the Streamlit UI:

streamlit run main_app.py

Environment Variables

Create a .env file for environment variables:

OPENAI_API_KEY=your_secret_key

API Documentation

After starting the backend, access the API docs:

http://localhost:8000/docs
