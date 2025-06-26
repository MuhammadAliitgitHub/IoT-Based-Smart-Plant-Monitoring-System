from flask import Flask, render_template 
import mysql.connector 
app = Flask(__name__) 
DB_CONFIG = { 
    'host': 'localhost', 
    'user': 'root', 
    'password': '123456789', 
    'database': 'plant_data' 
} 
@app.route('/') 
def index(): 
    conn = mysql.connector.connect(**DB_CONFIG) 
    cursor = conn.cursor() 
    cursor.execute(""" 
        SELECT id, moisture, temp, humidity, timestamp, pump_state 
        FROM sensor_data ORDER BY id DESC LIMIT 10 
    """) 
    data = cursor.fetchall() 
    cursor.close() 
    conn.close() 
    return render_template('index.html', sensor_data=data) 
if __name__ == '__main__': 
    app.run(debug=True, host='0.0.0.0', port=5000) 