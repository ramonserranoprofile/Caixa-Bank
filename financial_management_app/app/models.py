from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Date

# Instancia de SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    hashed_password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"

class RecurringExpense(db.Model):
    __tablename__ = 'recurring_expenses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    expense_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    frequency = db.Column(db.String(50), nullable=False)  # e.g., "monthly", "yearly"
    start_date = db.Column(db.Date, nullable=False)
    
    def __repr__(self):
        return f"<RecurringExpense {self.expense_name} for user {self.user_id}>"
