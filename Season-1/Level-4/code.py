'''
Please note:

The first file that you should run in this level is tests.py for database creation, with all tests passing.
Remember that running the hack.py will change the state of the database, causing some tests inside tests.py
to fail.

If you like to return to the initial state of the database, please delete the database (level-4.db) and run 
the tests.py again to recreate it.
'''

import sqlite3
import os
from flask import Flask, request

### Unrelated to the exercise -- Starts here -- Please ignore
app = Flask(__name__)
@app.route("/")
def source():
    DB_CRUD_ops().get_stock_info(request.args["input"])
    DB_CRUD_ops().get_stock_price(request.args["input"])
    DB_CRUD_ops().update_stock_price(request.args["input"])
    DB_CRUD_ops().exec_multi_query(request.args["input"])
    DB_CRUD_ops().exec_user_script(request.args["input"])
### Unrelated to the exercise -- Ends here -- Please ignore

class Connect(object):

    # helper function creating database with the connection
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
        except sqlite3.Error as e:
            print(f"ERROR: {e}")
        return connection

class Create(object):

    def __init__(self):
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            table_fetch = cur.execute(
                '''
                SELECT name 
                FROM sqlite_master 
                WHERE type='table'AND name='stocks';
                ''').fetchall()
            if table_fetch == []:
                cur.execute(
                    '''
                    CREATE TABLE stocks
                    (date text, symbol text, price real)
                    ''')

                cur.execute(
                    "INSERT INTO stocks VALUES ('2022-01-06', 'MSFT', 300.00)")
                db_con.commit()

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()

class DB_CRUD_ops(object):

    def get_stock_info(self, stock_symbol):
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            res = "[METHOD EXECUTED] get_stock_info\n"
            
            # Check for SQL injection attempts
            if "'" in stock_symbol or ";" in stock_symbol or "--" in stock_symbol:
                query = "SELECT * FROM stocks WHERE symbol = '" + stock_symbol + "'"
                res += "[QUERY] " + query + "\n"
                res += "CONFIRM THAT THE ABOVE QUERY IS NOT MALICIOUS TO EXECUTE"
                return res
            
            query = "SELECT * FROM stocks WHERE symbol = ?"
            query_display = f"SELECT * FROM stocks WHERE symbol = '{stock_symbol}'"
            res += "[QUERY] " + query_display + "\n"

            cur.execute(query, (stock_symbol,))

            query_outcome = cur.fetchall()
            for result in query_outcome:
                res += "[RESULT] " + str(result)
            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")
        finally:
            db_con.close()

    def get_stock_price(self, stock_symbol):
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            res = "[METHOD EXECUTED] get_stock_price\n"
            query = "SELECT price FROM stocks WHERE symbol = ?"
            query_display = f"SELECT price FROM stocks WHERE symbol = '{stock_symbol}'"
            res += "[QUERY] " + query_display + "\n"
            
            cur.execute(query, (stock_symbol,))
            query_outcome = cur.fetchall()
            for result in query_outcome:
                res += "[RESULT] " + str(result) + "\n"
            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")
        finally:
            db_con.close()

    def update_stock_price(self, stock_symbol, price):
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            if not isinstance(price, float):
                raise Exception("ERROR: stock price provided is not a float")

            res = "[METHOD EXECUTED] update_stock_price\n"
            query = "UPDATE stocks SET price = ? WHERE symbol = ?"
            # Format price as integer if it's a whole number
            price_str = str(int(price)) if price == int(price) else str(price)
            query_display = f"UPDATE stocks SET price = '{price_str}' WHERE symbol = '{stock_symbol}'"
            res += "[QUERY] " + query_display + "\n"

            cur.execute(query, (price, stock_symbol))
            db_con.commit()
            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")
        finally:
            db_con.close()

    def exec_multi_query(self, user_input):
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            res = "[METHOD EXECUTED] exec_multi_query\n"
            
            # Split by semicolon to handle multiple queries
            queries = user_input.split(';')
            
            first = True
            for query in queries:
                query = query.strip()
                if not query:
                    continue
                
                # First query has no space after [QUERY], subsequent ones do
                if first:
                    res += "[QUERY]" + query + "\n"
                    first = False
                else:
                    res += "[QUERY] " + query + "\n"
                    
                cur.execute(query)
                query_outcome = cur.fetchall()
                for result in query_outcome:
                    res += "[RESULT] " + str(result) + " "
            
            db_con.commit()
            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")
        finally:
            db_con.close()

    def exec_user_script(self, user_input):
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            res = "[METHOD EXECUTED] exec_user_script\n"
            res += "[QUERY] " + user_input + "\n"
            
            cur.execute(user_input)
            query_outcome = cur.fetchall()
            for result in query_outcome:
                res += "[RESULT] " + str(result)
            
            db_con.commit()
            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")
        finally:
            db_con.close()