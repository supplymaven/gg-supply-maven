from flask import Flask, escape, request, render_template
from flask_sqlalchemy import SQLAlchemy
from MainService import MainService
from flask import request

app = Flask(__name__)

# db = SQLAlchemy(app)
# engine = db.create_engine('mysql://JJCJ3FtEYC:x8g8zouU4u@remotemysql.com/JJCJ3FtEYC')
# connection = engine.connect()
# metadata = db.MetaData()
# Observations = db.Table('Observations', metadata, autoload = True, autoload_with = engine)
# Names = db.Table('Names', metadata, autoload = True, autoload_with = engine)

# print(Observations.columns.keys())



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')
 
@app.route('/search', methods=["GET", "POST"])
def search():
	if request.form:
		m = MainService()
		db, cursor = m.connectToSqlServer()
		query = request.form.get('Search Names')
		return query

	return render_template('search.html')


if __name__ == '__main__':
	app.run(debug=True)