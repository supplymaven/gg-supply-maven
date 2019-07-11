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
		print(self.repo + pagecode)
		doc = urlopen(self.repo + pagecode)
		soup = BeautifulSoup(doc, "lxml")
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
				txt = BeautifulSoup(newDoc, "lxml").get_text()
				self.store(txt)
		print('Download is complete. Length of dictionary is ' + str(len(self.masterDict)) + ' entries.')
		
	def mapSeriesToName(self, pagecode):
		'''
		Retrieves data for the series name
		'''
		doc = urlopen(self.repo + pagecode)
		soup = BeautifulSoup(doc, "lxml")
		repoLinks = soup.find_all('a')

		for i in repoLinks:
			link = 'https://download.bls.gov' + i.get('href')
			if self.containsSeriesInfo(link, pagecode):
				newDoc = urlopen(link)
				txt = BeautifulSoup(newDoc, "lxml").get_text()
				self.storeSeriesFileName(txt, pagecode)
		print("Successfully mapped series ids to names.")
				
	def storeSeriesFileName(self, text, pagecode):
		d = self.seriesName
		reader = csv.reader(text.splitlines())
		title = next(reader)
		pcSeriesIndex = {'cu': 7, 'wp': 5, 'pc':5, 'ap': 3, 'ei':5, 'cw': 7}
		for line in reader:
			newl = ''
			for string in line:
				newl = newl + string
			info = newl.split('\t')
			Id = info[0].strip()
			index = pcSeriesIndex[pagecode]
			series_title = info[index]
			d[Id] = series_title

	def containsSeriesInfo(self, link, pc):
		'''
		Checks if link contains timeseries info
		'''
		if link[-6:] == 'series':
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
			value = x[3]
			if month != '13' and value != '-':
				if name in d:
					d[name][month + '/' + year] = float(value)
				else:
					d[name] = {}
					d[name][month + '/' + year] = float(value)
