import requests
import json
import time

class FredReader:

	def __init__(self):
		self.apikey = 'a8710650cf294cabadecccc427417d5b'
		self.allTimeSeries = {}
		self.allNames = {}

	def searchSeries(self, search_text):
		'''
		Searches for relevant series based on a text query
		returns list of matching Ids
		'''
		base = 'https://api.stlouisfed.org/fred/series/search?search_text='
		api_key = '&api_key=' + self.apikey
		file_type = '&file_type=json'
		url = base + search_text + api_key + file_type
		response = requests.get(url)
		dataDict = json.loads(response.text)
		Ids = []
		series = dataDict['seriess']
		for Dict in series:
		    title = Dict['title']
		    frequency = Dict['frequency_short']
		    Id = Dict['id']
		    if frequency == 'M':
		        Ids.append(Id)
		return Ids

	def storeTimeSeries(self, Id):
		'''
		returns time series for an Id
		'''
		series = {}
		base = 'https://api.stlouisfed.org/fred/series/observations?series_id='
		api_key = '&api_key=' + self.apikey
		file_type = '&file_type=json'
		frequency = '&frequency=m'
		url = base + Id + api_key + file_type + frequency
		TRY = True
		while TRY:
			response = requests.get(url)
			if response.status_code == 200:
				TRY = False
			elif response.status_code == 429:
				time.sleep(.5)
			else:
				TRY = False
				print('could not store Id: ' + str(Id) + ' error code ' + str(response.status_code))
				raise KeyError
		dataDict = json.loads(response.text)
		observations = dataDict['observations']
		for observation in observations:
			date = observation['date']
			newdate = date[5:7] + '/' + date[:4]
			value = float(observation['value'])
			series[newdate] = value
		self.allTimeSeries[Id] = series

	def storeName(self, Id, name):
		self.allNames[Id] = name

	def getCategoryName(self, categoryId):
		base = 'https://api.stlouisfed.org/fred/category?category_id='
		api_key = '&api_key=' + self.apikey
		file_type = '&file_type=json'
		url = base + str(categoryId) + api_key + file_type
		response = requests.get(url)
		dataDict = json.loads(response.text)
		return dataDict['categories'][0]['name']


	def getCategoryChildren(self, categoryId):
		base = 'https://api.stlouisfed.org/fred/category/children?category_id='
		api_key = '&api_key=' + self.apikey
		file_type = '&file_type=json'
		url = base + str(categoryId) + api_key + file_type
		response = requests.get(url)
		dataDict = json.loads(response.text)
		categories = dataDict['categories']
		children = []
		for category in categories:
			Id = category['id']
			name = category['name']
			parent_id = category['parent_id']
			children.append((Id, name))
		return children

	def getSeriesForCategory(self, categoryId):
		base = 'https://api.stlouisfed.org/fred/category/series?category_id='
		api_key = '&api_key=' + self.apikey
		file_type = '&file_type=json'
		url = base + str(categoryId) + api_key + file_type
		TRY = True
		while TRY:
			counter = 0
			time.sleep(.5)
			print('trying to get series for category: ' + str(categoryId))
			try:
				response = requests.get(url)
				print(response)
				dataDict = json.loads(response.text)
				return dataDict['seriess']
			except:
				TRY = True
				counter +=	1
				if counter > 10:
					TRY = False
		return []


	def storeDesiredSeries(self):
		'''
		stores all the series that should be stored from the FRED database
		'''
		for category in [2, 104, 12,11]:
			children = self.getCategoryChildren(category)
		for cat in [33509, 33731]:
			children.append((cat, None))
		for category2 in children:
			seriess = self.getSeriesForCategory(category2[0])
			for series in seriess:
				frequency = series['frequency']
				if frequency == 'Monthly':
					Id = series['id']
					name = series['title']
					self.storeName(Id,name)
		print('FRED names stored.')

	def storeAllObservations(self):
		'''
		store all desired names to a master observations dictionary
		'''
		time.sleep(3)
		print('storing all observations')
		for Id in self.allNames:
			name = self.allNames[Id]
			try:
				self.storeTimeSeries(Id)
			except:
				print('could not store Id: ' + Id)
		print('FRED observations stored.')
			
	def saveNamesToJson(self,filename):
		with open(filename, "w") as f:
			json.dump(self.allNames, f)
							



