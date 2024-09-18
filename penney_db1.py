import sqlite3
import pandas as pd
import sqlite3
import pandas as pd

class DB:
    def __init__(self, db_name='../04_Store/example.db'):
        """Initialize the database connection."""
        self.db_name = db_name
        self.conn = None
        self.curs = None

    def connect_db(self):
        """Establish a connection to the SQLite database."""
        self.conn = sqlite3.connect(self.db_name)
        self.curs = self.conn.cursor()

    def close(self) -> None:
        """Close the database connection."""
        if self.conn:
            self.conn.close()

    def insert_results(self, df: pd.DataFrame) -> None:
        """Insert results DataFrame into the database."""
        df.to_sql('results', self.conn, if_exists='append', index=False)

  
    def run_query(self, sql: str, params=None, manage_conn=True):
        """Run a SQL query and return the results as a DataFrame."""
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


