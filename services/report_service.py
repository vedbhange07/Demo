import pandas as pd
from database.db import get_connection


def generate_report():

    conn = get_connection()

    query = "SELECT * FROM attendance"
    df = pd.read_sql(query, conn)

    df.to_csv("attendance_report.csv", index=False)

    conn.close()

    print("Attendance Report Generated Successfully")