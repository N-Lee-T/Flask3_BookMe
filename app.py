from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# To do: Search for how to do this with MongoDB, MySQL 
# Note - '///' is relative path; '////' would be absolute 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# Initialize the database 
db = SQLAlchemy(app)

basic_time = datetime.now()
the_date = basic_time.strftime("%m/%d/%Y")

# Define the schema through a Python class. Start a python3 shell in terminal & run 'from app import db' then 'db.create_all()' to create 
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(250), nullable=False)
    initials = db.Column(db.String(3), nullable=False)
    genre = db.Column(db.String(200), nullable=True)
    date = db.Column(db.String(100), default=the_date)

    def __repr__(self):
        # To do: research this syntax 
        return '<Books %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        book_title = request.form['title']
        book_author = request.form['author']
        book_genre = request.form['genre']
        inits = request.form['initials']
        new_book = Books(title=book_title, author=book_author, initials=inits, genre=book_genre) 

        # Add to the DB    
        try:
            db.session.add(new_book)
            db.session.commit()
            return redirect('/')
        except:
            return 'Looks like that did not work'

    else:
        books = Books.query.order_by(Books.date).all()
        # Otherwise, just show the page 
        return render_template('index.html', books=books)

@app.route('/delete/<int:id>')
def delete(id):
    book_to_delete = Books.query.get_or_404(id)

    try:
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return "did not delete :( "

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    book = Books.query.get_or_404(id)

    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.initials= request.form['initials']

        try:
            db.session.commit()
            return redirect('/')

        except:
            return "did not work :("

    else:
        return render_template('edit.html', book=book)


if __name__=='__main__':
    app.run(debug=True)