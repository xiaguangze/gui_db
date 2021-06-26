import pymysql


def connect_db(host, port, user, pswd, database=""):
    connection_db = pymysql.connect(host=host, port=port, user=user, password=pswd, database=database)
    cursor = connection_db.cursor()

    return cursor


def return_data(host, port, user, pswd, sql, databases="", status=0):
    cursor = connect_db(host, port, user, pswd, database=databases)
    cursor.execute(sql)
    data = cursor.fetchall()
    result = []
    if status == 0:
        for dt in data:
            result.append(dt[0])
    else:
        for dt in data:
            result.append(list(dt))

    return result

