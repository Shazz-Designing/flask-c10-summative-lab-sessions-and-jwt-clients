from flask import Flask, request, session, jsonify
from config import db, migrate, bcrypt
from models import User, Expense

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super-secret-key'


# extensions
db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)


def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return User.query.get(user_id)


@app.route('/')
def home():
    return jsonify(message="Expense Tracker API is running")


# ---------------- SIGNUP ----------------
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}

    username = data.get('username')
    password = data.get('password')

    # validate input
    if not username or not password:
        return jsonify(error="Username and password required"), 400

    # check if user exists
    if User.query.filter_by(username=username).first():
        return jsonify(error="Username already exists"), 400

    # create user
    new_user = User(username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    # log them in immediately
    session['user_id'] = new_user.id

    return jsonify(message="User created successfully"), 201


# ---------------- LOGIN ----------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}

    username = data.get('username')
    password = data.get('password')

    # validate input
    if not username or not password:
        return jsonify(error="Username and password required"), 400

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        session['user_id'] = user.id
        return jsonify(message="Login successful"), 200

    return jsonify(error="Invalid credentials"), 401


# ---------------- LOGOUT ----------------
@app.route('/logout', methods=['DELETE'])
def logout():
    session.pop('user_id', None)
    return jsonify(message="Logged out"), 200


# ---------------- CHECK SESSION ----------------
@app.route('/me', methods=['GET'])
def me():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify(error="Unauthorized"), 401

    user = User.query.get(user_id)

    if not user:
        return jsonify(error="User not found"), 404

    return jsonify(
        id=user.id,
        username=user.username
    ), 200



#EXPENSES#
@app.route('/expenses', methods=['POST'])
def create_expense():
    user = get_current_user()
    if not user:
        return jsonify(error="Unauthorized"), 401

    data = request.get_json() or {}

    amount = data.get('amount')
    category = data.get('category')

    if not amount or not category:
        return jsonify(error="Amount and category required"), 400

    new_expense = Expense(
        amount=amount,
        category=category,
        description=data.get('description'),
        date=data.get('date'),
        user_id=user.id
    )

    db.session.add(new_expense)
    db.session.commit()

    return jsonify(message="Expense created"), 201

#GET ALL#
@app.route('/expenses', methods=['GET'])
def get_expenses():
    user = get_current_user()
    if not user:
        return jsonify(error="Unauthorized"), 401

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))

    expenses = Expense.query.filter_by(user_id=user.id).paginate(page=page, per_page=per_page, error_out=False)

    results = []
    for exp in expenses.items:
        results.append({
            "id": exp.id,
            "amount": exp.amount,
            "category": exp.category,
            "description": exp.description,
            "date": exp.date
        })

    return jsonify(
        data=results,
        total=expenses.total,
        pages=expenses.pages,
        current_page=expenses.page
    ), 200


#GET ONE#
@app.route('/expenses/<int:id>', methods=['GET'])
def get_expense(id):
    user = get_current_user()
    if not user:
        return jsonify(error="Unauthorized"), 401

    expense = Expense.query.get(id)

    if not expense or expense.user_id != user.id:
        return jsonify(error="Expense not found"), 404

    return jsonify(
        id=expense.id,
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        date=expense.date
    ), 200

#UPDATE#
@app.route('/expenses/<int:id>', methods=['PATCH'])
def update_expense(id):
    user = get_current_user()
    if not user:
        return jsonify(error="Unauthorized"), 401

    expense = Expense.query.get(id)

    if not expense or expense.user_id != user.id:
        return jsonify(error="Expense not found"), 404

    data = request.get_json() or {}

    expense.amount = data.get('amount', expense.amount)
    expense.category = data.get('category', expense.category)
    expense.description = data.get('description', expense.description)
    expense.date = data.get('date', expense.date)

    db.session.commit()

    return jsonify(message="Expense updated"), 200

#DELETE#
@app.route('/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    user = get_current_user()
    if not user:
        return jsonify(error="Unauthorized"), 401

    expense = Expense.query.get(id)

    if not expense or expense.user_id != user.id:
        return jsonify(error="Expense not found"), 404

    db.session.delete(expense)
    db.session.commit()

    return jsonify(message="Expense deleted"), 200

if __name__ == '__main__':
    app.run(debug=True)
