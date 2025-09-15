import sqlite3
import datetime
import os


class CMD:

    @staticmethod
    def add_cmd(conn, cursor, prompt, command, model_name=None, provider_name=None):
        try:
            cursor.execute("INSERT INTO history (prompt,command,model_name,provider_name,created_at) VALUES(?,?,?,?,?)",
                           (prompt, command, model_name, provider_name, datetime.datetime.now()))
            conn.commit()

            return True
        except sqlite3.Error as e:
            print(f"Error 1012: Failed to add command to history: {e}")
        return False

    @staticmethod
    def get_cmd(cursor):
        from chatcmd import Colors, colored_print
        
        try:
            cursor.execute("SELECT prompt, command, model_name, provider_name, created_at FROM history ORDER BY id DESC LIMIT 1")
            command = cursor.fetchone()

            if command is not None:
                model_info = f" ({command[2]})" if command[2] else ""
                colored_print("Latest Command:\n", Colors.GOLD, bold=True)
                
                # Color the prompt and response differently
                colored_print(" ", Colors.WHITE, end="")  # Space before prompt
                colored_print(command[0] + ": ", Colors.CYAN, bold=True, end="")  # Prompt in cyan
                colored_print(command[1], Colors.BRIGHT_GREEN, bold=True, end="")  # Command in bright green
                colored_print(model_info + "\n", Colors.YELLOW)  # Model info in yellow
            else:
                colored_print("History is empty.", Colors.YELLOW)

        except sqlite3.Error as e:
            colored_print(f"Error 1013: Failed to get last command from history: {e}", Colors.RED, bold=True)

    @staticmethod
    def get_last_num_cmd(cursor, number):
        from chatcmd import Colors, colored_print
        
        try:
            number = int(number)
            if number < 1:
                colored_print('History is empty.', Colors.YELLOW)
            cursor.execute("SELECT prompt, command, created_at FROM history ORDER BY id DESC LIMIT ?", (number,))
            total_commands = cursor.fetchall()
            if len(total_commands) > 0:
                colored_print('Latest Command:\n', Colors.GOLD, bold=True)

                for command in total_commands:
                    # Color the prompt and response differently
                    colored_print("  ", Colors.WHITE, end="")  # Indentation
                    colored_print(command[0] + ": ", Colors.CYAN, bold=True, end="")  # Prompt in cyan
                    colored_print(command[1], Colors.BRIGHT_GREEN, bold=True)  # Command in bright green
            else:
                colored_print("History is empty.", Colors.YELLOW)
            return True
        except ValueError as ve:
            colored_print(str(ve), Colors.RED)
        except sqlite3.Error as e:
            colored_print(f"Error 1014: Failed to get last command from history: {e}", Colors.RED, bold=True)
        return False

    @staticmethod
    def delete_cmd(conn, cursor):
        from chatcmd import Colors, colored_print
        
        try:
            select_query = "SELECT * FROM history ORDER BY id DESC LIMIT 1"
            cursor.execute(select_query)
            latest_record = cursor.fetchone()

            if latest_record:
                delete_query = "DELETE FROM history WHERE id = ?"
                cursor.execute(delete_query, (latest_record[0],))
                conn.commit()
                colored_print("Latest command deleted successfully.", Colors.GREEN, bold=True)

        except sqlite3.Error as e:
            colored_print(f"Error 1015: Failed deleting last command: {e}", Colors.RED, bold=True)
        return False

    @staticmethod
    def clear_history(conn, cursor):
        from chatcmd import Colors, colored_print
        
        try:
            cursor.execute('DELETE FROM history')
            conn.commit()
            colored_print("\nAll command lookup has been cleared.", Colors.GREEN, bold=True)
            return True
        except sqlite3.Error as e:
            colored_print(f"Error 1017: Failed clearing history: {e}", Colors.RED, bold=True)
        return False

    @staticmethod
    def get_db_size(db_path):
        from chatcmd import Colors, colored_print
        
        file_size_bytes = os.path.getsize(db_path)
        units = ['bytes', 'KB', 'MB', 'GB']
        size = file_size_bytes
        unit_index = 0

        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1

        colored_print(f"\nDB File size: {size:.2f} {units[unit_index]}\n", Colors.GOLD, bold=True)

    @staticmethod
    def get_commands_count(cursor):
        cursor.execute('SELECT COUNT(*) FROM history')
        count = cursor.fetchone()[0]
        return count

    @staticmethod
    def delete_last_num_cmd(conn, cursor, number):
        from chatcmd import Colors, colored_print
        
        try:
            cursor.execute('SELECT COUNT(*) FROM history')
            count = cursor.fetchone()[0]

            if count == 0:
                colored_print('History is empty.', Colors.YELLOW)
            else:
                number = int(number)
                if number < 1:
                    colored_print('Please enter a correct number.', Colors.RED)
                else:
                    select_query = f"SELECT * FROM history ORDER BY id DESC LIMIT {number}"
                    cursor.execute(select_query)
                    latest_records = cursor.fetchall()

                    if latest_records:
                        record_ids = [record[0] for record in latest_records]
                        delete_query = f"DELETE FROM history WHERE id IN ({','.join(['?'] * len(record_ids))})"
                        cursor.execute(delete_query, record_ids)
                        conn.commit()
                        colored_print("Commands deleted successfully.", Colors.GREEN, bold=True)
        except sqlite3.Error as e:
            colored_print(f"Error 1016: Failed to get last command from history: {e}", Colors.RED, bold=True)


commands = CMD()
