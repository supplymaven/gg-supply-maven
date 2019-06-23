import quandl
import datetime



class QuandlReader:
	
	def __init__(self):
		'''
		Sets api key upon initialization
		'''
		quandl.ApiConfig.api_key = 'd-LyarSr8s9xzyQ7qoqG'
		self.now = datetime.datetime.now()
		self.funcKeys = {'QuandlGold': self.getGold, 'QuandlWTICrude': self.getWtiCrudeOil}
		#the available commodities maps the global id to local id
		self.availableCommodities = {'QuandlGold': 'Gold', 'QuandlWTICrude':'WTI Crude Oil'}

	def getGold(self):
		'''
		Gets gold value/ounce in usd
		'''
		now = self.now
		end_date = str(now)[:10]
		data = quandl.get("LBMA/GOLD", authtoken="d-LyarSr8s9xzyQ7qoqG", collapse = 'monthly')
		data_dict = dict(data.to_dict())
		usdGold = data_dict['USD (AM)']
		final = {}
		for series in usdGold:
			x = str(series)[:10]
			fin = x[5:7] + "/" + x[:4]
			final[fin] = float(usdGold[series])
		return final

	def getWtiCrudeOil(self):
		now = self.now
		end_date = str(now)[:10]
		data = quandl.get("EIA/PET_RWTC_D", authtoken="d-LyarSr8s9xzyQ7qoqG", collapse = 'monthly')
		data_dict = dict(data.to_dict())
		series = data_dict['Value']
		final = {}
		for s in series:
			x = str(s)[:10]
			fin = x[5:7] + "/" + x[:4]
			final[fin] = float(series[s])
		return final


	def getData(self, commodities):
		'''
		Given a list of commodities, this function selects which data to collect from Quandl.
		'''
		toReturn = {}
		for asset in commodities:
			toReturn[asset] = self.funcKeys[asset]()
		return toReturn


