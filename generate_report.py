from sqlalchemy import create_engine
import pandas as pd

DB_USER = "root"
DB_PASSWORD = "your_password"   # CHANGE THIS
DB_NAME = "attendance_db"

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}"
)

query = "SELECT * FROM attendance"
df = pd.read_sql(query, engine)

df.to_csv("attendance_report.csv", index=False)

print("Report Generated Successfully!")