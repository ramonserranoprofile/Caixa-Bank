from flask import Blueprint, jsonify, request
from app.utils.jwt_utils import verify_jwt
from app.models import RecurringExpense, db

recurring_expenses_bp = Blueprint("recurring_expenses", __name__)


@recurring_expenses_bp.route("/api/recurring-expenses", methods=["GET"])
@verify_jwt
def get_recurring_expenses():
    user_id = request.user_id
    expenses = RecurringExpense.query.filter_by(user_id=user_id).all()
    response = [
        {
            "id": e.id,
            "expense_name": e.expense_name,
            "amount": e.amount,
            "frequency": e.frequency,
            "start_date": str(e.start_date),
        }
        for e in expenses
    ]
    return jsonify(response), 200


@recurring_expenses_bp.route("/api/recurring-expenses/<int:expense_id>", methods=["PUT"])
@verify_jwt
def update_recurring_expense(expense_id):
    data = request.get_json()
    expense = RecurringExpense.query.get(expense_id)
    if not expense:
        return jsonify({"error": "Recurring expense not found"}), 404
    expense.expense_name = data.get("expense_name", expense.expense_name)
    expense.amount = data.get("amount", expense.amount)
    expense.frequency = data.get("frequency", expense.frequency)
    expense.start_date = data.get("start_date", expense.start_date)
    db.session.commit()
    return jsonify({"message": "Recurring expense updated successfully"}), 200


@recurring_expenses_bp.route("/api/recurring-expenses/<int:expense_id>", methods=["DELETE"])
@verify_jwt
def delete_recurring_expense(expense_id):
    expense = RecurringExpense.query.get(expense_id)
    if not expense:
        return jsonify({"error": "Recurring expense not found"}), 404
    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": "Recurring expense deleted successfully"}), 200


@recurring_expenses_bp.route("/api/recurring-expenses", methods=["POST"])
@verify_jwt
def post_recurring_expenses():
    data = request.get_json()
    user_id = request.user_id
    new_expense = RecurringExpense(
        user_id=user_id,
        expense_name=data["expense_name"],
        amount=data["amount"],
        frequency=data["frequency"],
        start_date=data["start_date"],
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({"message": "Recurring expense added successfully"}), 201