import requests
import json



# baseUrl = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=MSFT&apikey=D3V05J5VFISOLEIH'
# function = 'TIME_SERIES_MONTHLY'
# symbol = 'MSFT'
# apikey = 
# url = baseUrl + 'function=' + function + '&' + 'symbol' + symbol + '&' + 'apikey=' + apikey

# response = requests.get(baseUrl)
# dataDict = json.loads(response.text)

class AlphaVantageReader:

	def __init__(self):
		self.apiKey = 'D3V05J5VFISOLEIH'
		self.SupplyMavenSymbols = {}
		self.MasterAVNamesSM = {'DJI': 'Dow Jones Industrial Average', '^GSPC':'S&P 500'}

	def getEquity(self, symbol, frequency):
		
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
		for key in sorted(Equity.keys(), reverse = False):
			finalEquity[key] = Equity[key]

		return finalEquity

	def getMajorIndicesMonthly(self):

		majorIndices = {}
		for symbol in self.MasterAVNamesSM:
			majorIndices[symbol] = self.getEquity(symbol, 'TIME_SERIES_MONTHLY')
		return majorIndices


			


# a = AlphaVantageReader()
# x = a.getEquity('DJI', 'TIME_SERIES_MONTHLY')
# print(x)




