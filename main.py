from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
import cgi
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:launchcode@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key='1234'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(5000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, content, owner):
        self.title = title
        self.content = content
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(25), unique=True)
    password = db.Column(db.String(25))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route("/")
def index():
    users= User.query.all()
    return render_template('index.html', users=users)

@app.route("/blog")
def blog():
    ind_id = request.args.get('id')
    user_id= request.args.get('userid')

    if ind_id:
        blog=Blog.query.get(ind_id)
        return render_template('ind_entry.html',blog=blog)

    if user_id:
        user_posts = BLog.query.filter_by(owner_id=user_id).all()
        return render_template('singleUser.html', user_posts=user_posts)    

    blogs=Blog.query.all()
    return render_template('bloghome.html',blogs=blogs, page_header='Build a Blog')

@app.route("/newpost")
def newpost():
    return render_template('newpost.html')

@app.route("/validate-post", methods=['POST'])
def validate_post():

    title = request.form['title']
    content= request.form['content']
    
    title_error= ''
    content_error= ''
    
    if title=="":
        title_error = 'Please fill in the title'
    else: 
        if len(title) > 120:
            title_error= 'Your title may not be more than 120 characters long'
          
    if content=="":
        content_error = 'Please fill in the content'
    else: 
        if len(content) > 5000:
            content_error= 'Your content may not be more than 5000 characters'     
           
    if not title_error and not content_error:
        owner=User.query.filter_by(username=session['username']).first()
        new_blog= Blog(title,content, owner=owner)
        db.session.add(new_blog)
        db.session.commit()
        new_page="/blog?id=" + str(new_blog.id)
        return redirect(new_page)

    else: 
        return render_template('newpost.html',title=title, content=content,title_error=title_error, 
        content_error=content_error)

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session ['username'] = username
            return redirect ("/newpost")

        else:
            login_error = 'Username or password is incorrect'
            return render_template('login.html', username=username, password="",login_error=login_error)            
    return render_template('login.html')
    

@app.route("/signup", methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username= request.form['username']
        password= request.form['password']
        password_ver= request.form['password_ver']
        username_error= ''
        taken_error= ''
        password_error= ''
        password_ver_error=''

        if username=="":
            username_error = 'You must enter a username'
        else: 
            if len(username) <3 or len(username) >24:
                username_error= 'Your username must be between 3 and 25 characters long'

        taken= User.query.filter_by(username=username).first()
        if taken:
            taken_error= 'Username is already taken'
                    
        if password=="":
            password_error = 'You must enter a password'
        else: 
            if len(password) <3 or len(password)>24:
                password_error= 'Your password must be between 3 and 25 characters long'
                        
        if password_ver == "" or password_ver != password:
            password_ver_error = "Passwords don't match"     

        if not username_error and not taken_error and not password_error and not password_ver_error:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session ['username'] = username
            return redirect ("/newpost")

        else: 
            return render_template("signup.html", username='', password='', 
            password_ver='', username_error=username_error, taken_error=taken_error, password_error=password_error,
            password_ver_error=password_ver_error)
    
    return render_template('signup.html')

@app.route("/logout")
def logout():
    del session['username']
    return redirect('/blog')


if __name__ == '__main__':
    app.run()