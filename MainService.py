from MasterDataCollection import MasterDataCollection
from CorrelationFinder import CorrelationFinder
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
import datetime
import json

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
		self.correlator = None
	
	def updateAllData(self):
		'''
		replaces all data with their new timeseries values and initializes 
		the correlator with that data.
		'''
		print('Updating all data...')
		self.MasterData.collectAllBls()
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

	def findFiveHighestCorrelated(self, series_title, varied_ind = False):
	    '''
	    Finds the five highest correlated assets and returns them in a list of tuples
	    with Id in index 0 and correlation value in index 1
	    '''
	    Id = self.getIdFromName(series_title)
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

	def convertToDateTime(self, stringDate):
		'''
		Returns DateTime version of a stringDate
		'''
		newmonth = int(stringDate[:2])
		newyear = int(stringDate[3:])
		newday = 1
		newdate = datetime.date(year = newyear, month = newmonth, day = newday)
		return newdate


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
