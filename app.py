from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
 
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] ='root'
app.config['MYSQL_DB']='todo_list'

mysql = MySQL(app)
    
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    task = cur.fetchall()
    cur.close()
    return render_template('index.html',tasks = task)
 
@app.route('/insert', methods=['POST'])
def insert():
    print(request.form)
    if request.method =="POST":
        task_id = request.form['task_id']
        task_title = request.form['task_title']
        task_description = request.form['task_description']
       
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO tasks (task_id, task_title, task_description) VALUES (%s, %s, %s)', (task_id, task_title, task_description))
        mysql.connection.commit()
        mysql.connection.rollback()
 
        return redirect(url_for('index'))

@app.route('/update/<int:task_id>', methods=['POST'])
def update(task_id):
    if request.method =="POST":
        task_id = request.form.get('task_id')
        task_title = request.form.get('task_title')
        task_description = request.form.get('task_description')

        cur = mysql.connection.cursor()
        cur.execute('UPDATE tasks SET task_title=%s, task_description=%s WHERE task_id=%s',(task_title, task_description, task_id))
        mysql.connection.commit()
        mysql.connection.rollback()

        return redirect(url_for('index'))
 
    
@app.route('/delete/<string:task_id>', methods=['POST'])
def delete(task_id):
    if request.method =="POST":
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM tasks WHERE task_id= %s",(task_id))
        mysql.connection.commit()
        return redirect (url_for('index'))
 
if __name__== "__main__":
    app.run(debug=True)