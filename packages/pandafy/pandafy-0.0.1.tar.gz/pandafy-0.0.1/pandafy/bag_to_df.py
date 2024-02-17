import pandas as pd
import os
import subprocess
import sqlite3
import sys
import path_utils
from typing import List

def fetch_all_tablenames(path_to_bag:str):
    conn = sqlite3.connect(path_to_bag)
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    cursor = conn.cursor()
    cursor.execute(query)
    tables = cursor.fetchall()
    cursor.close()
    conn.close()
    return [table[0] for table in tables]

def fetch_all_dfs(path_to_bag:str):
    table_names = fetch_all_tablenames(path_to_bag)
    conn = sqlite3.connect(path_to_bag)
    query = lambda table_name: f"SELECT * FROM {table_name}"
    dfs = {table_name:pd.read_sql_query(query(table_name),conn) for table_name in table_names}
    return dfs





    