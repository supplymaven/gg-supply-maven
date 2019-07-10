import requests
import json

class AlphaVantageReader:

	def __init__(self):
		self.apiKey = 'D3V05J5VFISOLEIH'
		self.SupplyMavenSymbols = {}
		self.MasterAVNamesSM = {'DJI': 'Dow Jones Industrial Average', '^GSPC':'S&P 500'}

	def getEquity(self, symbol, frequency):
		'''
		Given the symbol for an equity and the freqeuncy desired, this 
		function returns a price dictionary for that equity.
		'''
		baseUrl = 'https://www.alphavantage.co/query?'
		url = baseUrl + 'function=' + frequency + '&' + 'symbol=' + symbol + '&apikey=' + self.apiKey
		response = requests.get(url)
		dataDict = json.loads(response.text)
		series = dataDict['Monthly Time Series']
		Equity = {}
		for date in series:
			month = date[5:7]
			year = date[:4]
			newdate = month + '/' + year
			Equity[newdate] = float(series[date]['4. close'])
		finalEquity = {}
		keys = list(Equity.keys())
		keys.reverse()
		for key in keys:
			finalEquity[key] = Equity[key]
		return finalEquity

	def getMajorIndicesMonthly(self):
		'''
		Gets the all the equities supplied in the master names dictionary
		'''
		majorIndices = {}
		for symbol in self.MasterAVNamesSM:
			majorIndices[symbol] = self.getEquity(symbol, 'TIME_SERIES_MONTHLY')
		return majorIndices
