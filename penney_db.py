import pandas as pd
import sqlite3
import os

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
    
    def connect(self) -> None:
        self.conn = sqlite3.connect(self.path_db)
        self.curs = self.conn.cursor()
        return
    
    def close(self) -> None:
        self.conn.close()
        return
    
    def run_query(self, sql:str,params=None, manage_conn=True):
        if manage_conn: self.connect()
        results = pd.read_sql(sql, self.conn, params = params)
        if manage_conn: self.close()
        return results


    def build_tables(self):
        '''
        Build all tables in the database,
        assuming they do not exist
        '''
        self.connect()
        self.curs.execute("DROP TABLE IF EXISTS tPenney;")
        
        sql = """
        CREATE TABLE tPenney (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            p1_guess TEXT NOT NULL,
            p2_guess TEXT NOT NULL,
            p1_cards INTEGER,
            p2_cards INTEGER,
            p1_tricks INTEGER,
            p2_tricks INTEGER,
            win_cards TEXT NOT NULL,
            win_tricks TEXT NOT NULL
        )
        ;"""
        self.curs.execute(sql)
        return

    def who_wins(self,p1_guess, p2_guess, p1_pot, p2_pot, p1_tricks,p2_tricks):
       
        self.connect()

        if p1_pot>p2_pot:
            win_cards='p1'
        if p1_pot<p2_pot:
            win_cards='p2'
        if p1_pot == p2_pot:
            win_cards='draw' ##need to ask abt what to do in this case
        if p1_tricks>p2_tricks:
            win_tricks='p1'
        if p2_tricks>p1_tricks:
            win_tricks='p2'
        if p1_tricks == p2_tricks:
            win_tricks='draw' ##need to ask abt what to do in this case
            
        sql= '''
            INSERT INTO tPenney (p1_guess, p2_guess, p1_cards, p2_cards, p1_tricks, p2_tricks,win_cards, win_tricks)
            VALUES (:p1_guess, :p2_guess, :p1_cards, :p2_cards, :p1_tricks, :p2_tricks, :win_cards, :win_tricks);

        '''
        
        self.curs.execute(sql, (p1_guess, p2_guess, p1_pot, p2_pot, p1_tricks,p2_tricks, win_cards, win_tricks))
        self.conn.commit()
        
        return
   
