import psycopg2
from flask import Flask, render_template, request, redirect

from config import DATABASE, USER, PASSWORD

app = Flask(__name__)
conn = psycopg2.connect(database=DATABASE,
                        user=USER,
                        password=PASSWORD,
                        host='localhost',
                        port='5432')
cursor = conn.cursor()


@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login/', methods=['POST'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            cursor.execute("SELECT * FROM users WHERE login=%s AND password=%s",
                            (str(username), str(password)))
            records = list(cursor.fetchall())
            match (username, password):
                case ('', ''):
                    return "Вы ничего не ввели"
                case (username, ''):
                    return "Вы не ввели пароль"
                case ('', password):
                    return "Вы не ввели логин"
                case (username, password):
                    if not records:
                        return ('Неверное имя пользователя или пароль')
                    else:
                        return render_template('account.html', full_name=records[0][1])
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        if not name.replace(' ', '').isalpha():
            return 'В имени должны быть только буквы'
        login = request.form.get('login')
        password = request.form.get('password')

        cursor.execute("SELECT * FROM users WHERE login=%s",
                        (str(login),))
        if not cursor.fetchone():
            cursor.execute('INSERT INTO users (fullname, login, password) VALUES (%s, %s, %s);',
                        (str(name), str(login), str(password)))
            conn.commit()
        else:
            return "Вы уже зарегистрированы"
        return redirect('/login/')

    return render_template('registration.html')
