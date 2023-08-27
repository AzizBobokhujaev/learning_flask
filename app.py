from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Article'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route("/posts")
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)


@app.route(f"/posts/<int:id>")
def post_detail(id):
    article = Article.query.get(id)
    return render_template('detail.html', article=article)


@app.route(f"/posts/<int:id>/delete")
def post_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/posts")
    except:
        return "Ошибка при удалении"


@app.route(f"/posts/<int:id>/update", methods=['POST', 'GET'])
def article_update(id):
    articel = Article.query.get(id)
    if request.method == "POST":
        articel.title = request.form['title']
        articel.intro = request.form['intro']
        articel.text = request.form['text']

        try:
            db.session.commit()
            return redirect("/posts")
        except:
            return "При обновление возникла ошибка"
    else:
        return render_template("update-article.html", article=articel)


@app.route('/article', methods=['POST', 'GET'])
def article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect("/posts")
        except:
            return "при добавление возникла ошибка"
    else:
        return render_template("article.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
