from flask import Blueprint, request, jsonify
from services import add_transaction, update_transaction, delete_transaction, add_category, update_category, delete_category
from models import Transaction, Category
from database import db

api = Blueprint('api', __name__)

# Transaction Endpoints
@api.route('/transactions', methods=['POST'])
def create_transaction():
    data = request.get_json()
    try:
        transaction = add_transaction(data)
        return jsonify({'message': 'Transaction added', 'transaction': {
            'id': transaction.id,
            'date': transaction.date.strftime('%Y-%m-%d'),
            'amount': transaction.amount,
            'description': transaction.description,
            'category_id': transaction.category_id
        }}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api.route('/transactions/<int:transaction_id>', methods=['PUT'])
def edit_transaction(transaction_id):
    data = request.get_json()
    try:
        transaction = update_transaction(transaction_id, data)
        return jsonify({'message': 'Transaction updated', 'transaction': {
            'id': transaction.id,
            'date': transaction.date.strftime('%Y-%m-%d'),
            'amount': transaction.amount,
            'description': transaction.description,
            'category_id': transaction.category_id
        }}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api.route('/transactions/<int:transaction_id>', methods=['DELETE'])
    
def remove_transaction(transaction_id):
    try:
        delete_transaction(transaction_id)
        return jsonify({'message': 'Transaction deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Category Endpoints
@api.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    try:
        category = add_category(data)
        return jsonify({'message': 'Category added', 'category': {
            'id': category.id,
            'name': category.name,
            'type': category.type
        }}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api.route('/categories/<int:category_id>', methods=['PUT'])

def edit_category(category_id):
    data = request.get_json()
    try:
        category = update_category(category_id, data)
        return jsonify({'message': 'Category updated', 'category': {
            'id': category.id,
            'name': category.name,
            'type': category.type
        }}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api.route('/categories/<int:category_id>', methods=['DELETE'])

def remove_category(category_id):
    reassign_id = request.args.get('reassign_category_id')
    try:
        if reassign_id:
            reassign_id = int(reassign_id)
        delete_category(category_id, reassign_category_id=reassign_id)
        return jsonify({'message': 'Category deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Additional endpoints to get list of transactions and categories
@api.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    result = []
    for t in transactions:
        result.append({
            'id': t.id,
            'date': t.date.strftime('%Y-%m-%d'),
            'amount': t.amount,
            'description': t.description,
            'category_id': t.category_id
        })
    return jsonify(result), 200

@api.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    result = []
    for c in categories:
        result.append({
            'id': c.id,
            'name': c.name,
            'type': c.type
        })
    return jsonify(result), 200
