from app import app
from config import db
from models import User, Expense

with app.app_context():
    print("Seeding database...")

    # clear existing data (users first, then expenses)
    User.query.delete()
    Expense.query.delete()

    # create users
    user1 = User(username="Sharon")
    user1.set_password("1234")

    user2 = User(username="Ochieng")
    user2.set_password("1234")

    db.session.add_all([user1, user2])
    db.session.commit()

    # create expenses
    expenses = [
        Expense(
            amount=500,
            category="Food",
            description="Lunch",
            date="2026-04-22",
            user_id=user1.id
        ),
        Expense(
            amount=1500,
            category="Transport",
            description="Uber",
            date="2026-04-22",
            user_id=user1.id
        ),
        Expense(
            amount=2000,
            category="Utilities",
            description="KPLC token",
            date="2026-04-22",
            user_id=user2.id
        )
    ]

    db.session.add_all(expenses)
    db.session.commit()

    print("Done seeding!")