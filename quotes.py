from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:010123@localhost/quotes"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class FavQuote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30), nullable=False)
    quote = db.Column(db.String(2000), nullable=False)

    def __repr__(self):
        return f"<FavQuote {self.author}>"

with app.app_context():
    db.create_all()

@app.route('/')
def index():
	result = FavQuote.query.all()
	return render_template('index.html',result=result)


@app.route('/quotes')
def quotes():
	 return render_template('quotes.html')

@app.route('/process', methods =['POST'])
def process():
	author = request.form['author']
	quote = request.form['quote']
	quotedata =FavQuote(author=author,quote=quote)
	db.session.add(quotedata)
	db.session.commit()

	return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)