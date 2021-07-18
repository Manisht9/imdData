import imdlib as imd
import numpy as np
import pandas as pd
# """ 
# # install imdlib python library
# # you should be connected to internet for downloading the data
# #-9999 value is for no data in saved csv file
# # This code will download the imd data first and then convert the data to csv file
# if you have data already downloaded then create folder named rain/tmax/tmin inside any folder and 
# copy yearly data files in the respective folder and rename yearly data file as year name i.e 1951.GRD 1952.GRD etc and 
# comment the line imd.get_data(variable,start_yr) and run the code it will convert the binary .GRD data into csv file
# """
start_yr = 2000 # give starting year from which you want to download/convert data: 1901 ownwards for rainfall, 1951 for tmax and tmin
end_yr = 2020 # give ending year upto which you want to download/convert data
variable = 'rain' # give variable name (rain for rainfall, tmax or tmin for min or max temperature)
file_format = 'yearwise' # other option (None), which will assume deafult imd naming convention
imd.get_data(variable, start_yr, end_yr, fn_format='yearwise', file_dir='H:/d/data/') # download IMD data: just change path as per your requirement
file_dir = 'H:/d/data/' # this path should be same as mentioned in previous line
data = imd.open_data(variable, start_yr, end_yr,'yearwise', file_dir) # this will open the data downloaded and saved in the location mentioned in previous line
if variable == 'rain':
    grid_size = 0.25 # grid spacing in deg
    y_count = 129 # no of grids in y direction
    x_count = 135 # no of grids in x direction
    x = 66.5 # starting longitude taken from control file (.ctl)
    y = 6.5 # starting latitude taken from control file (.ctl)
elif variable == 'tmax' or variable == 'tmin':
    grid_size = 1 # grid spacing in deg
    y_count = 31 # no of grids in y direction
    x_count = 31 # no of grids in x direction
    x = 67.5 # starting longitude taken from control file (.ctl)
    y = 7.5 # starting latitude taken from control file (.ctl)

#print(grid_size,x_count, y_count, x, y)
data
data.shape
np_array = data.data
#print(np_array[0,0,0])
#xr_objecct = data.get_xarray()
#type(xr_objecct)
#xr_objecct.mean('time').plot()
years_no = (end_yr - start_yr) + 1
#print(years_no)
day = 0
for yr in range(0,years_no):
    f = open("H:/d/data/"+str(start_yr+yr)+"_"+str(variable)+".csv",'w') # just change the path where you want to save csv file
    if ((start_yr+yr) % 4 == 0) and ((start_yr+yr) % 100 != 0):  # check for leap year
        days = 366
        count = yr + days
    elif ((start_yr+yr) % 4 == 0) and ((start_yr+yr) % 100 == 0) and ((start_yr+yr) % 400 == 0):
        days = 366
        count = yr + days
    else:
        days = 365
        count = yr + days

    day = day + days

    f.write("X,Y,")
    for d in range(0, days):
        f.write(str(d+1))
        f.write(",")
    f.write("\n")
    #print(np_array[364,0,0])
    for j in range(0, y_count):

        for i in range(0, x_count):

            f.write(str((i * grid_size) + x))
            f.write(",")
            f.write(str((j * grid_size) + y))
            f.write(",")
            time = 0
            for k in range(day-days, day):

                val = np_array[k,i,j]
                if val == 99.9000015258789 or val == -999:
                    f.write(str(-9999))
                    f.write(",")
                else:
                    f.write(str(val))
                    f.write(",")


            f.write("\n")
    print("File for " + str(start_yr + yr) + "_" + str(variable) + " is saved")
print("CSV conversion successful !")