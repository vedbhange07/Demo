from flask import Flask, render_template, redirect, url_for, request, session
from flask import request, render_template, redirect, url_for, session

from database.db import get_connection
from services.dataset_service import collect_dataset
from services.train_service import train_model
from services.recognize_service import recognize_face
from services.report_service import generate_report
from services.dataset_service import collect_dataset
import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

#home 
@app.route("/")
def home():
    return render_template("index.html")
# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return "Invalid Credentials"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        dept = request.form["department"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO students (name, department) VALUES (%s,%s)",
            (name, dept)
        )
        conn.commit()

        student_id = cursor.lastrowid
        conn.close()

        collect_dataset(student_id, name)

        return redirect(url_for("students"))

    return render_template("register.html")

# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():
    conn = get_connection()
    cursor = conn.cursor()

    # Total students
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    # Today present
    cursor.execute("SELECT COUNT(DISTINCT student_id) FROM attendance WHERE DATE(date) = CURDATE()")
    today_present = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        today_present=today_present
    )

# ---------------- REGISTER STUDENT ----------------

# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         name = request.form["name"]
#         dept = request.form["department"]

#         conn = get_connection()
#         cursor = conn.cursor()

#         cursor.execute(
#             "INSERT INTO students (name, department) VALUES (%s,%s)",
#             (name, dept)
#         )
#         conn.commit()

#         student_id = cursor.lastrowid  # 🔥 VERY IMPORTANT

#         conn.close()

#         collect_dataset(student_id, name)  # ✅ FIXED

#         return redirect(url_for("dashboard"))

#     return render_template("register.html")

# ---------------- TRAIN ----------------

@app.route("/train")
def train():
    train_model()
    return "Model trained successfully!"
# ---------------- ATTENDANCE ----------------

@app.route("/attendance")
def attendance():
    recognize_face()
    return redirect(url_for("dashboard"))


# ---------------- REPORT ----------------
@app.route("/reports")
def reports():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT student_id, date, time FROM attendance")
    data = cursor.fetchall()

    conn.close()

    return render_template("reports.html", reports=data)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/students")
def students():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    conn.close()

    return render_template("students.html", students=data)

@app.route("/smart_attendance")
def smart_attendance():
    return render_template("attendance.html")


# @app.route("/reports")
# def reports():
#     return render_template("reports.html")


if __name__ == "__main__":
    app.run(debug=True)