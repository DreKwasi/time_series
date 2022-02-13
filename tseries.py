# import vaex as vx
# import pandas as pd
# import numpy as np
# import os
# from datetime import datetime
# from dateutil import parser
# import matplotlib.pyplot as plt
# from matplotlib import dates as mpl_dates
# from scipy.signal import savgol_filter
# from statsmodels.tsa.seasonal import seasonal_decompose
# from statsmodels.tsa.arima.model import ARIMA
# from statsmodels.tsa.statespace.sarimax import SARIMAX
# from statsmodels.tsa.stattools import adfuller
# from sklearn.metrics import mean_squared_error
# from sklearn.metrics import mean_absolute_error
# from statsmodels.tsa.stattools import acf, pacf, arma_order_select_ic
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import vaex as vx
import numpy as np

class Tseries(vaex):
    def __init__(self, data, saleDate:str, qty:str, facility:str, drugClass:str, price:str) -> None:
        self.data = data
        self.saleDate = saleDate
        self.qty = qty
        self.facility = facility
        self.drugClass = drugClass
        self.price = price

    def show_dataset(self):
        return self.data.info
    
    def reduce_dataset(self):
        return self.data[[self.saleDate, self.qty, self.facility, self.drugClass, self.price]]
    
    def data_per_facility(self, name=None):
        '''
        If name is not specified
        Facility with the Highest number of Transactions 
        Is Used
        '''
        if name == None:
            highest = 0
            for name in self.data[self.facility].unique():
                transactions_per_facility = len(self.data[self.data[self.facility] == name])
                if transactions_per_facility > highest:
                    highest = transactions_per_facility
                    largest = name

            print(f"{largest} is the largest facility in terms of volume of transactions with  {highest} transactions")
            return self.data[self.data[self.facility] == name]
        else:
            return self.data[self.data[self.facility] == name]
        
    def data_per_drugclass(self, itemclass=None, per_facility=True):
        '''
        If name is not specified
        DrugClass with the Highest number of Transactions 
        Is Used

        If per_facility is True; data_per_facility is run before
        getting drug class of highest number of transactions

        '''

        if per_facility and item_class==None:
            facility_data = self.data_per_facility()

            highest = 0
            for item_class in facility_data[self.drugClass].unique():
                transactions_per_class = len(facility_data[facility_data[self.drugClass] == item_class])
                if transactions_per_class > highest:
                    highest = transactions_per_class
                    largest = item_class

            print(f"{largest} are sold more often with {highest} volume of transactions for {facility_data[self.facility][0]}")
            return facility_data[facility_data[self.drugClass] == largest]

        elif per_facility == False and item_class != None:
            return self.data[self.data[self.drugClass] == item_class]

        elif per_facility and item_class != None:
            facility_data = self.data_per_facility()
            return facility_data[facility_data[self.drugClass] == item_class]
        
        elif per_facility == False and item_class == None:
            highest = 0
            for item_class in self.data[self.drugClass].unique():
                transactions_per_class = len(self.data[self.data[self.drugClass] == item_class])
                if transactions_per_class > highest:
                    highest = transactions_per_class
                    largest = item_class

            print(f"{largest} are sold more often with {highest} volume of transactions")
            return self.data[self.data[self.drugClass] == largest]


    def frequency_data(self, freq_data, *freq):
        """
        freq : ['h', 'D', 'W', 'M']
        """

        freq_names = {'h' : 'Hourly', 
                      'D' : 'Daily',
                      'W':'Weekly',
                      'M':'Monthly'
                    }

        freq_dict = {}
        if freq:
            for i in freq:
                freq_dict[freq_names[i]] = freq_data.groupby(by=vx.BinnerTime(freq_data[self.saleDate]
                                            resolution=i), agg={self.qty:'sum'})

        return freq_dict

    


df = Tseries(np.array([1,2,3]))