import json
import pypyodbc as odbc
import logging
from config import DATABASE_CONFIG

def connect_to_database():
    connection_string = (
        f"Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{DATABASE_CONFIG['server']},1433;"
        f"Database={DATABASE_CONFIG['database']};Uid={DATABASE_CONFIG['username']};Pwd={DATABASE_CONFIG['password']};"
        f"Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    )
    
    try:
        conn = odbc.connect(connection_string)
        return conn
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")
        return None

def fetch_and_save_data():
    conn = connect_to_database()
    if conn is None:
        return
    
    tables = ['users', 'allData', 'resumeList', 'applyQueue', 'scoreBoard']
    data = {}
    
    for table in tables:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        data[table] = [dict(zip(columns, row)) for row in rows]
    
    with open('backup_data.json', 'w') as file:
        json.dump(data, file, indent=4)
    
    conn.close()



def reupload_data():
    with open('backup_data.json', 'r') as file:
        data = json.load(file)
    
    conn = connect_to_database()
    if conn is None:
        return
    
    tables = ['users', 'allData', 'resumeList', 'applyQueue', 'scoreBoard']
    
    cursor = conn.cursor()
    
    for table in tables:
        rows = data[table]
        
        for row in rows:
            columns = ', '.join(row.keys())
            placeholders = ', '.join(['?' for _ in row])
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            values = tuple(row.values())
            cursor.execute(sql, values)
            logging.info(f"Inserted row into {table}: {row}")
        
    conn.commit()
    conn.close()

# fetch_and_save_data()
reupload_data()
