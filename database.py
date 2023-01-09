import psycopg2
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')

host = config['DB']['host']
user = config['DB']['user']
password = config['DB']['password']
db_name = config['DB']['db_name']


def db_decorator(func):
    def wrapper(*args):
        try:
            # connect to exist database
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )

            connection.autocommit = True

            result = func(connection, args[0], args[1] if len(args) > 1 else 0)
            return result

        except Exception as _ex:
            print('[INFO] Error while working with PostgreSQL', _ex)
        finally:
            if connection:
                connection.close()
                print('[INFO] PostgreSQL connection closed')
    return wrapper


@db_decorator
def check_users(connection, *args):
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT name from lurker'
        )
        return args[0] in [user_name[0] for user_name in cursor.fetchall()]


@db_decorator
def get_points(connection, *args):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT points FROM lurker WHERE name=%s;", (args[0],)
        )
        return cursor.fetchone()[0]


@db_decorator
def update_points(connection, *args):
    with connection.cursor() as cursor:
        cursor.execute(
            f"UPDATE lurker SET points=%s WHERE name=%s;", (args[1], args[0])
        )


@db_decorator
def update_vip_time(connection, *args):
    with connection.cursor() as cursor:
        cursor.execute(
            f"UPDATE lurker SET vip_time=%s WHERE name=%s;", (args[1], args[0])
        )


@db_decorator
def get_vip_time(connection, *args):
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT vip_time from lurker where name=%s;", (args[0],)
        )
        return cursor.fetchone()[0]


@db_decorator
def insert_user(connection, *args):
    with connection.cursor() as cursor:
        cursor.execute(
            f"INSERT INTO lurker(name) values(%s);", (args[0],)
        )


if __name__ == '__main__':
    # print(check_users('pianoparrot'))
    # print(get_points('pianoparrot'))
    # update_points('pianoparrot', 50)
    # print(get_points('PianoParrot'))
    # print(update_vip_time('PianoParrot', 100))
    print(get_vip_time('PianoParrot'))
