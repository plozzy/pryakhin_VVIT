import psycopg2

from utils.config import *

conn = psycopg2.connect(database=DATABASE,
                        user=USER,
                        password=PASSWORD,
                        host='localhost',
                        port='5432')
cur = conn.cursor()
