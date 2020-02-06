from django.db import Error, connections
from django.conf import settings

def query_to_list(cursor):
    columns = [col[0] for col in cursor.description]

    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]

def __get_bwv_cursor__():
    return connections[settings.BWV_DATABASE_NAME].cursor()

def do_query(query):
    try:
        cursor = __get_bwv_cursor__()
        cursor.execute(query)
        return query_to_list(cursor)

    except Exception as e:
        print('BWV Database Query failed')
        print(e)
        print('Query:')
        print(query)
        return []


def return_first_or_empty(executed_query):
    if len(executed_query) > 0:
        return executed_query[0]
    else:
        return {}
