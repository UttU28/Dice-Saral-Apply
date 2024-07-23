import pypyodbc as odbc
from credential import username, password
from datetime import datetime, timezone

server = 'dice-sql.database.windows.net'
database = 'dice_sql_database'
connectionString = f'Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{server},1433;Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

def executeAllSQL(queryList):
    try:
        conn = odbc.connect(connectionString)
        cursor = conn.cursor()
        
        sql = '''
            INSERT INTO allData (id, title, location, company, description, datePosted, dateUpdated, myStatus, decisionTime) 
            VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', NULL);
        '''
        cursor.executemany(sql, queryList)

        timestamp = int(datetime.now(timezone.utc).timestamp())
        new_list = [(id_val, title_val, timestamp) for (id_val, title_val, *_) in queryList]
        sql = '''
            INSERT INTO myQueue (id, title, timeOfArrival) 
            VALUES (?, ?, ?);
        '''
        cursor.execute(sql, new_list)
        conn.commit()
        cursor.close()
        conn.close()
        return True
        # print(f"Data inserted successfully for {jobID}")
    except: return False

# Example usage
# executeAllSQL('1d2013e7-baa2-4f99-bd47-36de708e00f5', 'DevOps Databricks Engineer - Azure @ Remote', 'US', 'Aroha Technologies', 'Position:1min (Workspaces, Unity Catalog, Volumes, Ext volumes, etc.)', 1721504740, 1721504740)
