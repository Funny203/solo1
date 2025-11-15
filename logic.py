from config import *
import sqlite3

class DB_Manager:
    def __init__(self, database):
        self.database = database
    
    def __select_data(self, sql, data=()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
        
    def get_state_data(self, state_name):
        sql = "SELECT Market, Min_Price, Max_Price FROM market_prices WHERE State=? ORDER BY Min_Price ASC LIMIT 10"
        return self.__select_data(sql, (state_name,))

if __name__ == '__main__':
    manager = DB_Manager(DATABASE)