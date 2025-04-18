import sqlite3
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

DB_PATH = "earthquakes.db"

def generate_summary():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM earthquakes", conn)
    conn.close()

    df["date"] = pd.to_datetime(df["time"], unit="s").dt.date
    total = len(df)
    max_row = df.loc[df["magnitude"].idxmax()]
    top_day = df["date"].value_counts().idxmax()
    top_day_count = df["date"].value_counts().max()

    # PDF creation
    c = canvas.Canvas("earthquake_summary.pdf", pagesize=letter)
    c.setFont("Helvetica", 12)

    c.drawString(50, 750, "Earthquake Summary Report")
    c.drawString(50, 720, f"Total Earthquakes: {total}")
    c.drawString(50, 700, f"Strongest Earthquake: {max_row['magnitude']} at {max_row['place']}")
    c.drawString(50, 680, f"Most Active Day: {top_day} ({top_day_count} quakes)")

    c.save()
    print("PDF summary exported without wkhtmltopdf.")

if __name__ == '__main__':
    generate_summary()
