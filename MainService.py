from MasterDataCollection import MasterDataCollection
from CorrelationFInder import CorrelationFinder
import json
class MainService:
	'''
	This is the main service that Supply Maven will run upon.
	Uses the data collected from Master Data Collection, as well as the 
	priceforecasting and correlations
	'''
	def __init__(self, data, names):
		print('Collecting data...')
		m = MasterDataCollection()
		m.collectAllBls()
		m.cleanData()
		m.collectAllQuandl()
		m.collectAllAlphaVantage()
		self.TimeSeries = m.MasterPrices
		# self.TimeSeries = data
		self.Ids = m.CodeToNames
		# self.Ids = names
		
		
		
		self.correlator = CorrelationFinder(self.TimeSeries)
		print('Correlator initialized.')
	def updateAllData(self):


		print('---'*25)
		print('Data Collection Succesful.')
		print('TimeSeries dictionary has ' + str(len(self.TimeSeries)) + ' entries.')
	def queryNames(self, word):
		'''
    	Returns set of names likely to be relevant to the user
    	'''
		adjustments = [word, word.lower(), word.lower() + 's', word.capitalize(), word.capitalize() + 's', word[:-1] + 'ing']
		names = self.Ids
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
	    names = self.Ids
	    for Id in names:
	        if names[Id] == series_title:
	            return Id

	def getNameFromId(self, Id):
		return self.Ids[Id]

	def findFiveHighestCorrelated(self, series_title):
    
	    #Find the id
	    Id = self.getIdFromName(series_title)
	    return self.correlator.best_correlations(Id)

	def plotTimeSeries(self, titles):
		x = 1


	def saveTimeSeriesToFile(self, filename):
		'''
		Once desired information is stored, save the master database to a file.
		'''
		with open(filename,"w") as f:
			json.dump(self.TimeSeries, f)


	def saveIdsToFile(self, filename):
		with open(filename, "w") as f:
			json.dump(self.Ids, f)
