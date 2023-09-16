import sqlite3
import datetime
import os


class CMD:

    @staticmethod
    def add_cmd(conn, cursor, prompt, command):
        try:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, "
                "prompt TEXT, command TEXT, created_at DATETIME)")
            conn.commit()

            cursor.execute("INSERT INTO history (prompt,command,created_at) VALUES(?,?,?)",
                           (prompt, command, datetime.datetime.now()))
            conn.commit()

            return True
        except sqlite3.Error as e:
            print(f"Error 1012: Failed to add command to history: {e}")
        return False

    @staticmethod
    def get_cmd(cursor):
        try:
            cursor.execute("SELECT prompt, command, created_at FROM history ORDER BY id DESC LIMIT 1")
            command = cursor.fetchone()

            if command is not None:
                print("Latest Command:\n\n " + command[0] + ": " + command[1] + "\n")
            else:
                print("History is empty.")

        except sqlite3.Error as e:
            print(f"Error 1013: Failed to get last command from history: {e}")

    @staticmethod
    def get_last_num_cmd(cursor, number):
        try:
            number = int(number)
            if number < 1:
                print('History is empty.')
            cursor.execute("SELECT prompt, command, created_at FROM history ORDER BY id DESC LIMIT ?", (number,))
            total_commands = cursor.fetchall()
            if len(total_commands) > 0:
                print('Latest Command:\n')

                for command in total_commands:
                    print(f'  - {command[1]}')
            else:
                print("History is empty.")
            return True
        except ValueError as ve:
            print(str(ve))
        except sqlite3.Error as e:
            print(f"Error 1014: Failed to get last command from history: {e}")
        return False

    @staticmethod
    def delete_cmd(conn, cursor):
        try:
            select_query = "SELECT * FROM history ORDER BY id DESC LIMIT 1"
            cursor.execute(select_query)
            latest_record = cursor.fetchone()

            if latest_record:
                delete_query = "DELETE FROM history WHERE id = ?"
                cursor.execute(delete_query, (latest_record[0],))
                conn.commit()
                print("Latest command deleted successfully.")

        except sqlite3.Error as e:
            print(f"Error 1015: Failed deleting last command: {e}")
        return False

    @staticmethod
    def clear_history(conn, cursor):
        try:
            cursor.execute('DELETE FROM history')
            conn.commit()
            print("\nAll command lookup has been cleared.")
            return True
        except sqlite3.Error as e:
            print(f"Error 1017: Failed clearing history: {e}")
        return False

    @staticmethod
    def get_db_size(db_path):
        file_size_bytes = os.path.getsize(db_path)
        units = ['bytes', 'KB', 'MB', 'GB']
        size = file_size_bytes
        unit_index = 0

        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1

        print(f"\nDB File size: {size:.2f} {units[unit_index]}\n")

    @staticmethod
    def get_commands_count(cursor):
        cursor.execute('SELECT COUNT(*) FROM history')
        count = cursor.fetchone()[0]
        return count

    @staticmethod
    def delete_last_num_cmd(conn, cursor, number):
        try:
            cursor.execute('SELECT COUNT(*) FROM history')
            count = cursor.fetchone()[0]

            if count == 0:
                print('History is empty.')
            else:
                number = int(number)
                if number < 1:
                    print('Please enter a correct number.')
                else:
                    select_query = f"SELECT * FROM history ORDER BY id DESC LIMIT {number}"
                    cursor.execute(select_query)
                    latest_records = cursor.fetchall()

                    if latest_records:
                        record_ids = [record[0] for record in latest_records]
                        delete_query = f"DELETE FROM history WHERE id IN ({','.join(['?'] * len(record_ids))})"
                        cursor.execute(delete_query, record_ids)
                        conn.commit()
                        print("Commands deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error 1016: Failed to get last command from history: {e}")


commands = CMD()
