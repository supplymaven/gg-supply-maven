from MasterDataCollection import MasterDataCollection
from CorrelationFinder import CorrelationFinder
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import pymysql
import matplotlib.pyplot as plt
import datetime
import csv
import json
import pygal

class MainService:
	'''
	This is the main service that Supply Maven will run upon.
	Uses the data collected from Master Data Collection, as well as the 
	priceforecasting and correlations
	'''
	def __init__(self):
		'''
		Initialize MainService with a MasterDataCollection object and
		the correlator object set to None. It will be instantiated when the data
		is updated.
		'''
		self.MasterData = MasterDataCollection()
		self.correlator = CorrelationFinder(None)
	
	def updateAllData(self):
		'''
		replaces all data with their new timeseries values and initializes 
		the correlator with that data.
		'''
		print('Updating all data...')
		self.MasterData.collectAllBls()
		self.MasterData.collectAllFred()
		self.MasterData.cleanData()
		self.MasterData.collectAllQuandl()
		self.MasterData.collectAllAlphaVantage()
		print('---'*25)
		print('Data Collection Succesful.')
		print('TimeSeries dictionary has ' + str(len(self.MasterData.MasterPrices)) + ' entries.')
		print('Initializing correlator with updated data')
		self.correlator = CorrelationFinder(self.MasterData.MasterPrices)
	
	def mockUpdateAllData(self):
		'''
		For testing, reads from constant files
		'''
		with open('testingdata/MOCKallcleandata.json','r') as f: 
		    data = f.read()
		    allCleanData = json.loads(data)
		with open('testingdata/MOCKallcleannames.json','r') as f:
		    data = f.read()
		    allCleanNames = json.loads(data)
		print('Getting Mock data...')
		self.MasterData.MasterPrices = allCleanData
		self.MasterData.CodeToNames = allCleanNames
		print('---'*25)
		print('Data Collection Succesful.')
		print('TimeSeries dictionary has ' + str(len(self.MasterData.MasterPrices)) + ' entries.')
		print('Initializing correlator with updated data')
		self.correlator = CorrelationFinder(self.MasterData.MasterPrices)

	def makeSmallDatabase(self):
		print('Making Small Database...')
		self.MasterData.collectBls(['ei'])
		self.MasterData.cleanData()
		self.MasterData.collectAllQuandl()
		self.MasterData.collectAllAlphaVantage()
		self.correlator = CorrelationFinder(self.MasterData.MasterPrices)

	def querySqlNames(self, word):
		'''
		Given a string argument, this queries the sql database for titles containing the given text.
		Returns a set of tuples with ID in index 0 and title in index 1
		'''
		if len(word) > 5:
			adjustments = [word, word.lower(), word.lower() + 's', word.capitalize(), word.capitalize() + 's', word[:-1] + 'ing', word[:-1]]
		else:
			adjustments = [word, word.lower(), word.lower() + 's', word.capitalize(), word.capitalize() + 's', word[:-1] + 'ing']
		db, cursor = self.connectToSqlServer()
		query = "SELECT * FROM Names WHERE TITLE LIKE %s;"
		final = set()
		adjs = []
		for adjustment in adjustments:
			search = '%' + adjustment + '%'
			cursor.execute(query, search)
			matches = set(cursor.fetchall())
			final.update(matches)
		return final

	def getHistoricalData(self, Id, cursor = None, db = None):
		if cursor == None:
			db, cursor = self.connectToSqlServer()
		cursor.execute("SELECT MONTH, VALUE FROM Observations WHERE ID = %s", Id)
		results = cursor.fetchall()
		dates = []
		values = []
		for tup in results:
			dates.append(tup[0])
			values.append(float(tup[1]))
		return dates, values

	def getHighestCorrelatedIds(self, Id, db = None, cursor = None):
		if cursor == None:
			db, cursor = self.connectToSqlServer()
		cursor.execute("SELECT * FROM HighestCorrelations WHERE Id = %s", Id)
		result = cursor.fetchall()
		return result

	def queryNames(self, word):
		'''
    	Returns set of names likely to be relevant to the user
    	'''
		adjustments = [word, word.lower(), word.lower() + 's', word.capitalize(), word.capitalize() + 's', word[:-1] + 'ing']
		names = self.MasterData.CodeToNames
		matches = set()
		for Id in names:
			words = names[Id].split()
			for adjustment in adjustments:
				if adjustment in words:
					matches.add(names[Id])
					break
				else:
					for word in words:
						if adjustment in word:
							matches.add(names[Id])
							break
		return matches

	def getIdFromName(self, series_title):
	    '''
	    FOR USE BY SUPPLY MAVEN SYSTEM
	    Returns Id for a given series title
	    '''
	    names = self.MasterData.CodeToNames
	    for Id in names:
	        if names[Id] == series_title:
	            return Id

	def getNameFromId(self, Id):
		return self.MasterData.CodeToNames[Id]

	def getNameFromIdSql(self, Id, db = None, cursor = None):
		if cursor == None:
			db,cursor = self.connectToSqlServer()
		cursor.execute("SELECT TITLE FROM Names WHERE ID = %s", Id)
		return cursor.fetchone()[0]


	def findFiveHighestCorrelatedSql(self, Id, varied_ind = False):
		db, cursor = self.connectToSqlServer()
		self.correlator.getSqlData(cursor)
		return self.correlator.best_correlations(Id, varied_ind)

	def findFiveHighestCorrelated(self, Id, varied_ind = False):
	    '''
	    Finds the five highest correlated assets and returns them in a list of tuples
	    with Id in index 0 and correlation value in index 1
	    '''
	    return self.correlator.best_correlations(Id, varied_ind)

	def plotTimeSeries(self, Ids, plot = True):
		'''
		Given a list of series_IDs, this function will plot their time series
		on a time graph. If plot specified False, will return just the plot object
		and not show the graph
		'''
		for Id in Ids:
			x = list(self.MasterData.MasterPrices[Id].keys())
			newx = []
			for date in x:
				newx.append(self.convertToDateTime(date))
			y = list(self.MasterData.MasterPrices[Id].values())
			plt.plot_date(newx,y, linestyle = 'solid', marker = None, 
				label = self.getNameFromId(Id))
		if plot:
			plt.legend(loc = 'upper left')
			plt.show()
		else:
			return plt

	def plotForFlaskCorrelations(self, Id, db = None, cursor = None):
		if cursor == None:
			db, cursor = self.connectToSqlServer()
		corrInfo = list(self.getHighestCorrelatedIds(Id, db = db, cursor = cursor)[0])
		graphData= []
		Ids = []
		vals = []
		for i in range(len(corrInfo)):
		    if i in [0,1,3,5,7,9]:
		        Ids.append(corrInfo[i])
		    else:
		        vals.append(corrInfo[i])
		graph = pygal.DateLine(x_label_rotation=35, legend_at_bottom = True)
		graph.title = 'Highest TimeSeries Correlations with Id ' + Id
		for Id in Ids:
			d, values = self.getHistoricalData(Id, db = db, cursor = cursor)
			dates = []
			for date in d:
				dates.append(self.convertToDateTime(date))
			to_add = []
			for i in range(len(dates)):
				to_add.append((dates[i], values[i]))
			graph.add(Id, to_add)
		return graph, Ids[1:], vals

	def convertToDateTime(self, stringDate):
		'''
		Returns DateTime version of a stringDate
		'''
		newmonth = int(stringDate[:2])
		newyear = int(stringDate[3:])
		newday = 1
		newdate = datetime.date(year = newyear, month = newmonth, day = newday)
		return newdate

	def getDate(self):
		'''
		return utc time and date
		'''
		return datetime.datetime.today()
	
	def updateMonthlyData(self):
		raise NotImplementedError

	def saveTimeSeriesToFile(self, filename):
		'''
		Once desired information is stored, save the master database to a file.
		'''
		with open(filename,"w") as f:
			json.dump(self.MasterData.MasterPrices, f)

	def saveIdsToFile(self, filename):
		with open(filename, "w") as f:
			json.dump(self.MasterData.CodeToNames, f)

	def saveTimeSeriesToCsv(self, filename = None):
		'''
		once desired information is stored, given a filename save the master database to a CSV file.
		'''
		prices = self.MasterData.MasterPrices
		date = str(self.getDate())[5:10]
		if filename == None:
			filename = "CSV_data/EntireDatabase" + "-" + date + ".csv"
		csv_columns = ['Series Id', 'Date', 'Value']
		with open(filename, "w") as csvfile:
		    writer = csv.DictWriter(csvfile, fieldnames = csv_columns)
		    writer.writeheader()
		    for Id in prices:
		        timeseries = prices[Id]
		        for date in timeseries:
		            rowDict = {}
		            rowDict['Series Id'] = Id
		            rowDict['Date'] = date
		            rowDict['Value'] = timeseries[date]
		            writer.writerow(rowDict)
		        #NEED TO SEND TO SQL FILE
	
	def saveNameDictToCsv(self, filename = None):
		names = self.MasterData.CodeToNames
		date = str(self.getDate())[5:10]
		if filename == None:
			filename = "CSV_data/EntireNameDatabase" + "-" + date + ".csv"
		csv_columns = ['Series Id', 'Series Title']
		with open(filename, "w") as csvfile:
		    writer = csv.DictWriter(csvfile, fieldnames = csv_columns)
		    writer.writeheader()
		    for Id in names:
		    	rowDict = {}
		    	rowDict['Series Id'] = Id
		    	rowDict['Series Title'] = names[Id]
		    	writer.writerow(rowDict)
	
	def connectToSqlServer(self):
		host = "127.0.0.1"
		username = "ggordon"
		password = "BL$138575"
		database = "SM_Data"
		db = pymysql.connect(host, username, password, database)
		print('Succesful SQL connection.')
		cursor = db.cursor()
		return (db, cursor)

	def createTable(self, name, columns):
		'''
		Creates a table in SQL given a table namd and list of column titles
		'''
		try:
			db,cursor = self.connectToSqlServer()
		except:
			raise ConnectionRefusedError("CONNECTION FAILED. CHECK SSH SOCKET IS OPEN")
		cols = ' ('
		for col in columns:
			add = ' ' + col + ' VARCHAR(255),'
			cols += add
		cols = cols[:-1]
		cols += ')'
		sql = 'CREATE TABLE '  + name + cols + ';'
		cursor.execute(sql)
		db.commit()

	def insertIntoTable(self, name, columns, values):
		'''
		given name of table, name of columns, and values, this writes an insert into command
		'''
		vals = '('
		for val in values:
			vals += '%s,'
		vals = vals[:-1]
		vals += ')'
		cols = '('
		for col in columns:
			cols += col + ','
		cols = cols[:-1]
		cols += ')'
		command = 'INSERT INTO ' + name + ' ' + cols + ' VALUES ' +  vals + ';'
		return command
		

	def dropTable(self, name):
		'''
		given the name of a current table, drops that table.
		'''
		try:
			db,cursor = self.connectToSqlServer()
		except:
			raise ConnectionRefusedError("CONNECTION FAILED. CHECK SSH SOCKET IS OPEN")
		command = "DROP TABLE IF EXISTS " + name + ";"
		cursor.execute(command)
		db.commit()
		
	def updateSqlDB(self):
		try:
			db, cursor = self.connectToSqlServer()
		except:
			raise ConnectionRefusedError("CONNECTION FAILED. CHECK SSH SOCKET IS OPEN")
		#DELETE OLD TABLES IF THEY EXIST
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
		name_data = []
		for Id in self.MasterData.CodeToNames:
			title = self.MasterData.CodeToNames[Id]
			name_data.append((Id,title))
		sql = "INSERT INTO Names (ID, TITLE) VALUES (%s,%s)"
		cursor.executemany(sql, name_data)
		
		observation_data = []
		for Id in self.MasterData.MasterPrices:
			prices = self.MasterData.MasterPrices[Id]
			for date in prices:
				value = prices[date]
				observation_data.append((Id,date,value))

		sql = "INSERT INTO Observations (ID, MONTH, VALUE) VALUES (%s,%s,%s)"
		cursor.executemany(sql, observation_data)
		db.commit()
		print('SQL Database Successfully Updated.')


	def linearRegress(self, Id, plot = False):
		'''
		Calculates and returns intercept and coefficient as a tuple
		with intercept in index 0 and coeff in the other. Provides option
		to plot.
		'''
		prices = self.MasterData.MasterPrices
		series = prices[Id]
		months = []
		values = []
		datetimes = []
		x = []
		d = 0
		continuous = self.MasterData.isContinuous(Id)
		if continuous == 'Continuous':
			for date in list(series.keys()):
				months.append([d])
				datetimes.append(self.convertToDateTime(date))
				values.append(series[date])
				d += 1
		#Not continuous and we have to truncate data to last date
		else:
			append = False
			for date in list(series.keys()):
				if date == continuous:
					append = True
				if append:
					months.append([d])
					datetimes.append(self.convertToDateTime(date))
					values.append(series[date])
					d += 1
		model = LinearRegression()
		model.fit(months, values)
		x = np.array(range(len(datetimes)))
		y = model.intercept_ + model.coef_*x
		if plot:
			plot = self.plotTimeSeries([Id], False)
			plot.plot_date(datetimes,list(y), linestyle = 'solid', marker = None,
				label = 'Linear Regression Line')
			plot.legend(loc = 'upper left')
			plot.show()
		return (model.intercept_, model.coef_[0])
