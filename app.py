from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

FILE_NAME = "data.json"

def load_data():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r") as file:
        try:
            return json.load(file)
        except:
            return []

def save_data(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)

@app.route("/")
def home():
    students = load_data()
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add():
    students = load_data()

    name = request.form.get("name")
    age = request.form.get("age")

    students.append({
        "id": len(students) + 1,
        "name": name,
        "age": age
    })

    save_data(students)

    return redirect("/")

@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    students = load_data()

    for student in students:
        if student["id"] == id:
            student["name"] = request.form["name"]
            student["age"] = request.form["age"]

    save_data(students)
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    students = load_data()

    students = [s for s in students if s["id"] != id]

    for i, student in enumerate(students):
        student["id"] = i + 1

    save_data(students)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)