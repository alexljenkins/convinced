import logging
import sqlite3
import random
from typing import Tuple, List, Any, Union, Optional
from datetime import datetime
from src.database.entries import Entry, EntryCombat

logger = logging.getLogger(__name__)

def db_connect():
    db = LiteConnector('convinceme')
    db.connect()
    db.run_query('''
            CREATE TABLE IF NOT EXISTS convinceme_001 (
                response_id INTEGER PRIMARY KEY,
                user_input TEXT,
                character_response TEXT,
                vote_count INTEGER,
                elo INTEGER,
                enabled BOOLEAN
            )
            ''')
    db.run_query('''
                CREATE TABLE IF NOT EXISTS convinceme_001_log (
                    vote_id INTEGER PRIMARY KEY,
                    winning_response_id INTEGER,
                    losing_response_id INTEGER,
                    change_in_elo INTEGER,
                    created TIMESTAMP
                )
                ''')
    return db


def print_table_contents(db, table_name:str = 'convinceme_001') -> None:
    query = f"SELECT * FROM {table_name}"
    results = db.read_data(query)
    
    for row in results:
        logger.info(row)


def check_entry_against_db(db, user_input:str) -> Union[str, bool]:
    # Check if the user input is already in the database
    entry = db.read_data(f"SELECT * FROM convinceme_001 WHERE user_input = ?", [user_input])
    # If the user input is already in the database, return the saved response
    if entry:
        return entry[0][2]
    return False


def get_entries_for_voting(db, split_at:float = 1/2) -> EntryCombat:
    count = db.read_data("SELECT COUNT(*) FROM convinceme_001")[0][0]
    logger.info(f'Found {count} entries.')
    split_at = int((count * split_at))
    
    top_choice = random.randint(1, split_at-1)
    bottom_choice = random.randint(split_at, count)

    query = f"SELECT * FROM convinceme_001 WHERE response_id IN ({top_choice}, {bottom_choice})"

    entries = db.read_data(query)
    random.shuffle(entries)

    if entries[0][0] == entries[1][0]:
        raise Exception('Error - entries are the same')
    
    # Return the top and bottom rows as entries with combat resolution
    entry_a = Entry.from_list(entries[0])
    entry_b = Entry.from_list(entries[1])
    entries = EntryCombat(response_a = entry_a, response_b = entry_b)
    
    return entries


def save_entry(db, new) -> None:
    db.run_query("INSERT INTO convinceme_001 (user_input, character_response, vote_count, elo, enabled) VALUES (?, ?, ?, ?, ?)", new.to_db())


def update_entry_with_character(db, user_input:str, character_response:str) -> None:
    db.run_query(f"UPDATE convinceme_001 SET character_response = {character_response} WHERE response_id = {id} AND user_input = {user_input}")

def update_entry_from_vote(db, id:int, elo:int, vote_count:int) -> None:
    db.run_query(f"UPDATE convinceme_001 SET vote_count = {vote_count}, elo = {elo} WHERE response_id = {id}")

def add_vote_to_db_log(db, winning_response_id:int, losing_response_id:int, rating_change:int) -> None:
    db.run_query(f"""
        INSERT INTO convinceme_001_log
        (winning_response_id, losing_response_id, change_in_elo, created)
        VALUES (?, ?, ?)""", [winning_response_id, losing_response_id, rating_change, datetime.now()])


def delete_entry_from_vote(db, id:int) -> None:
    db.run_query(f"DELETE FROM convinceme_001 WHERE response_id = {id}")


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