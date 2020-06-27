import mysql.connector


def select(table, level, subject, roll):
    global cursor

    query = "SELECT * FROM result WHERE level = %s AND subject = %s AND roll = %s"
    data = (level, subject, roll)

    if table == 'solution':
        query = "SELECT * FROM solution WHERE level = %s AND subject = %s"
        data = (level, subject)

    cursor.execute(query, data)
    records = cursor.fetchall()
    return records


def insert(level, subject, roll):
    global cursor, connection

    query_result = "INSERT INTO result(level,subject,roll) VALUES(%s,%s,%s)"
    data_result = (level, subject, roll)
    cursor.execute(query_result, data_result)
    connection.commit()


def update(key, value, level, subject, roll):
    global cursor, connection

    query = "UPDATE result SET " + key + " = %s WHERE level = %s AND subject = %s AND roll = %s"
    data = (value, level, subject, roll)

    if key == 'number':
        query = "UPDATE result SET number = %s WHERE level = %s AND subject = %s AND roll = %s"
        data = (value, level, subject, roll)

    cursor.execute(query, data)
    connection.commit()


def get_solution(level, subject, roll):
    ANSWER_KEY = []

    records = select('solution', level, subject, roll)

    for row in records:
        for i in range(3, 23):
            ANSWER_KEY.append(row[i])

    return ANSWER_KEY


connection = mysql.connector.connect(host='localhost', database='16_mcq_evaluator', user='root', password='')
cursor = connection.cursor()
