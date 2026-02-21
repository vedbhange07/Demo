from flask import Flask, render_template, redirect, url_for
import subprocess
import mysql.connector
import pandas as pd

app = Flask(__name__)

# MySQL Connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vedant@2005",
        database="attendance_db"
    )

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Start Face Recognition
@app.route("/start")
def start_attendance():
    subprocess.Popen(["python", "recognize.py"])
    return redirect(url_for("home"))

# View Attendance
@app.route("/attendance")
def view_attendance():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM attendance", conn)
    conn.close()
    return render_template("attendance.html", tables=[df.to_html(classes='table table-bordered')])

# Generate CSV
@app.route("/report")
def generate_report():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM attendance", conn)
    df.to_csv("attendance_report.csv", index=False)
    conn.close()
    return "CSV Report Generated!"

if __name__ == "__main__":
    app.run(debug=True)