from flask import Flask, render_template, jsonify
import sqlite3
import export_pdf

app = Flask(__name__)

DB_PATH = "earthquakes.db"

def get_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, time, latitude, longitude, depth, magnitude, place FROM earthquakes")
    rows = cursor.fetchall()
    conn.close()
    
    # convert to list of dicts
    data = [
        {
            "id": row[0],
            "time": row[1],
            "latitude": row[2],
            "longitude": row[3],
            "depth": row[4],
            "magnitude": row[5],
            "place": row[6]
        }
        for row in rows
    ]
    return data

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/data')
def data():
    return jsonify(get_data())

# ✅ Add this route to trigger PDF export
@app.route('/export')
def export():
    export_pdf.generate_summary()
    return "PDF exported as 'earthquake_summary.pdf'. Check your project folder."


if __name__ == '__main__':
    app.run(debug=True)
