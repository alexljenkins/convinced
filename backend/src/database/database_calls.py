import logging
import sqlite3
from typing import List, Any, Union
from datetime import datetime
from database.entries import Entry, EntryCombat

logger = logging.getLogger(__name__)

# DATABASE.run_query(f"ALTER TABLE convinceme_001 ADD COLUMN report_count INTEGER DEFAULT 0")
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
                enabled BOOLEAN DEFAULT FALSE,
                report_count INTEGER DEFAULT 0
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
    db.run_query('''
                CREATE TABLE IF NOT EXISTS convinceme_001_report_log (
                    report_id INTEGER PRIMARY KEY,
                    response_id INTEGER,
                    created TIMESTAMP
                )
                ''')
    return db


def get_table_contents(db, enabled: int = 0, report_count:int = 0) -> List[List[Any]]:
    if report_count == 0:
        query = f"SELECT * FROM convinceme_001 WHERE enabled = ? AND report_count = ?"
    else:
        query = f"SELECT * FROM convinceme_001 WHERE enabled = ? AND report_count >= ?"
    results = db.read_data(query, [enabled, report_count])

    entries = []
    for result in results:
        entries.append(Entry.from_list(result).to_review())
    
    return entries


def check_entry_against_db(db, user_input:str) -> Union[str, bool]:
    # Check if the user input is already in the database
    entry = db.read_data(f"SELECT * FROM convinceme_001 WHERE user_input = ?", [user_input])
    # If the user input is already in the database, return the saved response
    if entry:
        return entry[0][2]
    return False


def get_entries_for_voting(db) -> EntryCombat:
    # enabled = true OR not reported yet. enabled is false by default, and only set to true by admin endpoint
    query = f"SELECT * FROM convinceme_001 WHERE enabled = 1 OR report_count < 2 ORDER BY RANDOM() LIMIT 2"
    entries = db.read_data(query)
    # random.shuffle(entries)

    if entries[0][0] == entries[1][0]:
        # get_entries_for_voting(db)
        raise Exception('Error - entries are the same')
    
    # Return the top and bottom rows as entries with combat resolution
    entry_a = Entry.from_list(entries[0])
    entry_b = Entry.from_list(entries[1])
    entries = EntryCombat(response_a = entry_a, response_b = entry_b)
    
    return entries

def get_specific_voted_on_entries(db, winner_id:int, loser_id:int) -> EntryCombat:
    query = f"SELECT * FROM convinceme_001 WHERE response_id IN ({int(winner_id)}, {int(loser_id)})"
    entries = db.read_data(query)

    if len(entries) != 2:
        raise Exception(f'Error {len(entries)} found. Expected 2.')
    
    # always put winner as entry_a/response_a
    if entries[0][0] == winner_id:
        entry_a = Entry.from_list(entries[0])
        entry_b = Entry.from_list(entries[1])
    else:
        entry_a = Entry.from_list(entries[1])
        entry_b = Entry.from_list(entries[0])
    entries = EntryCombat(response_a = entry_a, response_b = entry_b)
    return entries


def save_entry(db, new) -> None:
    db.run_query("INSERT INTO convinceme_001 (user_input, character_response, vote_count, elo, enabled) VALUES (?, ?, ?, ?, ?)", new.to_db())


def update_entry_with_character(db, user_input:str, character_response:str) -> None:
    db.run_query(f"UPDATE convinceme_001 SET character_response = {character_response} WHERE response_id = {id} AND user_input = {user_input}")

def update_entry_from_vote(db, id:int, elo:int, vote_count:int) -> None:
    db.run_query(f"UPDATE convinceme_001 SET vote_count = {vote_count}, elo = {elo} WHERE response_id = {id}")

def admin_entry_switch(db, id:int, enabled:int = 1) -> None:
    db.run_query(f"UPDATE convinceme_001 SET enabled = {enabled} WHERE response_id = {id}")

def add_vote_to_db_log(db, winning_response_id:int, losing_response_id:int, rating_change:int) -> None:
    db.run_query(f"""
        INSERT INTO convinceme_001_log
        (winning_response_id, losing_response_id, change_in_elo, created)
        VALUES (?, ?, ?, ?)""", [winning_response_id, losing_response_id, rating_change, datetime.now()])

def report_response_id(db, response_id:int):
    # add to log
    db.run_query(f"""
        INSERT INTO convinceme_001_report_log
        (response_id, created)
        VALUES (?, ?)""", [response_id, datetime.now()])
    
    # add to snapshot table
    db.run_query(f"""UPDATE convinceme_001 SET report_count = report_count + ? WHERE response_id = ?""", [1, response_id])


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
