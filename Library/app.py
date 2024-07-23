import os
import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for, session
from forms import *
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    search_form = SearchForm()
    if request.method == 'POST':
        return redirect(url_for('search', name=search_form.search.data))
    if session.get('name', "") == "Admin":
        books = conn.execute('SELECT * FROM books order by id').fetchall()
    else:
        books = conn.execute('SELECT * FROM books where rented = 0  order by id').fetchall()
    conn.close()
    return render_template('home.html', books=books, search_form=search_form)

@app.route('/search/<string:name>', methods=['GET', 'POST'])
def search(name):
    if not name:
        return redirect(url_for('index'))
    search_form = SearchForm()
    search_form.search.data = name
    if request.method == 'POST':
        return redirect(url_for('search', name=search_form.search.data))
    conn = get_db_connection()
    books = conn.execute(f"SELECT * FROM books WHERE name LIKE '%{name}%' order by id").fetchall()
    conn.close()
    return render_template('home.html', books=books, search_form=search_form)

@app.route('/books', methods=['GET', 'POST'])
def books():
    if session.get('id'):
        search_form = SearchForm()
        if request.method == 'POST':
            return redirect(url_for('search', name=search_form.search.data))
        conn = get_db_connection()
        books = conn.execute(f'SELECT * FROM Books JOIN book_rented ON books.id = book_rented.book_id WHERE book_rented.user_id = {session.get("id")} order by id').fetchall()
        conn.close()
        return render_template('home.html', books=books, heading="My Books", search_form=search_form)
    else:
        return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if session.get('name', ''):
        return redirect(url_for('index'))
    form = SignInForm(request.form)
    if request.method == 'POST' and form.validate():
        conn = get_db_connection()
        user = conn.execute(f"SELECT * FROM users where username = '{form.username.data}'").fetchall()
        if user:
            flash(f'Account already exists {form.username.data}', 'danger')
            return redirect(url_for('books'))
        query1 = f"INSERT INTO users (username, password) VALUES ('{form.username.data}', '{form.password.data}')"    
        conn.execute(query1)
        conn.commit()
        conn.close()
        flash(f'Account created {form.username.data}', 'success')
        return redirect(url_for('index'))
    return render_template('signup.html', form=form, name="Sign In")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('name', ''):
        return redirect(url_for('index'))
    form = LogInForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.username.data == "Admin":
            flash(f'You are a Librarian, Try Librarian Login', 'danger')
            return redirect(url_for('login'))
        conn = get_db_connection()
        user = conn.execute(f"SELECT * FROM users where username = '{form.username.data}'").fetchone()
        if user and user['password'] == form.password.data:
            session['name'] = user['username']
            session['id'] = user['id']
            flash(f'Login Successful {form.username.data}', 'success')
            conn.close()
            return redirect(url_for('index'))
        else:
            flash(f'Login Unsuccessful', 'danger')
            conn.close()
            return redirect(url_for('login'))
    return render_template('login.html', form=form, name="Log In")

@app.route('/librarian_login', methods=['GET', 'POST'])
def librarian_login():
    if session.get('name', ''):
        return redirect(url_for('index'))
    form = LogInForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.username.data != "Admin":
            flash(f'You are not a Librarian, Try User Login', 'danger')
            return redirect(url_for('librarian_login'))
        conn = get_db_connection()
        user = conn.execute(f"SELECT * FROM users where username = '{form.username.data}'").fetchone()
        if user and user['password'] == form.password.data:
            session['name'] = user['username']
            session['id'] = user['id']
            flash(f'Login Successful {form.username.data}', 'success')
            conn.close()
            return redirect(url_for('index'))
        else:
            flash(f'Login Unsuccessful', 'danger')
            conn.close()
            return redirect(url_for('librarian_login'))
    return render_template('librarian_login.html', form=form, name="Librarian Login")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['name'] = ''
    session['id'] = None
    return redirect(url_for('index'))

@app.route('/add_books', methods=['GET', 'POST'])
def add_books():
    if session.get('name', '') != 'Admin':
        return redirect(url_for('index'))
    form = BookForm(request.form)
    conn = get_db_connection()
    sections = conn.execute(f"SELECT * FROM section").fetchall()
    form.section.choices = [(section['name'], section['name']) for section in sections]
    if request.method == 'POST' and form.validate():
        query1 =  f"INSERT INTO books (name, author, description, price, content, section) VALUES ('{form.name.data}', '{form.author.data}', '{form.description.data}', {form.price.data}, '{form.content.data}', '{form.section.data}')"
        conn.execute(query1)
        conn.commit()
        conn.close()
        flash(f'Book Added {form.name.data}', 'success')
        return redirect(url_for('index'))
    return render_template('add_books.html', form=form, name="Add Book")

@app.route('/add_section', methods=['GET', 'POST'])
def add_section():
    if session.get('name', '') != 'Admin':
        return redirect(url_for('index'))
    conn = get_db_connection()
    form = SectionForm(request.form)
    if request.method == 'POST' and form.validate():
        section = conn.execute(f"SELECT * FROM section where name = '{form.name.data}'").fetchall()
        if section:
            flash(f'Section already exists {form.name.data}', 'danger')
            return redirect(url_for('add_section'))
        conn = get_db_connection()

        now = datetime.now()
        now_string = now.strftime("%m/%d/%Y")
        query1 =  f"INSERT INTO section (name, description, date) VALUES ('{form.name.data}', '{form.description.data}', '{now_string}')"
        conn.execute(query1)
        conn.commit()
        flash(f'Section Added {form.name.data}', 'success')
    sections = conn.execute(f'SELECT * FROM section').fetchall()    
    conn.close()
    return render_template('section.html', form=form, name="Add section", sections=sections)

