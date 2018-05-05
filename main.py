from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi
import os
import jinja2

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


template_dir= os.path.join(os.path.dirname(__file__), 'templates')
jinja_env= jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


app = Flask(__name__)
app.config['DEBUG'] = True

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(5000))

    def __init__(self, title, content):
        self.title = title
        self.content = content


@app.route("/")
def index():
    template = jinja_env.get_template('base.html')
    return template.render()

@app.route("/blog")
def blog():
        all_posts = Blog.query.all()
        return render_template('base.html', page_title= "Blog Home Page", 
        page_header="Blogs:", all_posts=all_posts)

@app.route("/newpost")
def newpost():
    template = jinja_env.get_template('newpost.html')
    return template.render()

@app.route("/validate-post", methods=['POST','GET'])
def validate_post():

    title = request.form['title']
    content= request.form['content']
    
    title_error= ''
    content_error= ''
    
    if title=="":
        title_error = 'You must enter a title'
    else: 
        if len(title) > 120:
            title_error= 'Your title may not be more than 120 characters long'
        
        
    if content=="":
        content_error = 'You must enter content'
    else: 
        if len(content) > 5000:
            content_error= 'Your content may not be more than 5000 characters'
        
            
           

    if not title_error and not content_error:
        template = jinja_env.get_template('newpost.html')
        return redirect('/')

    else: 
        template = jinja_env.get_template('newpost.html')
        return template.render(title=title, content=content,title_error=title_error, 
        content_error=content_error)



if __name__ == '__main__':
    app.run()