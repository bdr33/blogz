from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(5000))

    def __init__(self, title, content):
        self.title = title
        self.content = content




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



if __name__ == '__main__':
    app.run()