@app.route('/edit_books/<int:id>', methods=['GET', 'POST'])
def edit_books(id):
    conn = get_db_connection()
    if session.get('name', '') != 'Admin':
        return redirect(url_for('index'))
    book = conn.execute(f"SELECT * FROM books where id = '{id}'").fetchone()    
    sections = conn.execute(f"SELECT * FROM section").fetchall()
    if not book:
        return redirect(url_for('index'))
    form = BookForm(request.form)
    form.section.choices = [(section['name'], section['name']) for section in sections]
    if request.method == 'POST' and form.validate():
        query1 =  f'UPDATE books SET name = "{form.name.data}", author = "{form.author.data}", description = "{form.description.data}", price = {form.price.data}, content = "{form.content.data}", section = "{form.section.data}" where id = {id}'
        conn.execute(query1)
        conn.commit()
        conn.close()
        flash(f'Book Edited {form.name.data}', 'success')
        return redirect(url_for('index'))
    else:
        form.name.data = book['name']
        form.author.data = book['author']
        form.description.data = book['description']
        form.price.data = book['price']
        form.content.data = book['content']
        form.section.data = book['section']
    return render_template('add_books.html', form=form, name="Edit Book")

@app.route('/view_books/<int:id>', methods=['GET', 'POST'])
def view_books(id):
    conn = get_db_connection()
    book = conn.execute(f"SELECT * FROM books where id = {id}").fetchone()
    form = ReviewForm(request.form)
    if request.method == 'POST' and form.validate():
        query1 =  f"INSERT INTO book_review (book_id, username, description) VALUES ('{id}', '{session.get('name')}', '{form.description.data}')"
        conn.execute(query1)
        conn.commit()
        flash(f'Review Added', 'success')
    if book:
        try:
            rented = conn.execute(f"SELECT COUNT(*) AS COUNT FROM book_rented WHERE user_id = {session.get('id', 1)} and book_id = {id};").fetchone()['count']
        except:
            rentent = 0
        reviews = conn.execute(f"SELECT * FROM book_review WHERE book_id = {id}").fetchall()
        conn.close()
        return render_template('book.html', book=book, rented = rented, reviews=reviews, form=form)
    conn.close()
    return redirect(url_for('index'))   

@app.route('/delete_books/<int:id>', methods=['GET', 'POST'])
def delete_books(id):
    if session.get('name', '') != 'Admin':
        return redirect(url_for('index'))
    conn = get_db_connection()
    book = conn.execute(f"SELECT * FROM books where id = {id}").fetchone()    
    if book:
        conn.execute(f"DELETE FROM books WHERE id = {id};")
        conn.commit()
        conn.close()
        flash(f'Book Deleted {book["name"]}', 'danger')
    return redirect(url_for('index'))

@app.route('/rent_books/<int:id>', methods=['GET', 'POST'])
def rent_books(id):
    if not session.get('id') and session.get('name') != 'Admin':
        return redirect(url_for('login'))
    else:
        conn = get_db_connection()
        count = conn.execute(f"SELECT COUNT(*) AS COUNT FROM book_rented WHERE user_id = {session.get('id', 0)};").fetchone()    
        if count['COUNT'] == 5:  
            flash(f"You can't rent more than 5 books", 'danger')
            return redirect(url_for('books'))
        book = conn.execute(f"SELECT * FROM books where id = {id} and rented = 0").fetchone()   
        if book:
            conn.execute(f"UPDATE books SET rented = 1 where id = {id}")
            now = datetime.now().strftime("%m/%d/%Y")
            return_date = datetime.now() + timedelta(days=2)
            return_date = return_date.strftime("%m/%d/%Y")
            conn.execute(f"UPDATE books SET date_issued = '{now}' where id = {id}")
            conn.execute(f"UPDATE books SET return_date = '{return_date}' where id = {id}")
            conn.execute(f"INSERT INTO book_rented (book_id, user_id) VALUES ({id}, {session.get('id', 0)});")
            conn.commit()
            conn.close()
            flash(f'Book Rented {book["name"]}', 'success')
        return redirect(url_for('books'))
    
@app.route('/return_books/<int:id>', methods=['GET', 'POST'])
def return_books(id):
    if not session.get('id') and session.get('name') != 'Admin':
        return redirect(url_for('login'))
    else:
        conn = get_db_connection()
        book = conn.execute(f"SELECT * FROM books where id = {id} and rented = 1").fetchone()   
        if book:
            conn.execute(f"UPDATE books SET rented = 0 where id = {id}")
            conn.execute(f"UPDATE books SET date_issued = '-' where id = {id}")
            conn.execute(f"UPDATE books SET return_date = '-' where id = {id}")
            conn.execute(f"Delete From book_rented where book_id = {id}")
            conn.commit()
            conn.close()
            flash(f'Book Returned {book["name"]}', 'success')
        return redirect(url_for('books'))

if __name__ == '__main__':
    app.run(debug=True)