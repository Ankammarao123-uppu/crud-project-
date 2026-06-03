from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import json
import os

basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
FILE_NAME = os.path.join(basedir, "data.json")

# Create instance folder if it doesn't exist
os.makedirs(instance_path, exist_ok=True)

app = Flask(__name__, instance_path=instance_path)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_path, 'students.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Student Table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)


def seed_data_from_json():
    if not os.path.exists(FILE_NAME):
        return

    if Student.query.first() is not None:
        return

    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as file:
            students = json.load(file)
    except (json.JSONDecodeError, OSError):
        return

    for item in students:
        try:
            student = Student(
                name=item.get('name', '').strip(),
                age=int(item.get('age', 0))
            )
        except (TypeError, ValueError):
            continue

        db.session.add(student)

    db.session.commit()


# Create Database and seed initial data
with app.app_context():
    db.create_all()
    seed_data_from_json()


# Home Page
@app.route("/")
def home():
    students = Student.query.all()
    return render_template("index.html", students=students)


# Add Student
@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name")
    age = request.form.get("age")

    student = Student(
        name=name,
        age=int(age)
    )

    db.session.add(student)
    db.session.commit()

    return redirect("/")


# Edit Student
@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    student = Student.query.get_or_404(id)

    student.name = request.form.get("name")
    student.age = int(request.form.get("age"))

    db.session.commit()

    return redirect("/")


# Delete Student
@app.route("/delete/<int:id>")
def delete(id):
    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    return redirect("/")


# Temporary Route to Test Database
@app.route("/testdb")
def testdb():
    students = Student.query.all()

    result = ""

    for s in students:
        result += f"ID: {s.id}, Name: {s.name}, Age: {s.age}<br>"

    return result if result else "Database is empty"


if __name__ == "__main__":
    app.run(debug=True)