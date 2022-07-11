import sqlite3
import settings

db_file = settings.db_file

def init():
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        #Create Table "biermeter"
        cur.execute('''
            CREATE TABLE IF NOT EXISTS biermeter (
                id INTEGER PRIMARY KEY,
                team TEXT NOT NULL,
                Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        #Create Table "teams"
        cur.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                contactPerson VARCHAR(300),
                email VARCHAR(300)
            );
        ''')

        #Create Table "infos"
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS infos (
                        id INTEGER PRIMARY KEY,
                        titel char NOT NULL,
                        content TEXT NOT NULL,
                        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    );
                ''')

        #Create Table "items"
        cur.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                price DECIMAL(5,2)
            );
        ''')


        #Create Table "order_history"
        cur.execute('''
            CREATE TABLE IF NOT EXISTS order_history (
                id INTEGER PRIMARY KEY,
                team_id INTEGER NOT NULL,
                team_name VARCHAR(100) NOT NULL,
                item VARCHAR(100) NOT NULL,
                amount INTEGER NOT NULL,
                price DECIMAL(5,2),
                user_name VARCHAR(100),
                cash INTEGER,
                Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        con.commit()
        con.close()


def beer(team : str, add : bool):
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        if(add):
                cur.execute("INSERT INTO biermeter(team) VALUES (?)", (team,))
        elif(not add):
                timestamp = cur.execute("SELECT Timestamp FROM biermeter WHERE team=? ORDER BY Timestamp DESC LIMIT 1;", (team,)).fetchone()[0]
                cur.execute("DELETE FROM biermeter WHERE Timestamp=?", (timestamp,))
                print(timestamp)
        con.commit()
        con.close()


def get_List(ranking = False):
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        list = []
        result = None
        if ranking:
                result = cur.execute('SELECT team_name, sum(amount) FROM order_history WHERE item="Biermeter" GROUP BY team_name ORDER BY sum(amount) DESC')
        else:
                result = cur.execute('SELECT team, count(*) FROM biermeter GROUP BY team ORDER BY team')
        for row in result:
                list.append({""
                             "team": row[0],
                             "amount" : row[1]
                             })
        con.close()
        return list

def get_Teams():
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        list = []
        result = cur.execute('SELECT * FROM teams ORDER BY name ASC')
        for row in result:
                list.append({
                        "id":row[0],
                        "name":row[1],
                        "contactPerson":row[2],
                        "email":row[3],
                })

        con.close()
        return list


def add_Team(name, contactPerson=None, email=None):
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        try:
                cur.execute("INSERT INTO teams(name, contactPerson, email) VALUES (?,?,?)", (name, contactPerson, email))
        except Exception as e:
                print(e)
        con.commit()
        con.close()



def delete_Team(id):
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        team = cur.execute("SELECT name FROM teams WHERE id=?", (id,)).fetchone()[0]
        cur.execute("DELETE FROM biermeter WHERE team=?", (team,))
        cur.execute("DELETE FROM teams WHERE id=?", (id,))

        con.commit()
        con.close()



def get_Infos():
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        list = []
        result = cur.execute('SELECT * FROM infos ORDER BY timestamp desc')
        for row in result:
                list.append({
                        "id": row[0],
                        "title": row[1],
                        "content": row[2],
                        "Timestamp": row[3]
                })

        con.close()
        return list


def add_Info(title : str, content : str):
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        cur.execute("INSERT INTO infos(title, content) VALUES (?,?)", (title,content))

        con.commit()
        con.close()

def delete_Info(id):
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        cur.execute("DELETE FROM infos WHERE id=?", (id,))

        con.commit()
        con.close()

def get_Items():
        con = sqlite3.connect(db_file)
        cur = con.cursor()

        list = []
        result = cur.execute('SELECT * FROM items ORDER BY name ASC')
        for row in result:
                list.append({
                        "id":row[0],
                        "name":row[1],
                        "price":row[2]
                })

        con.close()
        return list


def add_Order(_data : dict):
        con = sqlite3.connect(db_file)
        cur = con.cursor()
        user_name = _data["user"]
        team_id = _data["team_id"]
        team_name = _data["team_name"]
        cash = _data["cash"]
        basket = _data["basket"]
        for item in basket:
                cur.execute("INSERT INTO order_history(team_id, team_name, item, amount, price, user_name, cash) VALUES (?,?,?,?,?,?,?)",
                            (team_id, team_name, basket[item]["name"], basket[item]["amount"], basket[item]["sum"], user_name, cash))
        con.commit()
        con.close()




if __name__ == "__main__":
        init()