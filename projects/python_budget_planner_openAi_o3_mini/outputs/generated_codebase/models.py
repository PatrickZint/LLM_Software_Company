from database import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'Income' or 'Expense'
    transactions = db.relationship('Transaction', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.name}: {self.type}>"


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    def __repr__(self):
        return f"<Transaction {self.id}: {self.amount} on {self.date}>"
