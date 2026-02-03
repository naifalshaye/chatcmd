"""
Command history management for ChatCMD.
"""

import sqlite3
import datetime
import os
from typing import Optional, Any

from chatcmd.constants import ERROR_CODES


class CMD:
    """Command history operations."""

    @staticmethod
    def add_cmd(
        conn: sqlite3.Connection,
        cursor: sqlite3.Cursor,
        prompt: str,
        command: str,
        model_name: Optional[str] = None,
        provider_name: Optional[str] = None
    ) -> bool:
        """Add a command to history."""
        try:
            cursor.execute(
                "INSERT INTO history (prompt,command,model_name,provider_name,created_at) VALUES(?,?,?,?,?)",
                (prompt, command, model_name, provider_name, datetime.datetime.now().isoformat())
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error {ERROR_CODES['NO_COMMANDS']}: Failed to add command to history: {e}")
            return False

    @staticmethod
    def get_cmd(cursor: sqlite3.Cursor) -> None:
        """Display the last command from history."""
        from chatcmd import Colors, colored_print

        try:
            cursor.execute(
                "SELECT prompt, command, model_name, provider_name, created_at "
                "FROM history ORDER BY id DESC LIMIT 1"
            )
            command = cursor.fetchone()

            if command is not None:
                model_info = f" ({command[2]})" if command[2] else ""
                colored_print("Latest Command:\n", Colors.GOLD, bold=True)
                colored_print(" ", Colors.WHITE, end="")
                colored_print(command[0] + ": ", Colors.CYAN, bold=True, end="")
                colored_print(command[1], Colors.BRIGHT_GREEN, bold=True, end="")
                colored_print(model_info + "\n", Colors.YELLOW)
            else:
                colored_print("History is empty.", Colors.YELLOW)

        except sqlite3.Error as e:
            colored_print(f"Error {ERROR_CODES['INVALID_NUMBER']}: Failed to get last command from history: {e}", Colors.RED, bold=True)

    @staticmethod
    def get_last_num_cmd(cursor: sqlite3.Cursor, number: Any) -> bool:
        """Display the last N commands from history."""
        from chatcmd import Colors, colored_print

        try:
            number = int(number)
            if number < 1:
                colored_print('History is empty.', Colors.YELLOW)
                return False

            cursor.execute(
                "SELECT prompt, command, created_at FROM history ORDER BY id DESC LIMIT ?",
                (number,)
            )
            total_commands = cursor.fetchall()

            if total_commands:
                colored_print('Latest Commands:\n', Colors.GOLD, bold=True)
                for command in total_commands:
                    colored_print("  ", Colors.WHITE, end="")
                    colored_print(command[0] + ": ", Colors.CYAN, bold=True, end="")
                    colored_print(command[1], Colors.BRIGHT_GREEN, bold=True)
            else:
                colored_print("History is empty.", Colors.YELLOW)
            return True

        except ValueError as ve:
            colored_print(str(ve), Colors.RED)
        except sqlite3.Error as e:
            colored_print(f"Error {ERROR_CODES['DELETE_FAILED']}: Failed to get last command from history: {e}", Colors.RED, bold=True)
        return False

    @staticmethod
    def delete_cmd(conn: sqlite3.Connection, cursor: sqlite3.Cursor) -> bool:
        """Delete the last command from history."""
        from chatcmd import Colors, colored_print

        try:
            cursor.execute("SELECT id FROM history ORDER BY id DESC LIMIT 1")
            latest_record = cursor.fetchone()

            if latest_record:
                cursor.execute("DELETE FROM history WHERE id = ?", (latest_record[0],))
                conn.commit()
                colored_print("Latest command deleted successfully.", Colors.GREEN, bold=True)
                return True
            else:
                colored_print("History is empty.", Colors.YELLOW)
                return False

        except sqlite3.Error as e:
            colored_print(f"Error {ERROR_CODES['DELETE_ERROR']}: Failed deleting last command: {e}", Colors.RED, bold=True)
            return False

    @staticmethod
    def clear_history(conn: sqlite3.Connection, cursor: sqlite3.Cursor) -> bool:
        """Clear all command history."""
        from chatcmd import Colors, colored_print

        try:
            cursor.execute('DELETE FROM history')
            conn.commit()
            colored_print("\nAll command lookup has been cleared.", Colors.GREEN, bold=True)
            return True
        except sqlite3.Error as e:
            colored_print(f"Error {ERROR_CODES['CLEAR_HISTORY_ERROR']}: Failed clearing history: {e}", Colors.RED, bold=True)
            return False

    @staticmethod
    def get_db_size(db_path: str) -> None:
        """Display the database file size."""
        from chatcmd import Colors, colored_print

        file_size_bytes = os.path.getsize(db_path)
        units = ['bytes', 'KB', 'MB', 'GB']
        size = float(file_size_bytes)
        unit_index = 0

        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1

        colored_print(f"\nDB File size: {size:.2f} {units[unit_index]}\n", Colors.GOLD, bold=True)

    @staticmethod
    def get_commands_count(cursor: sqlite3.Cursor) -> int:
        """Get the total count of commands in history."""
        cursor.execute('SELECT COUNT(*) FROM history')
        count = cursor.fetchone()[0]
        return count

    @staticmethod
    def delete_last_num_cmd(
        conn: sqlite3.Connection,
        cursor: sqlite3.Cursor,
        number: Any
    ) -> bool:
        """Delete the last N commands from history."""
        from chatcmd import Colors, colored_print

        try:
            cursor.execute('SELECT COUNT(*) FROM history')
            count = cursor.fetchone()[0]

            if count == 0:
                colored_print('History is empty.', Colors.YELLOW)
                return False

            # Validate and sanitize number parameter
            try:
                number = max(1, min(int(number), 10000))
            except (ValueError, TypeError):
                colored_print('Please enter a valid number.', Colors.RED)
                return False

            # Use parameterized query for LIMIT
            cursor.execute("SELECT id FROM history ORDER BY id DESC LIMIT ?", (number,))
            latest_records = cursor.fetchall()

            if latest_records:
                record_ids = [record[0] for record in latest_records]
                placeholders = ','.join(['?'] * len(record_ids))
                cursor.execute(f"DELETE FROM history WHERE id IN ({placeholders})", record_ids)
                conn.commit()
                colored_print("Commands deleted successfully.", Colors.GREEN, bold=True)
                return True

            return False

        except sqlite3.Error:
            colored_print(f"Error {ERROR_CODES['DELETE_RANGE_ERROR']}: Failed to delete commands from history.", Colors.RED, bold=True)
            return False


commands = CMD()
