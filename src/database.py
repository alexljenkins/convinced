import sqlite3
import random

def db_connect():
    db = LiteConnector('convinceme')
    db.connect()
    db.run_query('''
            CREATE TABLE IF NOT EXISTS convinceme_001 (
                id INTEGER PRIMARY KEY,
                user_input TEXT,
                response TEXT,
                vote_count INTEGER,
                elo INTEGER
            )
            ''')
    db.run_query('''
                CREATE TABLE IF NOT EXISTS convinceme_001_log (
                    event_id INTEGER PRIMARY KEY,
                    winning_response_id INTEGER,
                    winner_new_elo INTEGER,
                    losing_response_id INTEGER,
                    loser_new_elo INTEGER,
                    change_in_elo INTEGER
                )
                ''')
    return db


def print_table_contents(db, table_name = 'convinceme_001'):
    query = f"SELECT * FROM {table_name}"
    results = db.read_data(query)
    
    for row in results:
        print(row)


def check_entry_against_db(db, user_input):
    # Check if the user input is already in the database
    entry = db.read_data(f"SELECT * FROM convinceme_001 WHERE user_input = ?", [user_input])
    # If the user input is already in the database, return the saved response
    if entry:
        return entry[0][2]
    return False


def get_entries_for_voting(db, top_group = 2/3, bottom_group = 1/3):
    count = db.read_data("SELECT COUNT(*) FROM convinceme_001")[0][0]
    top_choice = random.randint(1, (count * top_group)-1)
    bottom_choice = random.randint(count - (count * bottom_group), count - 1)
    print(f"Top Choice: {top_choice}, Bottom Choice: {bottom_choice}")
    query = f"SELECT * FROM convinceme_001 WHERE id IN ({top_choice}, {bottom_choice})"

    entries = db.read_data(query)
    random.shuffle(entries)
    
    # Return the top and bottom rows
    return list(entries[0]), list(entries[1])


def save_entry(db, user_input, response, elo):
    db.run_query("INSERT INTO convinceme_001 (user_input, response, vote_count, elo) VALUES (?, ?, 0, ?)", [user_input, response, elo])

def update_entry(db, id, elo, vote_count):
    db.run_query(f"UPDATE convinceme_001 SET vote_count = {vote_count + 1}, elo = {elo} WHERE id = {id}")

def add_to_db_log(db, winning_response, losing_response, rating_change):
    db.run_query(f"""
        INSERT INTO convinceme_001_log
        (winning_response_id, winner_new_elo, losing_response_id, loser_new_elo, change_in_elo)
        VALUES (?, ?, ?, ?, ?)""", [winning_response[0], winning_response[4], losing_response[0], losing_response[4], rating_change])

    
class LiteConnector:
    database: str
    connection: ...
    cursor: ...

    def __init__(self, database, *args, **kwargs):
        # self.username = username
        # self.password = password
        # self.hostname = hostname
        self.database = database
        # self.schema = schema

    def connect(self):
        if not hasattr(self, "connection"):
            self.connection = sqlite3.connect(f"{self.database}.db")
        if not hasattr(self, "cursor"):
            self.cursor = self.connection.cursor()

    def read_data(self, query: str, varaibles: list = []):
        if varaibles:
            self.cursor.execute(query, varaibles)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def write_data(self, query: str):
        self.cursor.execute(query)
        self.connection.commit()

    def run_query(self, query, varaibles: list = []):
        if varaibles:
            self.cursor.execute(query, varaibles)
        else:
            self.cursor.execute(query)
        self.connection.commit()

    def df_to_table(self, df, table_name, if_exists="replace"):
        df.to_sql(name=table_name, con=self.connection, if_exists=if_exists)
        self.connection.commit()

    def disconnect(self):
        if hasattr(self, "connection"):
            self.connection.close()

    def __enter__(self):
        """ Determines what to do when opening a database connection using the content manager. """
        self.connect()

    def __exit__(self):
        """ Determines what happens when closing a database connection using the content manager. """
        self.disconnect()


if __name__ == '__main__':
    print_table_contents(db_connect())