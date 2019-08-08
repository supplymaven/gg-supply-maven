from flask import Flask, escape, request, render_template
from MainService import MainService
from flask import request


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
	data = m.getHistoricalData(Id)
	return render_template('historical_graph.html', graph_data = data)

	# return render_template('historical_graph.html', graph_data = data)

@app.route('/highest_correlations<Id>')
def highest_correlations(Id):
	return Id
	


if __name__ == '__main__':
	app.run(debug=True)

