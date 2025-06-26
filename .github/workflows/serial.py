import serial 
import time 
import mysql.connector 
DB_HOST = "localhost" 
DB_USER = "root" 
DB_PASSWORD = "123456789" 
DB_NAME = "plant_db" 
SERIAL_PORT = '/dev/ttyACM0' 
BAUD_RATE = 9600 
try: 
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) 
    print("Serial port connected.") 
except: 
    print("Connection failed.") 
    exit() 
def log_sensor_data(moisture, temp, humidity, pump_state): 
    try: 
        conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, 
password=DB_PASSWORD, database=DB_NAME) 
        cursor = conn.cursor() 
        query = "INSERT INTO sensor_data (moisture, temp, humidity, pump_state) VALUES 
(%s, %s, %s, %s)" 
        cursor.execute(query, (moisture, temp, humidity, pump_state)) 
        conn.commit() 
        print(f"Logged: {moisture}, {temp}, {humidity}, {pump_state}") 
    finally: 
        if conn.is_connected(): 
            cursor.close() 
            conn.close() 
while True: 
    if ser.in_waiting > 0: 
        line = ser.readline().decode().strip() 
        print("Received:", line) 
        parts = {} 
        for item in line.split(','): 
            if ':' in item: 
                key, val = item.split(':') 
                parts[key.strip().upper()] = float(val.strip()) 
        moisture = parts.get("MOISTURE") 
        temp = parts.get("TEMP") 
        humidity = parts.get("HUMIDITY") 
        pump_state = parts.get("PUMP_STATE") 
        if all(v is not None for v in [moisture, temp, humidity, pump_state]): 
            log_sensor_data(moisture, temp, humidity, int(pump_state)) 
    time.sleep(1)