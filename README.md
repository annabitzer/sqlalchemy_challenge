# sqlalchemy_challenge

An analysis was performed on climate data from Hawaii using SQLalchemy. Pandas dataframes and matplotlib plots were used to aid in interpreting the data. Precipitation and temperature data were both evaluated for 9 weather stations throughout Hawaii, focusing on data from the last year of data collected (August 2016 - August 2017). Using a SQLalchemy query to retrieve the precipitation data, it is found that for the year analyzed the precipitation ranges from 0 to 6.7 inches a day, with an overal average of 0.18 inches. The temperature for the particular station analyzed, USC00519281, ranged from the 60 to 80 degree range, with the majoity of days falling around 70-80 degrees. 

Additionally, Flask was used to create an application that could be used to retrieve data from the data tables imported through SQLalchemy. The app is able to pull information on precipitation, stations and general temperature data. Additionally it can return the minimum, maximum and average temperature after a specific date, as well as between a given start and end date, given by the user.


Sources used: 
-quantile refresher: https://www.geeksforgeeks.org/numpy-quantile-in-python/
-station analysis: https://stackoverflow.com/questions/62676385/sqlalchemy-query-to-count-the-times-that-a-value-exist-in-a-column
-Xpert learning assistant in bootcamp spot was utilized to identify minor syntax errors in the exploratory station analysis section.
-histogram plotting: https://www.geeksforgeeks.org/plotting-histogram-in-python-using-matplotlib/