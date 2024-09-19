import sqlite3

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = sqlite3.connect('contacts.db')
    return conn

def create_table():
    """Create the contacts table if it does not exist."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def add_contact(name, phone):
    """Add a new contact to the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
    conn.commit()
    conn.close()

def get_all_contacts():
    """Retrieve all contacts from the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts')
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_contact(contact_id):
    """Delete a contact from the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
    conn.commit()
    conn.close()

def update_contact(contact_id, name, phone):
    """Update a contact in the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE contacts SET name = ?, phone = ? WHERE id = ?', (name, phone, contact_id))
    conn.commit()
    conn.close()