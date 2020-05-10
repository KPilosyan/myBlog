from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/User/Desktop/blog/blog.db'
db = SQLAlchemy(app)

class blogPost(db.Model):
    __tablename__ = 'blogpost'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
def index():
    posts = blogPost.query.order_by(blogPost.date_posted.desc()).all()
    return render_template("index.html", posts=posts)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/post/<int:post_id>')
def post(post_id):
    post = blogPost.query.filter_by(id=post_id).one()

    return render_template("post.html", post=post)

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/add')
def add():
    return render_template("add.html")

@app.route('/addpost', methods=["POST"])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = blogPost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())
    
    db.session.add(post)
    db.session.commit()

    return redirect(url_for("index"))

