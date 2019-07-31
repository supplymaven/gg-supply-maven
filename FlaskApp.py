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

m = MainService()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')
 
@app.route('/search', methods=["GET", "POST"])
def search():
	response = {}
	if request.form:
		query = request.form.get('Search Names')
		results = m.querySqlNames(query)
		for tup in results:
			response[tup[0]] = tup[1]
	return render_template('search.html', nameDict = response)

@app.route('/historical_graph<Id>')
def historical_graph(Id):
	data = m.getHistoricalData(Id)
	return render_template('historical_graph.html', graph_data = data)

	# return render_template('historical_graph.html', graph_data = data)
	


if __name__ == '__main__':
	app.run(debug=True)

