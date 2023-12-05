import pyodbc

def connection():
    s = '194.177.217.92' 
    d = 'NT_DB' 
    u = 'ethnikoTheatroUSR'
    p = 'ethilsp!23'
    cstr = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER='+s+';DATABASE='+d+';UID='+u+';PWD='+ p+';TrustServerCertificate=yes'
    conn = pyodbc.connect(cstr)
    return conn

def getUserHistory(user_id):
    history = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT count(userHistoryID), object_table, object_id FROM userHistory WHERE user_id=? GROUP BY object_id,object_table", user_id)
    for row in cursor.fetchall():
        history.append({"userHistoryID": row[0], "object_table": row[1], "object_id": row[2]})
    conn.close()
    return history

def getUserHistoryList():
    historyRatings = {'object_id':[], 'user_id': [], 'historyRating': []}
    conn = connection()
    cursor = conn.cursor()
    sqlStmt = '''
    SELECT object_id, user_id,
    (CASE WHEN count(object_id)>5 THEN 1 ELSE 0 END) as historyRating
    FROM userHistory 
    WHERE object_table='plays'
    GROUP BY object_id, user_id
    '''
    cursor.execute(sqlStmt)
    for row in cursor.fetchall():
        historyRatings['object_id'].append(row[0])
        historyRatings['user_id'].append(row[1])
        historyRatings['historyRating'].append(row[2])
        #historyRatings.append({"object_id": row[0], "user_id": row[1], "historyRating": row[2]})
    conn.close()
    return historyRatings


def getPlays():
    plays = []
    conn = connection()
    cursor = conn.cursor()
    sqlStmt = "SELECT playID FROM Plays WHERE playID NOT IN (SELECT object_id FROM userHistory)"
    cursor.execute(sqlStmt)
    for row in cursor.fetchall():
        plays.append(row[0])
    conn.close()
    return plays