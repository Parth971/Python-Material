import psycopg2

def create_db_connection(host_name='localhost', user_name='postgres', user_password='parth123', db_name='grocerystoredb'):
    connection = None
    try:
        connection = psycopg2.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
    except Exception as err:
        print(f"Exception: '{err}'")

    return connection

def execute_query(query):
    connection = create_db_connection()
    cursor = connection.cursor()
    msg = None
    try:
        cursor.execute(query)
        connection.commit()
    except psycopg2.IntegrityError:
        connection.rollback()
        msg = 'Already exists!'
    except Exception as err:
        connection.rollback()
        print(f"Exception: '{err}'")
    finally:
        cursor.close()
        connection.close()

    return msg

def read_query(query):
    connection = create_db_connection()
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as err:
        print(f"Exception: '{err}'")
    finally:
        cursor.close()
        connection.close()