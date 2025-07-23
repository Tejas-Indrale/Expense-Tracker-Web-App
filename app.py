from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Load API key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # ✅ NEW client instance

# Store expenses in memory
DATA_FILE = 'data.json'

def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

def save_expenses(expenses):
    with open(DATA_FILE, 'w') as file:
        json.dump(expenses, file)

expenses = load_expenses()

@app.route('/')
def home():
    category = request.args.get('category')
    if category:
        filtered_expenses = [exp for exp in expenses if exp['category'].lower() == category.lower()]
        total = sum(exp['amount'] for exp in filtered_expenses)
        return render_template('index.html', expenses=filtered_expenses, total=total)
    else:
        total = sum(exp['amount'] for exp in expenses)
        return render_template('index.html', expenses=expenses, total=total)

@app.route('/add', methods=['POST'])
def add_expense():
    amount = float(request.form['amount'])
    category = request.form['category']
    new_expense = {'amount': amount, 'category': category}
    expenses.append(new_expense)
    save_expenses(expenses)
    return redirect('/')

@app.route('/filter', methods=['POST'])
def filter_expenses():
    selected_category = request.form['category']
    filtered = [exp for exp in expenses if exp['category'].lower() == selected_category.lower()]
    total = sum(exp['amount'] for exp in filtered)
    return render_template('index.html', expenses=filtered, total=total, filter_mode=True, category=selected_category)

@app.route('/insights')
def insights():
    suggestion = "AI insights are currently unavailable due to API limit. Please try again later or check your OpenAI account."
    return render_template('insights.html', suggestion=suggestion)

# ✅ Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
