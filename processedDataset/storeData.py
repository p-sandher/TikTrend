import sqlite3
import csv

# Connect to database
def create_connection(db_name):
    return sqlite3.connect(db_name)

# Create a new table
def create_table(conn, create_table_sql):
    """Create a table from a SQL statement."""
    with conn:
        conn.execute(create_table_sql)

# Fetch data from CSV
def populate_table_from_csv(conn, table_name, csv_file_path, columns):
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None) 

        placeholders = ', '.join(['?' for _ in columns])
        insert_query = f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({placeholders})'

        with conn:
            conn.executemany(insert_query, csv_reader)

#Populate a table with data
def populate_table(conn, table_name, columns, data):
    placeholders = ', '.join(['?' for _ in columns])
    insert_query = f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({placeholders})'

    with conn:
        conn.executemany(insert_query, data)

def main():
    db_name = 'tiktrend.db'
    hashtag_csv = 'hashtag_counts.csv'
    post_csv = 'preprocessedAccountData.csv'

    # Table creation SQL
    create_hashtags_table_sql = '''
    CREATE TABLE IF NOT EXISTS Hashtags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hashtag TEXT NOT NULL,
        count INTEGER NOT NULL
    )
    '''
    create_posts_table_sql = '''
    CREATE TABLE IF NOT EXISTS Posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        monthSin REAL NOT NULL,
        monthCos REAL NOT NULL,
        daySin REAL NOT NULL,
        dayCos REAL NOT NULL,
        hourSin REAL NOT NULL,
        hourCos REAL NOT NULL,
        weekdaySin REAL NOT NULL,
        weekdayCos REAL NOT NULL,
        hashtagVectors TEXT NOT NULL,
        nLikes INTEGER NOT NULL,
        nShares INTEGER NOT NULL,
        nFollowers INTEGER NOT NULL,
        nComments INTEGER NOT NULL,
        nViews INTEGER NOT NULL,
        nAccountTotalLikes INTEGER NOT NULL,
        postYear INTEGER NOT NULL
    )
    '''

    posts_columns = [
        "monthSin", "monthCos", "daySin", "dayCos", "hourSin", "hourCos", 
        "weekdaySin", "weekdayCos", "hashtagVectors", "nLikes", "nShares", 
        "nFollowers", "nComments", "nViews", "nAccountTotalLikes", "postYear"
    ]
    # Connect to the database
    conn = create_connection(db_name)

    # Create tables
    create_table(conn, create_hashtags_table_sql)
    create_table(conn, create_posts_table_sql)

    # Populate Hashtags table from CSV
    populate_table_from_csv(conn, "Hashtags", hashtag_csv, ["hashtag", "count"])

    populate_table_from_csv(conn, "Posts", post_csv, posts_columns)


    # Close the connection
    conn.close()
    print("Database setup and population complete.")

if __name__ == "__main__":
    main()
