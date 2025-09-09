from models import Transaction, Category
from database import db
from datetime import datetime

# Transaction Services

def add_transaction(data):
    try:
        # Data should contain: date, amount, description, category_id
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        amount = float(data.get('amount'))
        description = data.get('description')
        category_id = int(data.get('category_id'))

        transaction = Transaction(date=date, amount=amount, description=description, category_id=category_id)
        db.session.add(transaction)
        db.session.commit()
        return transaction
    except Exception as e:
        db.session.rollback()
        raise e


def update_transaction(transaction_id, data):
    try:
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            raise ValueError('Transaction not found')

        if 'date' in data:
            transaction.date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        if 'amount' in data:
            transaction.amount = float(data.get('amount'))
        if 'description' in data:
            transaction.description = data.get('description')
        if 'category_id' in data:
            transaction.category_id = int(data.get('category_id'))

        db.session.commit()
        return transaction
    except Exception as e:
        db.session.rollback()
        raise e


def delete_transaction(transaction_id):
    try:
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            raise ValueError('Transaction not found')
        db.session.delete(transaction)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise e

# Category Services

def add_category(data):
    try:
        name = data.get('name')
        type_ = data.get('type')  # Should be 'Income' or 'Expense'
        category = Category(name=name, type=type_)
        db.session.add(category)
        db.session.commit()
        return category
    except Exception as e:
        db.session.rollback()
        raise e


def update_category(category_id, data):
    try:
        category = Category.query.get(category_id)
        if not category:
            raise ValueError('Category not found')
        if 'name' in data:
            category.name = data.get('name')
        if 'type' in data:
            category.type = data.get('type')
        db.session.commit()
        return category
    except Exception as e:
        db.session.rollback()
        raise e


def delete_category(category_id, reassign_category_id=None):
    try:
        category = Category.query.get(category_id)
        if not category:
            raise ValueError('Category not found')
        
        # Reassign transactions if provided
        if reassign_category_id:
            transactions = category.transactions
            for transaction in transactions:
                transaction.category_id = reassign_category_id
        else:
            # Alternatively, archive or delete associated transactions
            for transaction in category.transactions:
                db.session.delete(transaction)

        db.session.delete(category)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise e
