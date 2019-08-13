from flask import Flask, escape, request, render_template
from MainService import MainService
from flask import request
import pygal


app = Flask(__name__)

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
	dates, values = m.getHistoricalData(Id)
	graph = pygal.Line()
	graph.title = 'Value of ' + Id + ' Over Time'
	graph.x_labels = dates
	graph.add(Id, values)
	data = graph.render_data_uri()
	return render_template('historical_graph.html', graph_data = data)

	# return render_template('historical_graph.html', graph_data = data)

@app.route('/highest_correlationsID=<Id>')
def highest_correlations(Id):
	'''
	For an Id return a graph showing the best correlations
	'''
	db, cursor = m.connectToSqlServer()
	graph, Ids, vals = m.plotForFlaskCorrelations(Id, db = db, cursor = cursor)
	titles = []
	for i in Ids:
		titles.append(m.getNameFromIdSql(i, db = db, cursor = cursor))
	Title = m.getNameFromIdSql(Id)
	return render_template('highest_correlation.html', graph_data = graph.render_data_uri(), 
		Ids = Ids, Vals = vals, Titles = titles, Id = Id, Title = Title)

if __name__ == '__main__':
	app.run(debug=True)

