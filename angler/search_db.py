import sqlite3

def search_flags(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        # Get all columns for the current table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        for column in columns:
            column_name = column[1]
            # Check if the column is text-based
            if column[2] in ('TEXT', 'VARCHAR', 'CHAR'):
                # Search for 'flag{...}' pattern
                cursor.execute(f"SELECT * FROM {table_name} WHERE {column_name} LIKE 'flag{{%' ESCAPE '\\';")
                rows = cursor.fetchall()
                for row in rows:
                    print(f"Found in {table_name}.{column_name}: {row}")

    conn.close()

search_flags('roadrecon.db')
