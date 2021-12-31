import psycopg2
import json


from config import DATABASE, USER, PASSWORD

conn = psycopg2.connect(database=DATABASE,
                        user=USER,
                        password=PASSWORD,
                        host="localhost",
                        port="5432")
cur = conn.cursor()

table_name = 'qtimetable'
filename = 'data.json'

def create_database(conn, cur, table_name):
    create_rasp_table = f"""
    CREATE TABLE {table_name} (
    id SERIAL,
    class_name VARCHAR(256),
    week VARCHAR(256),
    weekday INTEGER,
    class_num INTEGER,
    pr_id INTEGER
    );
    """
    create_teachers_table = f"""
    CREATE TABLE teachers (
    id SERIAL,
    name VARCHAR(256),
    place VARCHAR(256)
    );
    """
    cur.execute(create_rasp_table)
    cur.execute(create_teachers_table)
    # cur.close()
    conn.commit()

def post_timetable_to_db(conn, cur, filename):
    with open(filename, encoding='UTF-8') as file:
        data = json.loads(file.read())
    print(data)
    insert_data = f"""
    INSERT INTO {table_name} (class_name, week, weekday, class_num, pr_id)
    VALUES (%s, %s, %s, %s, %s);
    """
    for i, item in enumerate(data):
        class_num = str(i % 5)
        weekday = str((i // 5) % 6)
        # print(i, class_num, weekday)
        cur.execute(insert_data, (str(item['para']), str(item['week']), weekday, class_num, item['pr_id'], ))
    cur.execute(f'SELECT * FROM {table_name};')
    conn.commit()

def post_teachers_to_db(conn, cur):
    teachers = [
        ['Панков', 'к.520'],
        ['Сретенская', 'к.522'],
        ['Аршинов', 'к.301'],
        ['Куприн', 'к.312'],
        ['Королев', 'к.621'],
        ['Бакулин', 'к.502'],
        ['Калабекьянц', 'к.321'],
        ['Чупак', 'к.213'],
        ['Антипов', 'к.502'],
        ['Вакансия', 'к.213']
    ]
    insert_data = f"""
    INSERT INTO teachers (name, place)
    VALUES (%s, %s);
    """
    for teacher in teachers:
       cur.execute(insert_data, (teacher[0], teacher[1], ))
    cur.close()
    conn.commit()

# create_database(conn, cur, table_name)
post_timetable_to_db(conn, cur, filename)
post_teachers_to_db(conn, cur)
