import sqlite3
import settings
import datetime
from babel.dates import format_date, format_datetime, format_time

db_file = settings.db_file

def get_Biermeter_By_Date():
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        list = {}
        result = None

        result = cur.execute('SELECT team_name, sum(amount), strftime("%Y-%m-%d", timestamp) FROM order_history WHERE item="Biermeter" GROUP BY team_name, strftime("%Y-%m-%d", timestamp) ORDER BY strftime("%Y-%m-%d", timestamp) DESC, sum(amount) DESC')
        for row in result:
                timestamp =  datetime.datetime.strptime(row[2], '%Y-%m-%d')
                weekday = format_date(timestamp, "EEEE", locale='de')
                buffer = list.get(weekday,[])
                buffer.append({
                             "team": row[0],
                             "amount" : row[1]
                             })
                list[weekday] = buffer
        con.close()
        return list

def getOrderOverview():
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        list = []
        result = None

        result = cur.execute('SELECT item, sum(amount), sum(price) FROM order_history GROUP BY item ORDER BY sum(amount) DESC')
        for row in result:
                list.append({
                        "name": row[0],
                        "amount" : row[1],
                        "price" : row[2]
                        })
        con.close()
        return list