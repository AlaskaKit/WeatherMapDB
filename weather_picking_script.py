import sys
import psycopg2
from config import *


def select_cities(low_temp: float = 14.0, high_temp: float = 21.0) -> None:
    """
    Selects from the weather table records with certain temperature parameters and writes them to another table.
    DB credentials and parameters are set in the config file.
    If requested city already present in the table, its values are being updated.
    Throws error if DB is not found and if there are no required table in the DB.
    :return: the writing/updating status if there were no errors.
    """
    # connect to db
    try:
        conn = psycopg2.connect(
            host=HOST,
            database=DBNAME,
            user=USER,
            password=PASSWORD
        )
    except psycopg2.Error as err:
        print(err.pgerror, file=sys.stderr)
        sys.exit(1)
    
    # creating cursor
    cursor = conn.cursor()
    
    # creating table in case it doesn't exits
    try:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS public.{SORTED_W} "
                       f"AS TABLE {UNSORTED_W} WITH NO DATA")
                       
    except psycopg2.Error as err:
        print(err.pgerror, file=sys.stderr)
        sys.exit(1)
    
    # copying values
    try:
        cursor.execute(f"INSERT INTO {SORTED_W} SELECT * FROM {UNSORTED_W} "
                       f"WHERE temperature > {low_temp} OR temperature < {high_temp}")

    except psycopg2.Error as err:
        print(err.pgerror, file=sys.stderr)
        sys.exit(1)
    
    # commit transaction
    conn.commit()
    
    # close cursor
    cursor.close()
    
    # close connection
    conn.close()
    
    print(f"Transaction executed successfully.")


if __name__ == '__main__':
    select_cities()
