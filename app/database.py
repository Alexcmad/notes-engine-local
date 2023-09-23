import sqlite3
CONTENT_LIMIT = 500
# Create or connect to the database file (if it doesn't exist, a new one will be created)
initial_conn = sqlite3.connect('file_database.db')

# Create a cursor object to interact with the database
initial_cursor = initial_conn.cursor()

# Create a table with a unique constraint on the "filename" column
initial_cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT UNIQUE,  -- Enforce uniqueness on the filename
        content TEXT,
        keywords TEXT
    )
''')

# Commit changes and close the database connection
initial_conn.commit()
initial_conn.close()


def insert_file_data(filename, content, keywords):
    conn = sqlite3.connect('file_database.db')
    cursor = conn.cursor()

    # Convert the keywords list to a comma-separated string
    keywords_str = ', '.join(keywords)

    content = content[:CONTENT_LIMIT]

    # Insert the data into the files table
    cursor.execute("INSERT OR IGNORE INTO files (filename, content, keywords) VALUES (?, ?, ?)",
                   (filename, content, keywords_str))

    # Commit changes and close the database connection
    conn.commit()
    conn.close()


def query_files_by_keywords(keywords):
    conn = sqlite3.connect('file_database.db')
    cursor = conn.cursor()

    # Create a set to store unique file IDs
    unique_file_ids = set()

    # Iterate through the keywords and search for matching files
    for keyword in keywords:
        # Search for files with matching keywords in the "keywords" column
        cursor.execute("SELECT id FROM files WHERE keywords LIKE ?", ('%' + keyword + '%',))
        matching_ids = cursor.fetchall()
        unique_file_ids.update(matching_ids)

        # Search for files with matching keywords in the "content" column
        cursor.execute("SELECT id FROM files WHERE content LIKE ?", ('%' + keyword + '%',))
        matching_ids = cursor.fetchall()
        unique_file_ids.update(matching_ids)

        cursor.execute("SELECT id FROM files WHERE filename LIKE ?", ('%' + keyword + '%',))
        matching_ids = cursor.fetchall()
        unique_file_ids.update(matching_ids)

    # Retrieve file details for the unique file IDs
    matching_files = []
    for file_id in unique_file_ids:
        cursor.execute("SELECT filename, content, keywords FROM files WHERE id=?", (file_id[0],))
        file_data = cursor.fetchone()
        file_dict = {
            'filepath': file_data[0],
            'content': file_data[1],
            'keywords': file_data[2]
        }
        matching_files.append(file_dict)

    # Close the database connection
    conn.close()

    return matching_files
