from QuandlReader import QuandlReader
from BlsReader import BlsReader
from AlphaVantageReader import AlphaVantageReader
import datetime



class MasterDataCollection:
	'''
	Class contains methods that can collect all SupplyMaven pricing data
	'''
	def __init__(self):
		self.MasterPrices = {}
		self.CodeToNames = {}
	
	def collectBls(self, pagecodes):
		bls = BlsReader()
		for pagecode in pagecodes:
			bls.storePriceInfo(pagecode) 
			bls.mapSeriesToName(pagecode)
		self.MasterPrices.update(bls.masterDict)
		self.CodeToNames.update(bls.seriesName)
	def collectAllBls(self):
		bls = BlsReader()
		for pagecode in ['wp', 'pc', 'cu', 'ap']:
			bls.storePriceInfo(pagecode) 
			bls.mapSeriesToName(pagecode)
		self.MasterPrices.update(bls.masterDict)
		self.CodeToNames.update(bls.seriesName)

	def collectAllQuandl(self):
		qdl = QuandlReader()
		qdlData = qdl.getData(list(qdl.availableCommodities.keys()))
		self.MasterPrices.update(qdlData)
		self.CodeToNames.update(qdl.availableCommodities)

	def collectAllStockIndices(self):
		av = AlphaVantageReader()
		indices = av.getMajorIndicesMonthly()
		self.MasterPrices.update(indices)
		self.CodeToNames.update(av.MasterAVNamesSM)

	def cleanBlsData(self):
		#WE WANT AT LEAST 6 years of continuous recent data
		print('CLEANING DATA...')
		data = self.MasterPrices
		names = self.CodeToNames
		new = {}
		newnames = {}
		missing_data = set()
		for i in data:
			dates = list(data[i].keys())
			if self.isRecent(dates):
				new[i] = data[i]
				newnames[i] = names[i]
		
		#update master dictionary
		self.MasterPrices = new
		self.CodeToNames = newnames
		print('DATA CLEANED!')

	def isRecent(self, d):
		'''
		determines if 6 years of recent data are available for a list of dates
		'''
		dates = list(d)
		dates.reverse()
		now = datetime.date.today()
		seriesMonth = int(dates[0][:2])
		seriesYear = int(dates[0][3:])
		seriesDay = now.day
		seriesDate = datetime.date(seriesYear, seriesMonth, seriesDay)
		#make sure first date is within 3 months of current date
		difference = (now - seriesDate).days
		if difference > 100:
			return False
		else:
		#check if 6 years of continuous data
		#there should be 72 continuous entries
			counter = 0
			for i in range(len(dates)-1):
				counter += 1
				nextmonth = int(dates[i][:2])
				lastmonth = int(dates[i+1][:2])
				nextyear = int(dates[i][3:])
				lastyear = int(dates[i+1][3:])
				difference = 12*(nextyear - lastyear) + nextmonth - lastmonth
				if difference != 1:
					return False
				elif counter == 72:
					return True
		if counter < 72:
			return False
		return True

