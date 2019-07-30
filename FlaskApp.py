from flask import Flask, escape, request, render_template
import pymysql
from MainService import MainService

app = Flask(__name__)

db = pymysql.connect("sql9.freemysqlhosting.net", "sql9300254", "tlXYYYFzAF", "sql9300254")
cursor = db.cursor()

def updateSqlDB():
	
	#DELETE OLD OBSERVATION TABLE IF IT EXISTS
	try:
		cursor.execute('DROP TABLE Observations;')
	except:
		print("Observation table doesn't exist")
	cursor.execute('CREATE TABLE Observations (ID VARCHAR(255), MONTH VARCHAR(255), VALUE VARCHAR(255) );')
	try:
		cursor.execute('DROP TABLE Names;')
	except:
		print("Observation table doesn't exist")
	cursor.execute('CREATE TABLE Names (ID VARCHAR(255), TITLE VARCHAR(255));')
	
	m = MainService()
	m.makeSmallDatabase()
	
	name_data = []
	for Id in m.MasterData.CodeToNames:
		title = m.MasterData.CodeToNames[Id]
		name_data.append((Id,title))
	sql = "INSERT INTO Names (ID, TITLE) VALUES (%s,%s)"
	cursor.executemany(sql, name_data)
	
	observation_data = []
	for Id in m.MasterData.MasterPrices:
		prices = m.MasterData.MasterPrices[Id]
		for date in prices:
			value = prices[date]
			observation_data.append((Id,date,value))

	sql = "INSERT INTO Observations (ID, MONTH, VALUE) VALUES (%s,%s,%s)"
	cursor.executemany(sql, observation_data)
	db.commit()





updateSqlDB()

# m = MainService()
# m.mockUpdateAllData()

# @app.route('/')
# def home():
#     return render_template('home.html')

# @app.route('/about')
# def about():
# 	return render_template('about.html')
 
# @app.route('/search')
# def search():
# 	return render_template('search.html')



# if __name__ == '__main__':
# 	app.run(debug=True)