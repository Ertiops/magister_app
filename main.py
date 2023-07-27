import os
from flask import Flask, render_template, flash, redirect, url_for, request, g, session
import sqlite3
from datetime import datetime
from FDataBase import FDataBase
import NaiveBayes

DATABASE = '/tmp/texts.db'


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'texts.db')))
app.config['SECRET_KEY'] = "hbjasdadfbjkiljk;afhjlkfAOIN;F"

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    dbase = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        dbase.cursor().executescript(f.read())
    dbase.commit()
    dbase.close()

def get_db():
    '''Соединение с БД, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

database = None
@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global database
    dbase = get_db()
    database = FDataBase(dbase)

@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/', methods=['GET'])
def info():
    return render_template('info.html')


@app.route('/classify_topic', methods=['GET', 'POST'])
def classify_topic():
    category_type = 'topic'
    data = database.getTopicData(category_type)

    if request.method == 'POST':
        text = request.form.get('text')
        category = NaiveBayes.classify_topic(text)[0]
        current_datetime = datetime.now()
        database.addData(text, category_type, category, current_datetime)
        flash('Анализ текста сохранен в базе данных', category='success')
        return redirect(url_for('classify_topic'))



    return render_template('classify_topic.html', data=data)


@app.route('/classify_grade', methods=['GET', 'POST'])
def classify_grade():
    category_type = 'grade'
    data = database.getTopicData(category_type)

    if request.method == 'POST':
        text = request.form.get('text')
        category = NaiveBayes.classify_grade(text)[0]
        current_datetime = datetime.now()
        database.addData(text, category_type, category, current_datetime)
        flash('Анализ текста сохранен в базе данных', category='success')
        return redirect(url_for('classify_grade'))



    return render_template('classify_grade.html', data=data)


@app.route("/delete_topic")
def delete_text_topic():
    current_time = request.args.get('current_time', None)

    database.deleteText(current_time)

    return redirect(url_for('classify_topic'))


@app.route("/delete_grade")
def delete_text_grade():
    current_time = request.args.get('current_time', None)

    database.deleteText(current_time)

    return redirect(url_for('classify_grade'))


# print(NaiveBayes.classify_topic('броуновское движение'))

# print(NaiveBayes.classify_grade('броуновское движение'))


if __name__ == '__main__':
   app.run(debug=True)    


# create_db()



