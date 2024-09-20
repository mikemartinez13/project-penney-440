import sqlite3
import pandas as pd
import sqlite3
import pandas as pd
import os

def make_database(results,path):
    df = pd.DataFrame(results, columns=['seed','deck','p1_seq', 'p2_seq','p1_num_tricks','p2_num_tricks','win_tricks','p1_num_cards','p2_num_cards','win_cards'])
    db = DB(path, create = True)
    # this had the connect_db() method
    db.insert_results(df)
    return db.get_database_file()

class DB:
    def __init__(self,
                 path_db: str ,        # Path to the database file
                 create: bool = False # Should we create a new database if it doesn't exist?
                ):
        
        # Check if the file does not exist
        if not os.path.exists(path_db):
            # Should we create it?
            if create:
                self.conn = sqlite3.connect(path_db)
                self.conn.close()
            else:
                raise FileNotFoundError(path_db + ' does not exist.')
        self.path_db = path_db
        return
    

    def connect_db(self):
        self.conn = sqlite3.connect(self.path_db)
        self.curs = self.conn.cursor()

    def close(self) -> None:
        if self.conn:
            self.conn.close()

    def insert_results(self, df) -> None:
        self.connect_db()
        df.to_sql('win_results', self.conn, if_exists='append', index=False)
        self.close

  
    def run_query(self, sql: str, params=None, manage_conn=True):
        if manage_conn:
            self.connect_db()  # Establish a database connection

        # Execute the SQL query
        results = pd.read_sql(sql, self.conn, params=params)

        if manage_conn:
            self.close()  # Close the connection

        return results

    def run_action(self,
                   sql: str,
                   params: tuple|dict = None,
                   commit: bool = False,
                   keep_open: bool = False
                  ) -> int:
        
        if self.conn:
            self.connect_db()
            
        try:
            if params is None:
                self.curs.execute(sql)
            else:
                self.curs.execute(sql, params)

            if commit:
                self.conn.commit()
        except Exception as e:
            self.conn.rollback() #Undo all changes since the last commit
            self.close()
            raise type(e)(f'sql: {sql}\nparams: {params}') from e

        if not keep_open:
            self.close()

    def get_database_file(self):
        return self.path_db

