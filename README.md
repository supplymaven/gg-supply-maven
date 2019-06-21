# gg-supply-maven

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
* JupyterTesting.py.ipynb: Allows user to practice running these programs. In order to run, you must do these steps:  
1.) Follow [these](https://jupyter.org/install) steps to install jupyter as you'll need it to run the files.  
2.) Clone this repository onto whichever local directory you want and, using your terminal, change directory into that folder.  
3.) Now run jupyter notebook in that directory and select the JupyterTesting.py.ipynb file.(If unfamiliar with command line, open the anaconda app and click on the jupyter notebook app. From there, open the file.)   
4.) To run a line, click on the box then press shift + enter. I've provided sample code to change.











