from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import csv
import json


class BlsReader:
	'''
	Class takes a BLS repo and extracts data from every link based on the 
	specified repo code. Parameters: repo code ('wp', 'nd')
	'''

	def __init__(self):
		self.repo = 'https://download.bls.gov/pub/time.series/'
		self.masterDict = {}
		self.seriesName = {}
		self.availableData = {'ENTER': 'DENTER'}


	def storePriceInfo(self, pagecode):
		'''
		Gets all time series data for the repository
		parameter is file which determines the save location for the output
		'''
		# doc = urlopen(self.repo + pagecode)
		doc = urlopen(self.repo + pagecode)
		soup = BeautifulSoup(doc)
		repoLinks = soup.find_all('a')
		counter = 0
		numlinks = str(len(repoLinks))
		for i in repoLinks:
			counter += 1
			link = 'https://download.bls.gov' + i.get('href')
			
			print('File ' + str(counter) + '/' 
				+ numlinks + ': ' + link)

			if self.containsTimeSeriesData(link):
				newDoc = urlopen(link)
				txt = BeautifulSoup(newDoc).get_text()
				self.store(txt)
			else:
				print('No timeseries data')

		print('Download is complete. Length of dictionary is ' + str(len(self.masterDict)) + ' entries.')
		

	def saveTimeSeriesToFile(self, file):
		'''
		Once desired information is stored, save the master database to a file.
		'''
		with open(file,"w") as f:
			json.dump(self.masterDict, f)

	def mapSeriesToName(self, pagecode):
		'''
		Retrieves data for the information about series
		'''
		
		doc = urlopen(self.repo + pagecode)
		soup = BeautifulSoup(doc)
		repoLinks = soup.find_all('a')

		for i in repoLinks:
			link = 'https://download.bls.gov' + i.get('href')
			
			if self.containsSeriesInfo(link):
				newDoc = urlopen(link)
				txt = BeautifulSoup(newDoc).get_text()
				self.storeName(txt)
		print("Successfully mapped series ids to names.")
				
	
	
	# def storeEiName(self,text):
		'''
		Stores name of Import/Export .series files as they are slightly more
		complicated
		'''
		# d = self.seriesName
		# print(text)
		# reader = csv.reader(text.splitlines())
		# title = next(reader)
		# counter = 0
		# benjamincounter = 0
		# for line in reader:
		# 	info = line[0].split()
		# 	series_id = info[0]
		# 	# counter += 1if 'Monthly' in info:
		# 	# # 	benjamincounter += 1
		# 	print(info)
		# print(counter)
		# print(benjamincounter)

	def storeName(self, text):
		d = self.seriesName
		reader = csv.reader(text.splitlines())
		title = next(reader)
		for line in reader:
			info = line[0].split()
			industry_code = info[0]
			product_code = info[1]
			product_name_list = info[2:]
			product_name = product_name_list[0]
			for word in product_name_list[1:]:
				product_name += ' ' + word

			d[industry_code + product_code] = product_name


	def containsSeriesInfo(self, link):
		'''
		Checks if link contains timeseries info
		'''
		if link[-7:] == 'product':
			return True
		if link[-4:] == 'item':
			return True
		return False
	
	def containsTimeSeriesData(self, link):
		'''
		checks if link contains timeseries data.
		ensures it doesn't choose the current link as this only provides
		data since 1994
		'''
		if 'data' in link and "Current" not in link:
			return True
		return False

	def store(self, text):
		'''
		stores pricing string in master dictionary
		'''
		d = self.masterDict
		reader = csv.reader(text.splitlines())
		title = next(reader)
		for row in reader:
			x = row[0].split()
			name = x[0]
			year = x[1]
			month = x[2][-2:]
			value = float(x[3])
			

			if name in d:
				d[name][month + '/' + year] = value
			else:
				d[name] = {}
				d[name][month + '/' + year] = value
		




			




	

	

