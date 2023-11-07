import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

#flash  the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'

# function to open a connection to the database file
def get_db_connection():
    # get connection
    conn = sqlite3.connect('database.db')

    # allows us to have name based access to columns
    conn.row_factory = sqlite3.Row

    # return the connection object
    return conn

# function to get singular post
def get_post(post_id):
    query = 'SELECT * FROM posts WHERE id = ?'

    conn = get_db_connection()
    post = conn.execute(query, (post_id,)).fetchone()
    conn.close()

    if post is None:
        abort(404)

    return post

# use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def index():
    # get a db connection
    conn = get_db_connection()

    # execute a query to get all posts from the database
    query = 'SELECT * FROM posts'
    posts = conn.execute(query).fetchall() # fetchall() gets all rows from the query result

    # close the connection
    conn.close()
    
    return render_template('index.html', posts=posts)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']

        # display an error if title or content not submitted
        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else: # make database connect and insert new post
            query = 'INSERT INTO posts (title, content) VALUES (?, ?)'
            
            conn = get_db_connection()
            conn.execute(query, (title, content))
            conn.commit()
            conn.close()

            return redirect(url_for('index'))

    return render_template('create.html')

#route to edit post
@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']

        # display an error if title or content not submitted
        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else: # make database connect and insert new post
            query = 'UPDATE posts SET title = ?, content = ? WHERE id = ?'

            conn = get_db_connection()
            conn.execute(query, (title, content, id))
            conn.commit()
            conn.close()

            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

# route to delete a post
@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_post(id)

    query = 'DELETE FROM posts WHERE id = ?'

    conn = get_db_connection()
    conn.execute(query, (id,))
    conn.commit()
    conn.close()

    flash('"{}" was successfully deleted'.format(post['title']))

    return redirect(url_for('index'))


app.run(host="0.0.0.0", port=5001)