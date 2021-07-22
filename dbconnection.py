import sqlite3

class DBConnection:
    def __init__(self, dbname = 'data.db'):
        self.db_con = sqlite3.connect(dbname)
        self.db_cur = self.db_con.cursor()
    
    def create_table(self):
        self.db_cur.execute('''create table if not exists au_systems (
            asn integer PRIMARY KEY,
            organization text,
            country text
        )''')

    def insert(self, asn, org_info, country):
        self.db_cur.execute(f"insert into au_systems values ('{asn}', '{org_info}', '{country}')")

    def insert_all(self, values):
        self.db_cur.executemany('insert into au_systems values (?,?,?)', values)

    def find(self, column, value):
        self.db_cur.execute(f"select * from au_systems where {column}='{value}'")
        return self.db_cur.fetchall()

    def find_one(self, column, value):
        self.db_cur.execute(f"select * from au_systems where {column}='{value}'")
        return self.db_cur.fetchone()
    
    def find_all(self):
        self.db_cur.execute('select * from au_systems')
        return self.db_cur.fetchall()
    
    def commit(self):
        self.db_con.commit()

    def close(self):
        self.db_con.close()