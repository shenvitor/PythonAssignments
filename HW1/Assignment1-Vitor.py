#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python assignment 1
Created on Tue Sep 14 12:25:20 2021
@author: vitorshen
at Uppsala University
by Vitor Jose Shen
"""
import matplotlib.pyplot as plt
import numpy as np
# import math as m

#### Read file
data_file = 'pulses.csv'
#### File Columns
f = open(data_file , 'r')                ## here I first open the data file to read
num_cols = len(f.readline().split(','))  ## find out the column numbers of the file by read only one line
f.close()                                ## close file
#### File Rows
f = open(data_file , 'r')                ## open again
lines = f.readlines()                    ## read all lines
num_rows = len(lines)                    ## find out the row number of the file
f.close()                                ## close file
# print(num_cols)
# print(num_rows)

#%%  Q1
#### Use np.loadtxt
## load data using np and set the usecols in np.loadtxt as following
## print all content in datafile including the first column i.e. timestamp
data = np.loadtxt(data_file , dtype = int , delimiter=',' , usecols = range(0 , num_cols) , unpack=True)  
print(data)


#%%  Q2
#### Convert reading numbers  to voltages
## Only data reading numbers excluding the first column
data_num = np.loadtxt(data_file , dtype = float , delimiter=',' , usecols = range(1 , num_cols) , unpack=True)  
## Each row would be a pulse so did a transpose
data_row = np.transpose(data_num)
# print(data_row)

data_Volt = np.array(data_row)           ## Create Volt array
## Voltage (Volts) = (ADC Reading) / (2**10 - 1) * 0.6
for x in range(0,num_rows):
    for y in range(0,num_cols-1):
        data_Volt[x,y] = data_row[x,y] / (2**10 - 1) * 0.6
print('After conversion to V:' , data_Volt)                       ## Check the result the conversion of ADC to Volt
      
#%%  Q3
#### Plot a pulse
## 3.1 Plot a single pulse (i.e. row of the CSV file).
## 3.2 Add axis labels, and a title.
## 3.3 Make the code display your figure.
## 3.4 Save the figure to disk using .savefig(..)
## 3.5 Include this figure in your report.

## First create the array for x axis as 0.5 ns intervals and total 57 data points
data_timepoint = np.zeros(num_cols-1 , dtype=float)    #use num_col-1 exclude 1st column as we transposed in Q2
for i in range(0,num_cols-2):                
    data_timepoint[i+1] += data_timepoint[i] + 0.5

# print(data[0,0])
## Here I choose the first row corresponing to the timestamp 95084640686
fig_one = plt.figure(1)
# fig_one = plt.figure(figsize=(8.0,6.0))
plt.plot(data_timepoint , data_Volt[0] , marker='o' , markersize=3 , color='red')
plt.title('Single pulse of timestamp 95084640686')
plt.xlabel('Times (ns)')
plt.ylabel('Voltage (V)')
plt.savefig('firstrow_pulse.png')
plt.show()

#%% Test for data plotting of other rows 
##row number between 0 and 999
# plt.plot(data_Volt[999] , marker='o' , markersize=3 , color='red')
# plt.title('Single pulse ')
# plt.xlabel('Data points')
# plt.ylabel('Voltage (V)')

#%%  Q4
#### Baseline Correction
## 4.1 For each row/pulse:
## 4.1.1 find the mean (average) of the first 10 elements.
## 4.1.2 Subtract this value from all values for that pulse.
## 4.2 Use a constant for the number of elements used for the mean.
ten_sum = np.array(0 , dtype=float)     ## set a arbitary initial value for sum
ten_mean = np.zeros((num_rows , 1))     ## set a arbitary initial value for smean

## Find the mean value using 2 for loops
for r in range(0,num_rows):
    for c in range(0,10):
        ten_sum += data_Volt[r,c]           ## sum 10 values all that row
    ten_mean[r] = ten_sum / 10              ## divided by 10 that row
    ten_sum = np.array(0 , dtype=float)     ## reset sum for the use of next row

## Check the Mean value of first 10 values for each row
for ti in range(0,num_rows):
    print('Mean value of Row' , ti+1 , ten_mean[ti])

## Subtract this value from all values in that row
data_Basecorr = np.array(data_Volt)
for ri in range(0,num_rows):
    for ci in range(0,num_cols-1):
        data_Basecorr[ri,ci] = data_Volt[ri,ci] - ten_mean[ri]

#  This is the baseline corrected data
print('This is the baseline corrected data:' , data_Basecorr)        

#%%  Q5
fig_two = plt.figure(2)
# fig_two = plt.figure(figsize=(8.0,6.0))
plt.plot(data_timepoint , data_Basecorr[0] , marker='o' , markersize=3 , color='red')
plt.title('Baseline Correction Single pulse ')
plt.xlabel('Times (ns)')
plt.ylabel('Voltage (V)')
plt.savefig('firstrow_baselinecorr_pulse.png')
plt.show()

#%% Test for data plotting of other rows 
#row number between 0 and 999
# plt.plot(data_Basecorr[500] , marker='o' , markersize=3 , color='red')
# plt.title('Single pulse ')
# plt.xlabel('Data points')
# plt.ylabel('Voltage (V)')


#%%  Q6
max_value = np.zeros((num_rows , 1))
for mi in range(0,num_rows):
    max_value[mi] = np.min(data_Basecorr[mi])

sum_value = np.zeros((num_rows , 1))
for si in range(0,num_rows):
    sum_value[si] = np.sum(data_Basecorr[si])
    
# print(max_value)
# print(sum_value)

## Here I try to plot 2 distributions in a same plot
########################################################################
# bins = np.linspace(-10, 0, 100)
# bins = np.linspace(-10,10,100)
# fig_fem = plt.figure(5)
# plt.hist(max_value , bins , alpha=0.5 , label='Max Value')
# plt.hist(sum_value , bins , alpha=0.5 , label='Sum Value')
# plt.title('Two distributions of All Baseline Correction Single pulse ')
# plt.xlabel('Values (V)')
# plt.ylabel('Counts')
# plt.legend()
# plt.savefig('hist_maxandsum_hundredbin_1010.png')
# plt.show()
########################################################################
## But it turns out 2 separate plots would be better to identify their trend

bins = np.linspace(-2.5,2.5,100)
fig_tre = plt.figure(3)
# fig_tre = plt.figure(figsize=(8.0,6.0))
plt.hist(max_value , bins , alpha=1 , label='Max Value' , color='purple')
# plt.hist(sum_value , bins , alpha=0.5 , label='Sum Value')
plt.title('Maximun value distribution')
plt.xlabel('Values (V)')
plt.ylabel('Counts')
plt.legend()
plt.savefig('hist_max.png')
plt.show()

bins = np.linspace(-10,10,100)
fig_fyra = plt.figure(4)
# plt.hist(max_value , bins , alpha=0.5 , label='Max Value')
plt.hist(sum_value , bins , alpha=1 , label='Sum Value' , color='green')
plt.title('All sum up value distribution')
plt.xlabel('Values (V)')
plt.ylabel('Counts')
plt.legend()
plt.savefig('hist_sum.png')
plt.show()

#%% Histogram bin testing
# bins = np.linspace(-10, 10, 1000)
# fig_fyra = plt.figure(4)
# plt.hist(max_value , bins , alpha=0.5 , label='Max Value')
# plt.hist(sum_value , bins , alpha=0.5 , label='Sum Value')
# plt.title('Two distributions of All Baseline Correction Single pulse ')
# plt.xlabel('Values (V)')
# plt.ylabel('Counts')
# plt.legend()
# plt.savefig('hist_maxandsum_thousandbin_1010.png')
# plt.show()
