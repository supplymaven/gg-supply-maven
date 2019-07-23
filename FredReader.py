import requests
import json

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
		response = requests.get(url)
		dataDict = json.loads(response.text)
		observations = dataDict['observations']
		for observation in observations:
			date = observation['date']
			newdate = date[5:7] + '/' + date[:4]
			value = float(observation['value'])
			series[newdate] = value
		self.allTimeSeries[Id] = series

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
		response = requests.get(url)
		dataDict = json.loads(response.text)
		return dataDict

f = FredReader()
# for i in range(100):
# 	print(i, f.getCategoryName(i))
# series = f.getSeriesForCategory(0)
# print(series)
# f.getCategoryName(32991)
series = f.getCategoryChildren()
print(series)


