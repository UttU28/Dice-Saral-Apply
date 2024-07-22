import pypyodbc as odbc
from credential import username, password
from datetime import datetime, timezone

server = 'dice-sql.database.windows.net'
database = 'dice_sql_database'
connectionString = f'Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{server},1433;Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

def getMyQueue():
    try:
        conn = odbc.connect(connectionString)
        cursor = conn.cursor()
        
        timestamp = int(datetime.now(timezone.utc).timestamp())
        sql = '''
            SELECT * FROM myQueue ORDER BY time;
        '''
        cursor.execute(sql)
        
        conn.commit()
        # print(f"Data inserted successfully for {jobID}")
    except odbc.Error as e:
        print("Error occurred while inserting data: ", e)
    finally:
        cursor.close()
        conn.close()

# Example usage
# addNewJobSQL('1d2013e7-baa2-4f99-bd47-36de708e00f5', 'DevOps Databricks Engineer - Azure @ Remote', 'US', 'Aroha Technologies', 'Position:1min (Workspaces, Unity Catalog, Volumes, Ext volumes, etc.)', 1721504740, 1721504740)
