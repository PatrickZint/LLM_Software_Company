import io
import base64
from flask import Blueprint, jsonify, send_file, request
import matplotlib.pyplot as plt
import pandas as pd
from models import Transaction, Category
from database import db

viz = Blueprint('viz', __name__)

# Helper to generate chart from DataFrame
 def generate_bar_chart(df, title):
    plt.figure(figsize=(10,6))
    df.plot(kind='bar', legend=True)
    plt.title(title)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    return image_base64

@viz.route('/reports/monthly', methods=['GET'])
 def monthly_report():
    # Aggregate transactions by month
    transactions = Transaction.query.all()
    data = []
    for t in transactions:
        data.append({
            'date': t.date,
            'amount': t.amount
        })
    if not data:
        return jsonify({'error': 'No transactions found'}), 404

    df = pd.DataFrame(data)
    df['month'] = df['date'].dt.to_period('M')
    summary = df.groupby('month')['amount'].sum()
    # Generate bar chart
    chart = generate_bar_chart(summary, 'Monthly Transaction Summary')
    return jsonify({'chart': chart, 'summary': summary.to_dict()}), 200

@viz.route('/reports/yearly', methods=['GET'])
 def yearly_report():
    # Aggregate transactions by year
    transactions = Transaction.query.all()
    data = []
    for t in transactions:
        data.append({
            'date': t.date,
            'amount': t.amount
        })
    if not data:
        return jsonify({'error': 'No transactions found'}), 404

    df = pd.DataFrame(data)
    df['year'] = df['date'].dt.year
    summary = df.groupby('year')['amount'].sum()
    chart = generate_bar_chart(summary, 'Yearly Transaction Summary')
    return jsonify({'chart': chart, 'summary': summary.to_dict()}), 200

@viz.route('/charts/pie', methods=['GET'])
 def pie_chart_expenses():
    # Generate a pie chart based on expenses per category
    transactions = Transaction.query.join(Category).filter(Category.type=='Expense').all()
    if not transactions:
        return jsonify({'error': 'No expense transactions found'}), 404

    data = {}
    for t in transactions:
        cat = t.category.name
        data[cat] = data.get(cat, 0) + t.amount
    if not data:
        return jsonify({'error': 'No data for pie chart'}), 404

    labels = list(data.keys())
    sizes = list(data.values())
    plt.figure(figsize=(8,8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Expenses Distribution by Category')
    plt.axis('equal')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    return jsonify({'chart': image_base64}), 200
