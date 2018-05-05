from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:launchcode@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(5000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author

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
    return redirect("/blog")

@app.route("/blog")
def blog():
    if request.args.get('id'):
        ind_id = request.args.get('id')
        blog=Blog.query.get(ind_id)
        return render_template('ind_entry.html',blog=blog)
    
    else:
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
        if request.method=='POST':
            new_blog= Blog(title,content)
            db.session.add(new_blog)
            db.session.commit()
            new_page="/blog?id=" + str(new_blog.id)
        return redirect(new_page)

    else: 
        return render_template('newpost.html',title=title, content=content,title_error=title_error, 
        content_error=content_error)

@app.route("/login", methods = ['POST', 'GET'])
def login():
    return render_template('login.html')

def validate_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form ['password']
        #clarify this
        user = User.query.filter_by(username=username).first()
        users = User.query.all()

        if user not in users: 
            username_error = 'User does not exist'

        if user.password != password:
            password_error = 'Password is incorrect'
        
        if not username_error and not password_error:
            session['username'] = username
            return redirect ('/newpost')
        else:
            return render_template('login.html', username_error=username_error, password_error=password_error)

@app.route("/signup", methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username= request.form['username']
        password= request.form['password']
        password_ver= request.form['password_ver']

        username_error= ''
        password_error= ''
        password_ver_error=''

    if user_name=="":
        user_name_error = 'You must enter a username'
    else: 
        if len(user_name) <3 or len(user_name) >20:
            user_name_error= 'Your username must be between 3 and 20 characters long'
        else: 
            if " " in user_name:
                user_name_error= 'Your username cannot contain any spaces'

        
    if password=="":
        password_error = 'You must enter a password'
    else: 
        if len(password) <3 or len(password)>20:
            password_error= 'Your password must be between 3 and 20 characters long'
        else: 
            if " " in password: 
                password_error= 'Your password cannot contain any spaces'
            
    if password_ver == "" or password_ver != password:
        password_ver_error = "Passwords don't match"
    
    if email !="":
        if len(email) <3 or len(email)>20 or " " in email: 
            email_error='Please enter a valid email'
        else: 
            if email.count('@') != 1 or email.count('.') !=1:
                email_error='Please enter a valid email'
        

    if not user_name_error and not password_error and not password_ver_error and not email_error:
        template = jinja_env.get_template('welcome.html')
        return template.render(user_name=user_name)

    else: 
        template = jinja_env.get_template('index_form.html')
        return template.render(user_name=user_name, password='', 
        password_ver='', email=email, user_name_error=user_name_error, password_error=password_error,
         password_ver_error=password_ver_error, email_error=email_error)


if __name__ == '__main__':
    app.run()