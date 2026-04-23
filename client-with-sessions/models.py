from config import db, bcrypt

# ---------------- USER MODEL ----------------
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

    # relationship
    expenses = db.relationship('Expense', backref='user', cascade='all, delete-orphan')

    # password setter
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # password checker
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


# ---------------- EXPENSE MODEL ----------------
class Expense(db.Model):
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    date = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))