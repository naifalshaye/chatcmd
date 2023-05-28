import sqlite3
from .helpers import *

def get_api_key(conn, cursor):
    try:
        cursor.execute('CREATE TABLE IF NOT EXISTS config (id INTEGER PRIMARY KEY, api_key TEXT)')
        conn.commit()

        cursor.execute('INSERT OR IGNORE INTO config (id, api_key) VALUES(?,?)', [1,None])
        conn.commit()

        cursor.execute("SELECT api_key FROM config WHERE id = 1")
        api_key = cursor.fetchone()
        if api_key[0] is not None:
            if (validate_api_key(api_key[0])):
                return api_key[0]
        return None
    except sqlite3.Error as e:
        print(f"Error 1003: Failed to get API key from database: {e}")
        return None

def output_api_key(conn, cursor):
    try:
        api_key = get_api_key(conn, cursor)
        print("\n ChatGPT API key: "+api_key+"\n")
    except Exception as e:
        print(f"Error 1004: Failed to output API key: {e}")
        return None

def save_api_key(conn, cursor, api_key):
    try:
        cursor.execute("UPDATE config SET api_key = ? WHERE id = ?", (api_key,1))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error 1005: Failed to save API key to database: {e}")

def ask_for_api_key(conn, cursor):
    try:
        while True:
            api_key = input("\nEnter a valid ChatGPT API key: ")
            if (validate_api_key(api_key)):
                if save_api_key(conn, cursor, api_key):
                    print("\nChatGPT API Key updated successfully.\n")
                    return api_key
            print('Error 1006: Invalid ChatGPT API key!')
    except Exception as e:
        print(f"Error 1007: Failed asking for API key: {e}")