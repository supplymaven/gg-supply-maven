import json
#imports the different regressors
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from sklearn.metrics import r2_score
from sklearn.metrics import explained_variance_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import median_absolute_error
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np

with open('data/pricedictionary.json', 'r') as f:
	prices = json.load(f)


#finds the linear trend between a specified start and end month
def linear_regress(commodity, start_month, end_month, plot = False):
	#generate range of months (xs)
	
	months = []
	values = []
	x = []
	m = 1

	if start_month in prices[commodity]:
		append = False
	else:
		append = True

	#Normalize all dates to begin with the start month and end with the end month
	for month in prices[commodity]:
		if month == start_month:
			append = True
		if append:
			if month[:2] != '13':
				x.append(m)
				months.append([m])
				values.append(prices[commodity][month])
				m += 1
		if month == end_month:
			append = False


	#create the linear model
	model = LinearRegression()
	model.fit(months, values)
	print('intercept:', model.intercept_, 'coeff:', model.coef_)

	# plt.plot(months, values, 'ro')
	
	#generate best fit line
	x = np.array(range(1, 2*len(months)))
	
	y = model.intercept_ + model.coef_*x
	
	if plot:	
		plt.plot(months, values, 'ro')
		plt.plot(x,y)
		plt.show()

	

	
regressions = []
for i in prices:
	start = list(prices[i].keys())[0]
	end = list(prices[i].keys())[-1]
	regressions.append(linear_regress(i, start, end))
# i = 'PCU1133--1133--'
# start = list(prices[i].keys())[0]

# end = list(prices[i].keys())[-1]

# linear_regress(i, start, end, True)

	


		