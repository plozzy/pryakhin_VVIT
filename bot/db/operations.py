def simple_select(conn, cur, select_what, select_from, where=None):

    if where:
        where_expression = f'WHERE {where};'
    else:
        where_expression = ''
    select_what_str = ', '.join(select_what)
    cur.execute(f'''
        SELECT ({select_what_str}) FROM {select_from}
            {where_expression}
    ''')
    result_tuples = cur.fetchall()
    result_list = [item[0] if item[0] != 'None' else None for item in result_tuples]

    return result_list
