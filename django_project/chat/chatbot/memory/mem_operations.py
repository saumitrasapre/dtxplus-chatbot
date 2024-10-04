import psycopg2

from django.conf import settings


def clear_memory(thread_id="1"):
    db_config = settings.DATABASES["default"]
    conn = psycopg2.connect(
        database=db_config["NAME"],
        user=db_config["USER"],
        password=db_config["PASSWORD"],
        host="localhost",
        port="5432",
    )
    conn.autocommit = True
    cursor = conn.cursor()
    tables = ['checkpoints','checkpoint_blobs','checkpoint_writes']
    for tab in tables:
        sql = f'''DELETE FROM {tab} WHERE thread_id=%s''' 
        cursor.execute(sql, (thread_id,)) 
        conn.commit()
    conn.close()

def get_next_available_thread_id():
    try:
        # Connect to the PostgreSQL database
        db_config = settings.DATABASES["default"]
        conn = psycopg2.connect(
        database=db_config["NAME"],
        user=db_config["USER"],
        password=db_config["PASSWORD"],
        host="localhost",
        port="5432",
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Query to fetch all distinct thread_ids
        query = "SELECT DISTINCT thread_id FROM checkpoints ORDER BY thread_id ASC;"
        cursor.execute(query)
        existing_ids = cursor.fetchall()

        # Convert the list of tuples into a flat list of integers
        existing_ids = [int(row[0]) for row in existing_ids]

        # Find the first missing integer
        if existing_ids:
            for i in range(1, max(existing_ids) + 1):
                if i not in existing_ids:
                    return i
            return max(existing_ids) + 1  # If no gaps, return the next number
        else:
            return 1  # Start from 1 if no thread_ids exist

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()  