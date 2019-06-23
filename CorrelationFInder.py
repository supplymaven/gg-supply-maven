import json
import matplotlib.pyplot as plt
import numpy

numpy.seterr(invalid='ignore')


with open('jsondata/allcleandata.json','r') as f:
    data = f.read()

allcleandata = json.loads(data)



class CorrelationFinder:
	
	def __init__(self, data):
		self.prices = data

	
	def gen_return_vector(self, commodity, start_month, end_month):
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
				if month[:2] != '13':
					
					values.append(self.prices[commodity][month])
					
			if month == end_month:
				append = False
		
		returns = []
		for i in range(1,len(values)):
			val1 = values[i]
			val2 = values[i-1]
			r = (val1-val2)/100.0
			returns.append(r)
		return returns


	def find_correlation(self, id_1, id_2, start, end, plot = False):
		'''returns correlation between two vectors 
		of data specified by a given start and end month'''
		
		#find vector of self.prices between these two months
		id1_dict = self.prices[id_1]
		id2_dict = self.prices[id_2]

		
		id1returns = self.gen_return_vector(id_1, start, end)
		id2returns = self.gen_return_vector(id_2, start, end)


		if plot:
			plt.plot(id1returns, id2returns, 'ro')
			plt.show()

		#Ensure that the correlation is over a period of reasonable length
		if len(id1returns) == len(id2returns) and len(id1returns) > 48:
			
			coefficient = numpy.corrcoef(id1returns, id2returns)[0][1]

			return coefficient
		else:
			return 'Missing Data'	

		
	def start_and_end(self, series_id):
		'''returns start and end of both ids as given by the excel file'''
		
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
		
		coeff = self.find_correlation(id1, id2, start, end, plot = False)
		if coeff != 'Missing Data':
			return float(coeff)
		else:
			return 'Missing Data'


	def best_correlations(self, series_id, varied_ind = False):
		'''find the 5 best correlations between an id and the other data points
		   returns a list of 5 tuples with id in index 0 and correlation in index 1
		   if varied_ind is set to true, all 5 commodities will be from separate 
		   industries.'''
		f_ids = set()
		ind1 = series_id[3:6]
		inds = {ind1}
		found = []

		while len(found) < 5:
			best_correlation = 0
			for id2 in self.prices:
				
				corr = self.asset_correlation(series_id, id2)
				industry = id2[3:6]
				if id2 not in f_ids:
					if corr != 'Missing Data' and series_id != id2:

						if abs(corr) >= best_correlation:
							#if specified to vary the industry, will only search through data that represents
							#a different industry
							if varied_ind:
								if industry not in inds:
									best_correlation = corr
									best_id = id2
									best_ind = industry
									
							else:
								best_correlation = corr
								best_id = id2
			# inds.add(best_ind)
			f_ids.add(best_id)
			found.append((best_id, best_correlation))
		return found

