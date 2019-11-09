from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:beproductive@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route("/")
def index():
	return redirect('/blog')

@app.route("/blog")
def display_blog():
	return render_template("blog.html")


@app.route("/newpost")
def newpost():
	return render_template("newpost.html", heading="Add a Blog Entry")


@app.route('/newpost', methods=['POST'])
def new_post():
	""" New post"""

	if request.method == 'POST':
		blog_title = request.form['blog-title']
		blog_body = request.form['blog-body']
		title_error = ""
		body_error = ""
		
		

		if not blog_title:
			title_error = "Please enter a title"
		if not blog_body:
			body_error = "Please enter a blog entry"


		if not title_error and not body_error:
			new_post = Blog(blog_title, blog_body)
			db.session.add(new_post)
			db.session.commit()
			return redirect("/blog")
		else:
			return render_template("newpost.html", title="New Entry", title_error=title_error, body_error=body_error, blog_title=blog_title, blog_body=blog_body)
	return render_template("newpost.html", title="New Entry")




if __name__ == '__main__':
	app.run()