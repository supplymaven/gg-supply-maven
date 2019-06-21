from QuandlReader import QuandlReader
from BlsReader import BlsReader
from AlphaVantageReader import AlphaVantageReader



class MasterDataCollection:

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
		for pagecode in ['wp', 'nd', 'pc', 'pd', 'wd']:
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



# m = MasterDataCollection()

# m.collectAllStockIndices()
# print(m.MasterPrices)
# print(m.MasterNames)
# for key in m.MasterNames:
# 	print(m.MasterPrices[key])


		