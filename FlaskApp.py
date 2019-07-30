from flask import Flask, escape, request, render_template
import pymysql
from MainService import MainService

app = Flask(__name__)

m = MainService()
m.makeSmallDatabase()
m.updateSqlDB()
db, cursor = m.connectToSqlServer()

@app.route('/')
def home():
    return render_template('home.html', l = )

@app.route('/about')
def about():
	return render_template('about.html')
 
@app.route('/search')
def search():
	return render_template('search.html')



if __name__ == '__main__':
	app.run(debug=True)