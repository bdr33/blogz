from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(5000))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/', methods=['GET'])
def index():
    return redirect('/blog')

@app.route('/blog', methods=['GET'])
def home_page():
    if request.args.get('id'):
        post_id = request.args.get('id')
        post_content = Blog.query.get(post_id)
        return render_template('newpost.html', page_title= "Blog Home Page", page_header="New Entry", post_content=post_content)
    else:
        all_posts = Blog.query.all()
        return render_template('blog.html', page_title= "Blog Home Page", page_header="Blogs:", all_posts=all_posts)


    

@app.route('/newpost', methods= ['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        title_error= ''
        body_error= ''

        if len(title)==0:
            title_error= "You must submit a title"
        if len(body)==0:
            body_error= "You must submit content"
        if len(title)>120:
            title_error= "Title max is 120 characters"
        if len(body)>5000:
            body_error= "Content max is 5000 characters"
        if title_error or body_error: 
            return render_template('blog.html', page_title= "New Post", page_header= "New Post", title_error= title_error, body_error=body_error)
        
        else: 
            new_post= Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog')
        
        

if __name__ == '__main__':
    app.run()