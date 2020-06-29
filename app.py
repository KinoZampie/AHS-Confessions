from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main.db"
db = SQLAlchemy(app)

class Confessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(1500), nullable=False)
    dateCreated = db.Column(db.String(100),nullable=False, default=datetime.now().strftime('%B %d, %Y %I:%M%p'))

@app.route("/", methods=["GET","POST"])
@app.route("/index", methods=["GET","POST"])
def index():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        if title == "" or description == "":
            return redirect("/")
        elif len(title) > 250 or len(description) > 1500:
            return "Failed to create post <br> Maximum title length is 250 characters, maximum description length is 1500 characters <br>Lol no need to write an essay"
        try:
            newPost = Confessions(title=title, description=description)
            db.session.add(newPost)
            db.session.commit()
            return redirect("/")
        except:
            return "Failed to create a post :/ Idk why... <br>Try again later or just do your homework or smthing lol"
    else:
        page = request.args.get('page', 1, type=int)
        posts = Confessions.query.order_by(Confessions.id.desc()).paginate(page=page,per_page=5)
        print(datetime.now().strftime('%B %d, %Y %I:%M%p'))
        return render_template("index.html", posts=posts)

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
