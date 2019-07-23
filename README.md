# gg-supply-maven

**Installation**  
1.) Clone the repository.    
2.) Cd into folder where you saved the repository.  
3.) Run "pip install -r requirements.txt" from your terminal.  
4.) Once this successfully completes, you should be able to run all the code.  

**File Overview:**     
1.) Data Collection 
* AlphaVantageReader.py: Reads data from [AlphaVantage](https://www.alphavantage.co/)
* BlsReader.py: Scrapes data from text files published by the [Bureau of Labor Statistics](https://www.bls.gov/)
* QuandlReader.py: Reads data from [Quandl](https://www.quandl.com/)
* MasterDataCollection.py: Has methods to get all data from all sources.

2.) Prediction Model
* CorrelationFInder.py: For a pricing dictionary, this service finds the correlation between any one commodity and every   
other commodity in the dictionary. Also has a method to find the top 5 highest correlated commodities.

3.) Jupyter Testing
* SimulateService.ipynb: Allows user to practice running programs defined by the MainService.py class. In order to run, you must do these steps:  
1.) Follow [these](https://jupyter.org/install) steps to install jupyter as you'll need it to run the files.  
2.) Clone this repository onto whichever local directory you want and, using your terminal, change directory into that folder.  
3.) Now run jupyter notebook in that directory and select the MainServiceTest.ipynb file.(If unfamiliar with command line, open the anaconda app and click on the jupyter notebook app. From there, open the file.)   
4.) To run a line, click on the box then press shift + enter. I've provided sample code to change.

4.) MainService.py Functions  
* To initialize an object in jupyter, set a variable equal to "MainService()" after importing the object
* class attributes are a MasterData object (which stores timeseries data in its MasterPrices dictionary attribute and names in CodeToNames attribute), and a CorrelationFinder object which is used for correlating commodities.  
* updateAllData: stores all database in MainService
* mockUpdateAllData: stores all database in MainService from saved file. This is much faster if you don't want to spend the time updating everything.  
* queryNames: takes in one argument as a string search. When called, it returns everything in the database matching that name.  
* getIdFromName: takes in one argument as a string representing the series title. It returns the database Id associated with it.  
* getNameFromId: takes in one argument as a string representing the Id. Returns the series title associated with it.  
* findFiveHighestCorrelated: given an id, this returns the five highest correlated ids along with their correlation values as a list of tuples.  
* plotTimeSeries: given a list of ids, this returns a plot of all their timeseries data.  
* saveTimeSeriesToFile: given the string name of the desired title for a filename, this saves the stored database of timeseries data to a json file in your current directory.  
* saveIdsToFile:  given the string name of the desired title for a filename, this saves the stored database of ids mapped to their names to a json file in your current directory.  
* linearRegress: given and Id, this performs a regression on the ID and returns the coefficient and intercept for that regression line. If in the arguments, you put plot = True, it will plot each id along with its regression line.


    











