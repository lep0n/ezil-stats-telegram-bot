import sqlite3


conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()


def insert(table: str, column_values: dict) -> None:
    """Insert new row in table"""

    columns = ", ".join( column_values.keys() )
    values = [tuple(column_values.values())]
    placeholders = ", ".join( "?" * len(column_values.keys()) )

    cursor.executemany(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
        values
    )
    conn.commit()


def update(table: str, user_id: int, column_values: dict) -> None:
    """Update row values in table"""

    values = ", ".join(["=".join(tuple(map(lambda v: f"'{v}'", value))) \
        for value in column_values.items()])
    cursor.execute(f"UPDATE {table} SET {values} WHERE {user_id=}")
    conn.commit()


def fetchall(table: str, columns: list) -> list:
    """Return dict with columns from table"""

    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    conn.commit()

    result = []

    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def fetchone(table: str, user_id: int, column: str) -> str:
    """Return one column from table"""

    cursor.execute(f"SELECT {column} FROM {table} WHERE {user_id=}")
    result = cursor.fetchone()
    conn.commit()

    return result[0]


def delete(table: str, user_id: int) -> None:
    """Delete row from table"""
    
    cursor.execute(f"DELETE FROM {table} WHERE {user_id=}")
    conn.commit()
