import json
import matplotlib.pyplot as plt
import numpy
import time

numpy.seterr(invalid='ignore')

class CorrelationFinder:
	
	def __init__(self, data):
		'''
		initialize correlation finder
		'''
		self.prices = data

	def gen_return_vector(self, commodity, start_month, end_month):
		'''
		Decides if bls data or not and runs appropriate function
		'''
		dataType = commodity[:2]
		PPIData = {'CU', 'PC', 'WP'}
		if dataType in PPIData:
			return self.blsReturnVector(commodity, start_month, end_month)
		else:
			return self.priceReturnVector(commodity, start_month, end_month)

	def blsReturnVector(self, commodity, start_month, end_month):
		values = []
		if start_month in self.prices[commodity]:
			append = False
		else:
			append = True
		
		#Normalize all dates to begin with the start month and end with the end month
		for month in self.prices[commodity]:
			if month == start_month:
				append = True
			if append:
				values.append(self.prices[commodity][month])		
			if month == end_month:
				append = False
		
		returns = []
		for i in range(1,len(values)):
			val1 = values[i]
			val2 = values[i-1]
			r = ((val1-val2)/val1)*100
			returns.append(r)
		return returns

	def priceReturnVector(self, commodity, start_month, end_month):
		'''given a price vector, start month, and end month
		this creates a vector of returns 
		by computing the percent change in each data entry'''

		values = []
		if start_month in self.prices[commodity]:
			append = False
		else:
			append = True

		#Normalize all dates to begin with the start month and end with the end month
		for month in self.prices[commodity]:
			if month == start_month:
				append = True
			if append:
				values.append(self.prices[commodity][month])	
			if month == end_month:
				append = False
		
		returns = []
		for i in range(1,len(values)):
			val1 = values[i]
			val2 = values[i-1]
			try:
				r = ((val1-val2)/val2)*100
			except:
				#when val2 is zero
				r = 1000
			returns.append(r)
		return returns

	def find_correlation(self, id1returns, id2returns, start, end):
		'''returns correlation between two vectors 
		of data specified by a given start and end month'''
		if len(id1returns) == len(id2returns) and len(id1returns) > 48:
			coefficient = numpy.corrcoef(id1returns, id2returns)[0][1]
			return coefficient
		else:
			return 'Missing Data'	

	def start_and_end(self, series_id):
		'''returns start and end of both ids as given by the file'''
		iddates = list(self.prices[series_id].keys())
		start = iddates[0]
		end = iddates[-1]
		return start, end

	def start_find(self, start1, start2):
		#determine which start is last
		year1 = int(start1[-4:])
		month1 = int(start1[:2])
		year2 = int(start2[-4:])
		month2 = int(start2[:2])

		if year2 == year1:
			if month1 <= month2:
				return start2
			else:
				return start1
		elif year1 < year2:
			return start2
		else:
			return start1

	def end_find(self, end1, end2):
		'''finds which end is first'''
		year1 = int(end1[-4:])
		month1 = int(end1[:2])
		year2 = int(end2[-4:])
		month2 = int(end2[:2])
		if year1 == year2:
			if month1 <= month2:
				end = end1
			else:
				end = end2
		elif year1 < year2:
			end = end1
		else:
			end = end2
		return end

	def asset_correlation(self, id1, id2):
		'''returns asset correlation between two commodities. If there
		is missing data, returns "Missing Data" '''
		
		id1start, id1end = self.start_and_end(id1)
		id2start, id2end = self.start_and_end(id2)
		start = self.start_find(id1start, id2start)
		end = self.end_find(id1end, id2end)
		id1_dict = self.prices[id1]
		id1returns = self.gen_return_vector(id1, start, end)
		id2_dict = self.prices[id2]
		id2returns = self.gen_return_vector(id2, start, end)
		coeff = self.find_correlation(id1returns, id2returns, start, end)
		
		if coeff != 'Missing Data':
			return float(coeff)
		else:
			return 'Missing Data'

	def best_correlations(self, series_id, varied_ind = False):
		'''
		find the 5 best correlations between an id and the other data points
		returns a list of 5 tuples with id in index 0 and correlation in index 1
		varied_ind parameter decides whether to have an assortment of industries 
		or not and ensures a variety of industries are represented.
		'''
		f_ids = set()
		ind1 = series_id[3:6]
		inds = {ind1}
		found = []
		correlations = {}

		for id2 in self.prices:
			if id2 != series_id:
				corr = self.asset_correlation(series_id, id2)
				correlations[id2] = corr
		
		while len(found) < 5:
			bestcorr = 0
			best_series = str()
			for Id in correlations:
				if varied_ind:
					ind = Id[3:6]
					corr = correlations[Id]
					if corr != 'Missing Data':
						if abs(corr) > abs(bestcorr):
							if ind not in inds:
								bestcorr = corr
								best_series = Id
								inds.add(ind)
				elif Id not in f_ids:
					corr = correlations[Id]
					if corr != 'Missing Data':
						if abs(corr) > abs(bestcorr):
							bestcorr = corr
							best_series = Id
			found.append((best_series, bestcorr))
			f_ids.add(best_series)
		return found
