import sqlite3

def connect_to_database(db_name):
    connection = sqlite3.connect(db_name)
    return connection

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')
    connection.commit()

def save_item(connection, name, quantity, price):
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)
    ''', (name, quantity, price))
    connection.commit()

def load_items(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM inventory')
    return cursor.fetchall()

def update_item(connection, item_id, name, quantity, price):
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE inventory SET name = ?, quantity = ?, price = ? WHERE id = ?
    ''', (name, quantity, price, item_id))
    connection.commit()

def delete_item(connection, item_id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
    connection.commit()

def search_items(connection, search_term):
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM inventory WHERE name LIKE ?
    ''', ('%' + search_term + '%',))
    return cursor.fetchall()

def filter_items(connection, quantity=None, price=None):
    cursor = connection.cursor()
    query = 'SELECT * FROM inventory WHERE 1=1'
    params = []
    if quantity is not None:
        query += ' AND quantity = ?'
        params.append(quantity)
    if price is not None:
        query += ' AND price = ?'
        params.append(price)
    cursor.execute(query, params)
    return cursor.fetchall()

def close_connection(connection):
    connection.close()