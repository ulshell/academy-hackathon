import os

from flask import Flask
from flask import request

from flask import render_template
import psycopg2
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL)
curr = conn.cursor()

# our fake db
todo_store = {}
todo_store['depo'] = ['Go for run', 'Listen Rock Music']
todo_store['shivang'] = ['Read book', 'Play Fifa', 'Drink Coffee']
todo_store['raj'] = ['Study', 'Brush']
todo_store['sanket'] = ['Sleep', 'Code']
todo_store['aagam'] = ['play cricket', 'have tea']

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    def select_todos(name):
        curr.execute('SELECT todo FROM todolist WHERE name=name')
        todo = curr.fetchall()
        return todo

    def insert_todo(name, todo):
        curr.execute('INSERT INTO todolist VALUES(%s, %s)', (name, todo))
        conn.commit()
        return

    def add_todo_by_name(name, todo):
        # call DB function
        #insert_todo(name, todo)
        insert_todo(name, todo)



    def get_todos_by_name(name):
        try:
            return select_todos(name)
        except:
            return None


    # http://127.0.0.1:5000/todos?name=duster
    @app.route('/todos')
    def todos():
        name = request.args.get('name')
        print('---------')
        print(name)
        print('---------')

        person_todo_list = get_todos_by_name(name)
        if person_todo_list == None:
            return render_template('404.html'), 404
        else:
            person_todo_list = [x[0] for x in person_todo_list]
            return render_template('todo_view.html',todos=person_todo_list)


    @app.route('/add_todos')
    def add_todos():
        name = request.args.get('name')
        todo = request.args.get('todo')
        add_todo_by_name(name, todo)
        return 'Added Successfully'

    return app

