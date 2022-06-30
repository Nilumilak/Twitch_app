import psycopg2
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')

host = config['DB']['host']
user = config['DB']['user']
password = config['DB']['password']
db_name = config['DB']['db_name']

def check_users(user_name):
    try:
        # connect to exist database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        connection.autocommit = True

        # the cursor for persorrming database operations

        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT name from lurker'
            )
            return user_name in [user_name[0] for user_name in cursor.fetchall()]

    except Exception as _ex:
        print('[INFO] Error while working with PostgreSQL', _ex)
    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')


def get_score(user_name):
    try:
        # connect to exist database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        # the cursor for persorrming database operations

        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT score FROM lurker WHERE name='{user_name}';"
            )
            return cursor.fetchone()[0]

    except Exception as _ex:
        print('[INFO] Error while working with PostgreSQL', _ex)
    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')


def update_score(user_name, score):
    try:
        # connect to exist database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        connection.autocommit = True

        # the cursor for persorrming database operations

        with connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE lurker SET score={score} WHERE name='{user_name}';"
            )

    except Exception as _ex:
        print('[INFO] Error while working with PostgreSQL', _ex)
    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')


def insert_user(user_name):
    try:
        # connect to exist database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        connection.autocommit = True

        # the cursor for persorrming database operations

        with connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO lurker(name) values('{user_name}');"
            )

    except Exception as _ex:
        print('[INFO] Error while working with PostgreSQL', _ex)
    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')

if __name__ == '__main__':
    pass