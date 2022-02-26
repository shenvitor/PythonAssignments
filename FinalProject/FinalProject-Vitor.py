#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 4 13:37:27 2021

@author: Vitor Jose Shen
at Uppsala University
"""

"""
Penalty!
The origin of this project is the need to estimate expected detector count rates. 
# Assume a radioactive source emitting radiation of some kind (particles or gamma rays) 
isotropically, i.e. with no preferred direction. 
# Assume further a detector with given dimensions placed in some distance from the source. 
# We would be interested in knowing what fraction of the emitted radiation
would impinge on the detector surface.


This problem can be transferred into the world of macroscopic objects. 
As an example, we chose a football pitch:
    
What is the probability that you score a goal when you shoot a football from 
the penalty spot, but in completely random directions (including e.g. straight up)?

Write a code that performs a Monte Carlo simulation of a (high) number of penalties 
and determine the fraction of kicks where the ball ends up in the goal. 

Make reasonable assumptions (shooting e.g. straight down is not a good idea). 

Find relevant information and give references!

For a start, you may assume that the ball has a diameter of zero (point mass) 
and that if will move on a straight line after the kick. 
(This would correspond to the emission from the radioactive source mentioned above.)
Obviously we assume that there is no goalkeeper.

Additional work might include (some of) the following aspects:
• The ball has a finite diameter and so have the goalposts. 
A collision between the ball and the post can result in that the ball 
bounces into the goal or back in the pitch.
• There is gravity.
• There is a drag force.
• How large would the influence of a goalkeeper be, if he or she moves randomly to any
position in front of the goal?
• What is the probability for scoring an own goal?
"""
#%%
import matplotlib.pyplot as plt
import numpy as np
# import math as m
import random
import scipy.constants as const
from scipy.integrate import solve_ivp


#########################################
#1st section parameter point mass ball and without posts and bar
#########################################
#penalty spot = 11m = 12yd 
distance = 11
# Goal area = 8yd*8ft = 7.32m*2.44m
height = 2.44
width = 7.32
half_width = width/2
area = height*width
# print(distance,height,width,area)

#first assume the ball's radius = 0 point mass
r_ballone = 0
m_ballone = 0
####################################
#end of 1st section parameter
####################################


####################################
#simulation events setting
####################################
# sim_time = 10000 #10k
# sim_time = 100000 #100k
sim_time = 1000000 #1E6


score = np.zeros(sim_time)

#%%

#####################################################
# Setting the possible value in spherical coordinate
####################################################
# Assume only move on a straight line after the kick
# Only theta & phi matter

# theta  # [0,90deg] with 2 decimal
# theta indices between 0 ~ 8999
theta = np.linspace(0, np.pi/2, 9000)

# phi only forward angles  # [0,180deg] with 2 decimal
# phi indices between 0 ~ 17999
phi = np.linspace(0, np.pi, 18000)

# phi all direction  # [0,359.99deg] with 2 decimal
# phi indices between 0 ~ 17999
phi_all = np.linspace(0, 2*np.pi, 35999)
####################################


#random test region
theta_index_collect = []
phi_index_collect = []

theta_collect = []
phi_collect = []

theta_deg_collect = []
phi_deg_collect = []


phi_all_index_collect = []
phi_all_collect = []
phi_all_deg_collect = []


# assume theta in 0~90deg we here excluding go underground
for ti in range(0,sim_time):
    randtest = random.randint(0,8999)
    theta_index_collect.append(randtest)
    rad = theta[randtest]
    theta_collect.append(rad)
    deg = rad / const.pi * 180
    theta_deg_collect.append(deg)
    
    # print("num:",randtest)

# assume phi in  only forward angles 0~180deg
for pi in range(0,sim_time):
    randtest = random.randint(0,17999)
    phi_index_collect.append(randtest)
    rad = phi[randtest]
    phi_collect.append(rad)
    deg = rad / const.pi * 180
    phi_deg_collect.append(deg)
    # print("num:",randtest)

# For phi go literally all directional angles 0~360deg
for pi_all in range(0,sim_time):
    rand_all = random.randint(0,35999-1)
    phi_all_index_collect.append(rand_all)
    rad = phi_all[rand_all]
    phi_all_collect.append(rad)
    deg = rad / const.pi * 180
    phi_all_deg_collect.append(deg)
    # print("num:",randtest)
    


#%% Test Plot 
plt.figure()
plt.hist(theta_deg_collect,bins=90)
plt.title('Theta angle distribution test')
plt.xlim([0, 90])
plt.savefig('RandTheta.png')
plt.show()

plt.figure()
plt.hist(phi_deg_collect,bins=180)
plt.xlim([0, 180])
plt.title('Phi angle in forward direction distribution test')
plt.savefig('RandPhi.png')
plt.show()
#%%
plt.figure()
plt.hist(phi_all_deg_collect,bins=360)
plt.xlim([0, 360])
plt.title('Phi angle all directional distribution test')
plt.savefig('RandPhiAll.png')
plt.show()
#%%
# plt.figure()
# plt.bar(range(0,90), theta_deg_collect)
# plt.show()

# plt.figure()
# plt.bar(range(0,180), phi_deg_collect)
# plt.show()

#%%

####################################
range_intheta = np.arctan(height / distance)
range_inphi = 2 * np.arctan(half_width / distance)
range_thetadeg = range_intheta / const.pi * 180
range_phideg = range_inphi / const.pi * 180
print('range:',range_intheta,range_thetadeg)
print("range:",range_inphi,range_phideg)

print('first rand:',theta[theta_index_collect[0]],theta[theta_index_collect[0]]/const.pi*180)
print('first rand:',phi[phi_index_collect[0]],phi[phi_index_collect[0]]/const.pi*180)
print('first rand:',phi_all[phi_all_index_collect[0]],phi_all[phi_all_index_collect[0]]/const.pi*180)


#%%
# y1=6
# y2=3

# if y1 <=6 and y2>3:
#     print('yes')
# else:
#     print('no') 
#%%
#Determine when hit the target as goal
# 0 <= theta <= arctan(height / distance)
# 0 <= phi <= 2*arctan(half_width / distance)

# np.arctan(height/distance)
# np.arctan(height/distance)

# for a in range(0,10):
#     print(a)

############################################
# coefficient 
# find the new distance everytime!!!
# np.arctan(height/distance)
##############################################

# delta_phi 

# new_distance

# #%%
# test_abs= abs(-100)
# print(test_abs)
#%% ForPhi in  Forward Angles only

score_error = np.zeros(sim_time)

count_error = np.zeros(1)

for sim in range(0,sim_time):
    if theta_collect[sim] <= np.arctan(height/distance) \
and (const.pi/2 - np.arctan(half_width/distance) <= phi_collect[sim] \
and phi_collect[sim] <= const.pi/2 + np.arctan(half_width/distance)):
        score_error[sim] = 1
        print(score_error)
        count_error = count_error + 1
        print(count_error)


count = np.zeros(1)
for sim in range(0,sim_time):
    #### The goal range: Theta as a function of phi
    delta_phi = abs(const.pi/2 - phi_collect[sim])
    # use absolute value above
    distance_new = distance / np.cos(delta_phi)
    
    if theta_collect[sim] <= np.arctan(height/distance_new) \
and (const.pi/2 - np.arctan(half_width/distance) <= phi_collect[sim] \
and phi_collect[sim] <= const.pi/2 + np.arctan(half_width/distance)):
        score[sim] = 1
        print(score)
        count = count + 1
        print(count)

print('The fraction of goals without consideration of theta as function of phi in',sim_time,'isotropic events is:', count_error/sim_time)
print('The fraction of goals with the consideration of theta as function of phi in',sim_time,'isotropic events is:', count/sim_time)



#%% ForPhi in  All directional Angles

score_error_all = np.zeros(sim_time)

count_error_all = np.zeros(1)

for sim in range(0,sim_time):
    if theta_collect[sim] <= np.arctan(height/distance) \
and (const.pi/2 - np.arctan(half_width/distance) <= phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_width/distance)):
        score_error_all[sim] = 1
        print(score_error_all)
        count_error_all = count_error_all + 1
        print(count_error_all)



score_all = np.zeros(sim_time)
count_all = np.zeros(1)
for sim in range(0,sim_time):
    #### The goal range: Theta as a function of phi
    delta_phi = abs(const.pi/2 - phi_all_collect[sim])
    # use absolute value above
    distance_new = distance / np.cos(delta_phi)
    
    if theta_collect[sim] <= np.arctan(height/distance_new) \
and (const.pi/2 - np.arctan(half_width/distance) <= phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_width/distance)):
        score_all[sim] = 1
        print(score_all)
        count_all = count_all + 1
        print(count_all)

###########
print('The fraction of goals without consideration of theta as function of phi in',sim_time,'isotropic events is:', count_error_all/sim_time)
print('The fraction of goals with the consideration of theta as function of phi in',sim_time,'isotropic events is:', count_all/sim_time)




#####################################################
# end of spherical coordinate
####################################################

#%%
# The ball has a finite diameter and so have the goalposts. 
# A collision between the ball and the post can result in that the ball bounces into the goal or back in the pitch.

##################################################
#2nd section parameter ball has a finite diameter 
##################################################

# football diameter 22cm
# football radius=11cm
d_ball = 0.22
# 2D projection
circle = const.pi*d_ball
# print(circle)


##################################################
#3rd section parameter point mass ball and  posts and bar
##################################################
# Resize the area of goal
# crossbar and goalpost thickness 12cm
Goal_PostsBars = 0.12   #12cm=0.12m
Goal_Height = height - Goal_PostsBars
Goal_Width = width - 2*Goal_PostsBars

# inside goal posts and bar
# only Goal_Width * Goal_Width

## Post and bar area
# height * width - Goal_Width * Goal_Width

# the percentage of distribution to use for finite diameter ball with posts and bar
P_d = np.around(np.linspace(0,100,18),decimals=2)
P_dint = np.around(np.linspace(0,100,18),decimals=0)

# P_d[0~17] , P_d[0]=0, P_d[17]=100
tenthousand = []
for dice in range(0,10000):
    rint = random.randint(0, 10000)
    tenthousand.append(rint)

index = 1
multi = int(P_d[index] * 100)
save = np.zeros(10000)
toslice = np.linspace(0,10000-1,multi)
using = toslice.astype(int)
for i in range (0,multi):
    save[using]=1    
    
#%%
def possibility(index):
    # index between 1~16
    mul = int(P_d[index] * 100)
    tempsave = np.zeros(10000)
    tempslice = np.linspace(0,10000-1,mul)
    useslice = tempslice.astype(int)
    for i in range (0,mul):
        tempsave[useslice]=1
    return tempsave

count_outcome_1 = np.zeros(10000)
count_outcome_2 = np.zeros(10000)
count_outcome_3 = np.zeros(10000)
count_outcome_4 = np.zeros(10000)
count_outcome_5 = np.zeros(10000)
count_outcome_6 = np.zeros(10000)
count_outcome_7 = np.zeros(10000)
count_outcome_8 = np.zeros(10000)
count_outcome_9 = np.zeros(10000)
count_outcome_10 = np.zeros(10000)
count_outcome_11 = np.zeros(10000)
count_outcome_12 = np.zeros(10000)
count_outcome_13 = np.zeros(10000)
count_outcome_14 = np.zeros(10000)
count_outcome_15 = np.zeros(10000)
count_outcome_16 = np.zeros(10000)

#%%
for i in range(10000):
    thisrand_1 = random.randint(0,10000-1)
    thisarray_1 = possibility(1)
    count_outcome_1[thisrand_1] = thisarray_1[thisrand_1]
    # the_outcome = thisarray[thisrand]
    # print(the_outcome)
    print('event',i,' P(1):',count_outcome_1[thisrand_1])
    
    thisrand_2 = random.randint(0,10000-1)
    thisarray_2 = possibility(2)
    count_outcome_2[thisrand_2] = thisarray_2[thisrand_2]
    print('event',i,' P(2):',count_outcome_2[thisrand_2])

    thisrand_3 = random.randint(0,10000-1)
    thisarray_3 = possibility(3)
    count_outcome_3[thisrand_3] = thisarray_3[thisrand_3]
    print('event',i,' P(3):',count_outcome_3[thisrand_3])

    thisrand_4 = random.randint(0,10000-1)
    thisarray_4 = possibility(4)
    count_outcome_4[thisrand_4] = thisarray_4[thisrand_4]
    print('event',i,' P(4):',count_outcome_4[thisrand_4])
    
    thisrand_5 = random.randint(0,10000-1)
    thisarray_5 = possibility(5)
    count_outcome_5[thisrand_5] = thisarray_5[thisrand_5]
    print('event',i,' P(5):',count_outcome_5[thisrand_5])
    
    thisrand_6 = random.randint(0,10000-1)
    thisarray_6 = possibility(6)
    count_outcome_6[thisrand_6] = thisarray_6[thisrand_6]
    print('event',i,' P(6):',count_outcome_6[thisrand_6])
    
    thisrand_7 = random.randint(0,10000-1)
    thisarray_7 = possibility(7)
    count_outcome_7[thisrand_7] = thisarray_7[thisrand_7]
    print('event',i,' P(7):',count_outcome_7[thisrand_7])
    
    thisrand_8 = random.randint(0,10000-1)
    thisarray_8 = possibility(8)
    count_outcome_8[thisrand_8] = thisarray_8[thisrand_8]
    print('event',i,' P(8):',count_outcome_8[thisrand_8])
    
    thisrand_9 = random.randint(0,10000-1)
    thisarray_9 = possibility(9)
    count_outcome_9[thisrand_9] = thisarray_9[thisrand_9]
    print('event',i,' P(9):',count_outcome_9[thisrand_9])
    
    thisrand_10 = random.randint(0,10000-1)
    thisarray_10 = possibility(10)
    count_outcome_10[thisrand_10] = thisarray_10[thisrand_10]
    print('event',i,' P(10):',count_outcome_10[thisrand_10])
    
    thisrand_11 = random.randint(0,10000-1)
    thisarray_11 = possibility(11)
    count_outcome_11[thisrand_11] = thisarray_11[thisrand_11]
    print('event',i,' P(11):',count_outcome_11[thisrand_11])
    
    thisrand_12 = random.randint(0,10000-1)
    thisarray_12 = possibility(12)
    count_outcome_12[thisrand_12] = thisarray_12[thisrand_12]
    print('event',i,' P(12):',count_outcome_12[thisrand_12])
    
    thisrand_13 = random.randint(0,10000-1)
    thisarray_13 = possibility(13)
    count_outcome_13[thisrand_13] = thisarray_13[thisrand_13]
    print('event',i,' P(13):',count_outcome_13[thisrand_13])
    
    thisrand_14 = random.randint(0,10000-1)
    thisarray_14 = possibility(14)
    count_outcome_14[thisrand_14] = thisarray_14[thisrand_14]
    print('event',i,' P(14):',count_outcome_14[thisrand_14])
    
    thisrand_15 = random.randint(0,10000-1)
    thisarray_15 = possibility(15)
    count_outcome_15[thisrand_15] = thisarray_15[thisrand_15]
    print('event',i,' P(15):',count_outcome_15[thisrand_15])
    
    thisrand_16 = random.randint(0,10000-1)
    thisarray_16 = possibility(16)
    count_outcome_16[thisrand_16] = thisarray_16[thisrand_16]
    print('event',i,' P(16):',count_outcome_16[thisrand_16])

#%%    
plt.figure() 
plt.hist(count_outcome_1)
plt.xlim(0, 1, 1)
plt.savefig('possibility1.png')
plt.show()

plt.figure() 
plt.hist(count_outcome_2)
plt.xlim(0, 1, 1)
plt.savefig('possibility2.png')
plt.show()

plt.figure() 
plt.hist(count_outcome_3)
plt.xlim(0, 1, 1)
plt.savefig('possibility3.png')
plt.show()

plt.figure() 
plt.hist(count_outcome_4)
plt.xlim(0, 1, 1)
plt.savefig('possibility4.png')
plt.show()

plt.figure() 
plt.hist(count_outcome_5)
plt.xlim(0, 1, 1)
plt.savefig('possibility5.png')
plt.show()

plt.figure() 
plt.hist(count_outcome_6)
plt.xlim(0, 1, 1)
plt.savefig('possibility6.png')
plt.show()

plt.figure() 
plt.hist(count_outcome_7)
plt.xlim(0, 1, 1)
plt.savefig('possibility7.png')
plt.show()

plt.figure() 
plt.hist(count_outcome_8)
plt.xlim(0, 1, 1)
plt.savefig('possibility8.png')
plt.show()    

plt.figure() 
plt.hist(count_outcome_9)
plt.xlim(0, 1, 1)
plt.savefig('possibility9.png')
plt.show()

plt.figure() 
plt.hist(count_outcome_10)
plt.xlim(0, 1, 1)
plt.savefig('possibility10.png')
plt.show()

plt.figure() 
plt.hist(count_outcome_11)
plt.xlim(0, 1, 1)
plt.savefig('possibility11.png')
plt.show()

plt.figure() 
plt.hist(count_outcome_12)
plt.xlim(0, 1, 1)
plt.savefig('possibility12.png')
plt.show()

plt.figure() 
plt.hist(count_outcome_13)
plt.xlim(0, 1, 1)
plt.savefig('possibility13.png')
plt.show()

plt.figure() 
plt.hist(count_outcome_14)
plt.xlim(0, 1, 1)
plt.savefig('possibility14.png')
plt.show()

plt.figure() 
plt.hist(count_outcome_15)
plt.xlim(0, 1, 1)
plt.savefig('possibility15.png')
plt.show()

plt.figure() 
plt.hist(count_outcome_16)
plt.xlim(0, 1, 1)
plt.savefig('possibility16.png')
plt.show()

#%%
# print('the percentage of simulation result of ')
#%%
count_with_postsbar = np.zeros(1)
score_with_postbar = np.zeros(sim_time)
# range that must goal without touching posts or bar

################################################################
##4th section parameter finite diameter ball and  posts and bar
################################################################
## with interaction with goal posts and bar determined by probabilities in different touch areas
height_directgoal = Goal_Height - d_ball / 2
half_w_directgoal = half_width - Goal_PostsBars - d_ball / 2


#%%
# Count with post bar case
# And also with consideration of theta as function of phi
# #### The goal range: Theta as a function of phi
#     delta_phi = abs(const.pi/2 - phi_all_collect[sim])
#     # use absolute value above
#     distance_new = distance / np.cos(delta_phi)

# several in posts or bar area chosen 0.01m as seperate unit 
height_bar_touch1 = height_directgoal + 0.01
half_w_post_touch1 = half_w_directgoal + 0.01

height_bar_touch2 = height_directgoal + 0.02
half_w_post_touch2 = half_w_directgoal + 0.02

height_bar_touch3 = height_directgoal + 0.03
half_w_post_touch3 = half_w_directgoal + 0.03

height_bar_touch4 = height_directgoal + 0.04
half_w_post_touch4 = half_w_directgoal + 0.04

height_bar_touch5 = height_directgoal + 0.05
half_w_post_touch5 = half_w_directgoal + 0.05

height_bar_touch6 = height_directgoal + 0.06
half_w_post_touch6 = half_w_directgoal + 0.06

height_bar_touch7 = height_directgoal + 0.07
half_w_post_touch7 = half_w_directgoal + 0.07

height_bar_touch8 = height_directgoal + 0.08
half_w_post_touch8 = half_w_directgoal + 0.08

height_bar_touch9 = height_directgoal + 0.09
half_w_post_touch9 = half_w_directgoal + 0.09

height_bar_touch10 = height_directgoal + 0.1
half_w_post_touch10 = half_w_directgoal + 0.1

height_bar_touch11 = height_directgoal + 0.11
half_w_post_touch11 = half_w_directgoal + 0.11

height_bar_touch12 = height_directgoal + 0.12
half_w_post_touch12 = half_w_directgoal + 0.12

height_bar_touch13 = height_directgoal + 0.13
half_w_post_touch13 = half_w_directgoal + 0.13

height_bar_touch14 = height_directgoal + 0.14
half_w_post_touch14 = half_w_directgoal + 0.14

height_bar_touch15 = height_directgoal + 0.15
half_w_post_touch15 = half_w_directgoal + 0.15

height_bar_touch16 = height_directgoal + 0.16
half_w_post_touch16 = half_w_directgoal + 0.16

height_bar_touch17 = height_directgoal + 0.17
half_w_post_touch17 = half_w_directgoal + 0.17

#%%
################################################################
# finite d ball
##Forward Angles case : 0 <= phi <= 180deg
################################################################
# For phi in forward angles
for sim in range(0,sim_time):
    
    print('event:',sim+1)
    #### The goal range: Theta as a function of phi
    delta_phi = abs(const.pi/2 - phi_collect[sim])
    # use absolute value above
    distance_new = distance / np.cos(delta_phi)
    
    if theta_collect[sim] <= np.arctan(height_directgoal / distance_new) \
and (const.pi/2 - np.arctan(half_w_directgoal / distance) <= phi_collect[sim] \
and phi_collect[sim] <= const.pi/2 + np.arctan(half_w_directgoal / distance)):
        score_with_postbar[sim] = 1
        print('direct goal',score_with_postbar)
        count_with_postsbar = count_with_postsbar + 1
        
    elif theta_collect[sim] < np.arctan(height_bar_touch1 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch1 / distance) < phi_collect[sim] \
and phi_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch1 / distance)):
        thisrand_16 = random.randint(0,10000-1)
        thisarray_16 = possibility(16)
        count_outcome_16[thisrand_16] = thisarray_16[thisrand_16]
        if count_outcome_16[thisrand_16] == 1:
            score_with_postbar[sim] = 1
            print('touch1 goal',score_with_postbar)
            count_with_postsbar = count_with_postsbar + 1
        print('touch1 No goal',score_with_postbar)
            
    elif theta_collect[sim] < np.arctan(height_bar_touch2 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch2 / distance) < phi_collect[sim] \
and phi_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch2 / distance)):
        thisrand_15 = random.randint(0,10000-1)
        thisarray_15 = possibility(15)
        count_outcome_15[thisrand_15] = thisarray_15[thisrand_15]
        if count_outcome_15[thisrand_15] == 1:
            score_with_postbar[sim] = 1
            print('touch2 goal',score_with_postbar)
            count_with_postsbar = count_with_postsbar + 1
        print('touch2 No goal',score_with_postbar)
            
    elif theta_collect[sim] < np.arctan(height_bar_touch3 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch3 / distance) < phi_collect[sim] \
and phi_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch3 / distance)):
        thisrand_14 = random.randint(0,10000-1)
        thisarray_14 = possibility(14)
        count_outcome_14[thisrand_14] = thisarray_14[thisrand_14]
        if count_outcome_14[thisrand_14] == 1:
            score_with_postbar[sim] = 1
            print('touch3 goal',score_with_postbar)
            count_with_postsbar = count_with_postsbar + 1
        print('touch3 No goal',score_with_postbar)
            
    elif theta_collect[sim] < np.arctan(height_bar_touch4 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch4 / distance) < phi_collect[sim] \
and phi_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch4 / distance)):
        thisrand_13 = random.randint(0,10000-1)
        thisarray_13 = possibility(13)
        count_outcome_13[thisrand_13] = thisarray_13[thisrand_13]
        if count_outcome_13[thisrand_13] == 1:
            score_with_postbar[sim] = 1
            print('touch4 goal',score_with_postbar)
            count_with_postsbar = count_with_postsbar + 1
        print('touch4 No goal',score_with_postbar)    
        
    elif theta_collect[sim] < np.arctan(height_bar_touch5 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch5 / distance) < phi_collect[sim] \
and phi_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch5 / distance)):
        thisrand_12 = random.randint(0,10000-1)
        thisarray_12 = possibility(12)
        count_outcome_12[thisrand_12] = thisarray_12[thisrand_12]
        if count_outcome_12[thisrand_12] == 1:
            score_with_postbar[sim] = 1
            print('touch5 goal',score_with_postbar)
            count_with_postsbar = count_with_postsbar + 1
        print('touch5 No goal',score_with_postbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch6 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch6 / distance) < phi_collect[sim] \
and phi_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch6 / distance)):
        thisrand_11 = random.randint(0,10000-1)
        thisarray_11 = possibility(11)
        count_outcome_11[thisrand_11] = thisarray_11[thisrand_11]
        if count_outcome_11[thisrand_11] == 1:
            score_with_postbar[sim] = 1
            print('touch6 goal',score_with_postbar)
            count_with_postsbar = count_with_postsbar + 1
        print('touch6 No goal',score_with_postbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch7 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch7 / distance) < phi_collect[sim] \
and phi_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch7 / distance)):
        thisrand_10 = random.randint(0,10000-1)
        thisarray_10 = possibility(10)
        count_outcome_10[thisrand_10] = thisarray_10[thisrand_10]
        if count_outcome_10[thisrand_10] == 1:
            score_with_postbar[sim] = 1
            print('touch7 goal',score_with_postbar)
            count_with_postsbar = count_with_postsbar + 1
        print('touch7 No goal',score_with_postbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch8 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch8 / distance) < phi_collect[sim] \
and phi_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch8 / distance)):
        thisrand_9 = random.randint(0,10000-1)
        thisarray_9 = possibility(9)
        count_outcome_9[thisrand_9] = thisarray_9[thisrand_9]
        if count_outcome_9[thisrand_9] == 1:
            score_with_postbar[sim] = 1
            print('touch8 goal',score_with_postbar)
            count_with_postsbar = count_with_postsbar + 1
        print('touch8 No goal',score_with_postbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch9 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch9 / distance) < phi_collect[sim] \
and phi_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch9 / distance)):
        thisrand_8 = random.randint(0,10000-1)
        thisarray_8 = possibility(8)
        count_outcome_8[thisrand_8] = thisarray_8[thisrand_8]
        if count_outcome_8[thisrand_8] == 1:
            score_with_postbar[sim] = 1
            print('touch9 goal',score_with_postbar)
            count_with_postsbar = count_with_postsbar + 1
        print('touch9 No goal',score_with_postbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch10 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch10 / distance) < phi_collect[sim] \
and phi_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch10 / distance)):
        thisrand_7 = random.randint(0,10000-1)
        thisarray_7 = possibility(7)
        count_outcome_7[thisrand_7] = thisarray_7[thisrand_7]
        if count_outcome_7[thisrand_7] == 1:
            score_with_postbar[sim] = 1
            print('touch10 goal',score_with_postbar)
            count_with_postsbar = count_with_postsbar + 1
        print('touch10 No goal',score_with_postbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch11 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch11 / distance) < phi_collect[sim] \
and phi_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch11 / distance)):
        thisrand_6 = random.randint(0,10000-1)
        thisarray_6 = possibility(6)
        count_outcome_6[thisrand_6] = thisarray_6[thisrand_6]
        if count_outcome_6[thisrand_6] == 1:
            score_with_postbar[sim] = 1
            print('touch11 goal',score_with_postbar)
            count_with_postsbar = count_with_postsbar + 1
        print('touch11 No goal',score_with_postbar)
            
    elif theta_collect[sim] < np.arctan(height_bar_touch12 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch12 / distance) < phi_collect[sim] \
and phi_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch12 / distance)):
        thisrand_5 = random.randint(0,10000-1)
        thisarray_5 = possibility(5)
        count_outcome_5[thisrand_5] = thisarray_5[thisrand_5]
        if count_outcome_5[thisrand_5] == 1:
            score_with_postbar[sim] = 1
            print('touch12 goal',score_with_postbar)
            count_with_postsbar = count_with_postsbar + 1
        print('touch12 No goal',score_with_postbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch13 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch13 / distance) < phi_collect[sim] \
and phi_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch13 / distance)):
        thisrand_4 = random.randint(0,10000-1)
        thisarray_4 = possibility(4)
        count_outcome_4[thisrand_4] = thisarray_4[thisrand_4]
        if count_outcome_4[thisrand_4] == 1:
            score_with_postbar[sim] = 1
            print('touch13 goal',score_with_postbar)
            count_with_postsbar = count_with_postsbar + 1
        print('touch13 No goal',score_with_postbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch14 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch14 / distance) < phi_collect[sim] \
and phi_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch14 / distance)):
        thisrand_3 = random.randint(0,10000-1)
        thisarray_3 = possibility(3)
        count_outcome_3[thisrand_3] = thisarray_3[thisrand_3]
        if count_outcome_3[thisrand_3] == 1:
            score_with_postbar[sim] = 1
            print('touch14 goal',score_with_postbar)
            count_with_postsbar = count_with_postsbar + 1
        print('touch14 No goal',score_with_postbar)  
        
    elif theta_collect[sim] < np.arctan(height_bar_touch15 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch15 / distance) < phi_collect[sim] \
and phi_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch15 / distance)):
        thisrand_2 = random.randint(0,10000-1)
        thisarray_2 = possibility(2)
        count_outcome_2[thisrand_2] = thisarray_2[thisrand_2]
        if count_outcome_2[thisrand_2] == 1:
            score_with_postbar[sim] = 1
            print('touch15 goal',score_with_postbar)
            count_with_postsbar = count_with_postsbar + 1
        print('touch15 No goal',score_with_postbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch16 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch16 / distance) < phi_collect[sim] \
and phi_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch16 / distance)):
        thisrand_1 = random.randint(0,10000-1)
        thisarray_1 = possibility(1)
        count_outcome_1[thisrand_1] = thisarray_1[thisrand_1]
        if count_outcome_1[thisrand_1] == 1:
            score_with_postbar[sim] = 1
            print('touch16 goal',score_with_postbar)
            count_with_postsbar = count_with_postsbar + 1
        print('touch16 No goal',score_with_postbar)
        
    else:
        score_with_postbar[sim] = 0
        print('No goal',score_with_postbar)
#     elif theta_collect[sim] < np.arctan(height_bar_touch17 / distance) \
# and (const.pi/2 - np.arctan(half_w_post_touch1 / distance) < phi_collect[sim] \
# and phi_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch1 / distance)):
#         thisrand_1 = random.randint(0,10000-1)
#         thisarray_1 = possibility(1)
#         count_outcome_1[thisrand_1] = thisarray_1[thisrand_1]
#         if count_outcome_1[thisrand_1] == 1:
#             score[sim] = 1
#             print(score)
    ####Goal keeper section    
#     if score_with_postbar[sim] == 1:
        
#         random_human_phi_index = random.randint(0,int(range_place_phi_deg*100))
#         random_phi_man_begin = random_human_phi_index /180 * const.pi
#         random_phi_man_end = random_phi_man_begin + range_human_phi
#         random_use_phi_area = random_phi_man_begin+random_phi_man_end 
        
#         delta_phi_man = abs(const.pi/2 - random_use_phi_area/2)
#         distance_man_new = distance / np.cos(delta_phi_man)

#         # possible human theta
#         range_random_human_theta = np.arctan(human_height/distance_man_new)

#         theta_in_goal = np.arctan(height/distance)
#         theta_ratio = theta_in_goal / range_random_human_theta

#         random_human_theta = theta_in_goal - range_random_human_theta 
#         random_human_theta_index = random.randint(0,int(random_human_theta*100))
#         random_theta_man_begin = random_human_theta_index /180 * const.pi
#         random_theta_man_end = random_human_theta_index /180 * const.pi + range_random_human_theta 
        
#         if (random_theta_man_begin <= theta_collect[sim] \
# and theta_collect[sim] <= random_theta_man_end) \
# and (random_phi_man_begin <= phi_all_collect[sim] \
# and phi_all_collect[sim] <= random_phi_man_end):
#             score_with_postbar[sim] = 0
#             score_with_ownpostbar[sim] = 0
#             count_keepersave = count_keepersave + 1
                


print(count_with_postsbar)
# ball with diameter d
print('The fraction of goals in',sim_time,'isotropic events with posts and bar is:', count_with_postsbar/sim_time)





#%%
# How large would the influence of a goalkeeper be, 
# if he or she moves randomly to any position in front of the goal?

################################################################
##human size section in theta and phi
################################################################


human_height = 1.88 #m
human_width = 2*0.782+0.4  #when fully strength =1.964m=196.4cm
human_halfwidth = human_width/2
#lower limit for human stand
stand_theta = np.arctan(human_height/distance)
stand_phi = np.arctan(human_halfwidth/distance)
#phi
phi_human = 2*np.arctan(human_halfwidth/distance)
#theta
theta_human = np.arctan(human_height/distance)

# possible goal phi
begin_goal_phi = const.pi/2 - np.arctan(half_w_directgoal / distance) 
end_goal_phi = const.pi/2 + np.arctan(half_w_directgoal / distance) 
range_goal_phi = end_goal_phi - begin_goal_phi

# possible human phi
begin_human_phi = const.pi/2 - np.arctan(human_halfwidth / distance) 
end_human_phi = const.pi/2 + np.arctan(human_halfwidth / distance) 
range_human_phi = end_human_phi - begin_human_phi

range_ratio = range_goal_phi / range_human_phi 

# possible place area phi
begin_place_phi = begin_goal_phi
end_place_phi = end_goal_phi - range_human_phi
range_place_phi = end_place_phi - begin_place_phi

range_place_phi_deg = range_place_phi / const.pi *180

# print(range_place_phi_deg)
# print(int(range_place_phi_deg*100))


######################################################################
# random_human_phi_index = random.randit(0,int(range_place_phi_deg*100))

# random_phi_man_begin = random_human_phi_index /180 * const.pi

# random_phi_man_end = random_phi_man_begin + range_human_phi

# random_use_phi_area = random_phi_man_begin+random_phi_man_end 

######################################################################

####################################################################################
# determine thefunction of theta to phi
# delta_phi_man = abs(const.pi/2 - random_use_phi_area/2)
# distance_man_new = distance / np.cos(delta_phi_man)

# # possible human theta
# range_random_human_theta = np.arctan(human_height/distance_man_new)

# theta_in_goal = np.arctan(height/distance)
# theta_ratio = theta_in_goal / range_random_human_theta

# # begin theta 0

# random_human_theta = theta_in_goal - range_random_human_theta 
# random_human_theta_index = random.randint(0,int(random_human_theta*100))
# random_theta_man_use = random_human_theta_index /180 * const.pi
####################################################################################
####



#%%
# What is the probability for scoring an own goal?

##Recall###########################################################
# Resize the area of goal
# crossbar and goalpost thickness 12cm
# Goal_PostsBars = 0.12   #12cm=0.12m
# Goal_Height = height - Goal_PostsBars
# Goal_Width = width - Goal_PostsBars
# height_directgoal = Goal_Height - d_ball / 2
# half_w_directgoal = half_width - Goal_PostsBars - d_ball / 2
###################################################################

################################################################
##include own goal section
################################################################

field_distance = 90   #m
long_distance = field_distance - distance #90-11=79
# theta_own = np.arctan(height / long_distance)
phi_own = np.arctan(half_w_directgoal / long_distance)

count_own = np.zeros(1)
owngoal = np.zeros(sim_time)

for sim in range(0,sim_time):
    #### The goal range: Theta as a function of phi
    delta_phi = abs(3*const.pi/2 - phi_all_collect[sim])
    # use absolute value above
    long_distance_new = long_distance / np.cos(delta_phi)
    theta_own = np.arctan(height / long_distance_new)
    
    if theta_collect[sim] <= theta_own \
and (3*const.pi/2 - phi_own <= phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + phi_own):
        owngoal[sim] = 1
        print(owngoal)
        count_own = count_own + 1
        print(count_own)

print('Own goal percentage when isotropically shoot in any phi direction:', count_own/sim_time)
#%% own goal
### also with goalkeeper
# For phi in all direction
# with posts and bar in goal area

# Goal_Height = height - Goal_PostsBars
# Goal_Width = width - Goal_PostsBars
# height_directgoal = Goal_Height - d_ball / 2
# half_w_directgoal = half_width - Goal_PostsBars - d_ball / 2
count_with_ownpostsbar = np.zeros(1)
score_with_ownpostbar = np.zeros(sim_time)
count_keepersave = np.zeros(1)
count_with_allpostsbar = np.zeros(1)
score_with_allpostbar = np.zeros(sim_time)

for sim in range(0,sim_time):
    
    print('event:',sim+1)
    #### The goal range: Theta as a function of phi
    delta_phi = abs(const.pi/2 - phi_all_collect[sim])
    # use absolute value above
    distance_new = distance / np.cos(delta_phi)
    
    delta_own_phi = abs(3*const.pi/2 - phi_all_collect[sim])
    # use absolute value above
    distance_own_new = long_distance / np.cos(delta_own_phi)
    
    if theta_collect[sim] <= np.arctan(height_directgoal / distance_new) \
and (const.pi/2 - np.arctan(half_w_directgoal / distance) <= phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_directgoal / distance)):
        score_with_allpostbar[sim] = 1
        print('direct goal',score_with_allpostbar)
        count_with_allpostsbar = count_with_allpostsbar + 1
        
    elif theta_collect[sim] < np.arctan(height_bar_touch1 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch1 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch1 / distance)):
        thisrand_16 = random.randint(0,10000-1)
        thisarray_16 = possibility(16)
        count_outcome_16[thisrand_16] = thisarray_16[thisrand_16]
        if count_outcome_16[thisrand_16] == 1:
            score_with_allpostbar[sim] = 1
            print('touch1 goal',score_with_allpostbar)
            count_with_allpostsbar = count_with_allpostsbar + 1
        print('touch1 No goal',score_with_allpostbar)
            
    elif theta_collect[sim] < np.arctan(height_bar_touch2 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch2 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch2 / distance)):
        thisrand_15 = random.randint(0,10000-1)
        thisarray_15 = possibility(15)
        count_outcome_15[thisrand_15] = thisarray_15[thisrand_15]
        if count_outcome_15[thisrand_15] == 1:
            score_with_allpostbar[sim] = 1
            print('touch2 goal',score_with_allpostbar)
            count_with_allpostsbar = count_with_allpostsbar + 1
        print('touch2 No goal',score_with_allpostbar)
            
    elif theta_collect[sim] < np.arctan(height_bar_touch3 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch3 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch3 / distance)):
        thisrand_14 = random.randint(0,10000-1)
        thisarray_14 = possibility(14)
        count_outcome_14[thisrand_14] = thisarray_14[thisrand_14]
        if count_outcome_14[thisrand_14] == 1:
            score_with_allpostbar[sim] = 1
            print('touch3 goal',score_with_allpostbar)
            count_with_allpostsbar = count_with_allpostsbar + 1
        print('touch3 No goal',score_with_allpostbar)
            
    elif theta_collect[sim] < np.arctan(height_bar_touch4 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch4 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch4 / distance)):
        thisrand_13 = random.randint(0,10000-1)
        thisarray_13 = possibility(13)
        count_outcome_13[thisrand_13] = thisarray_13[thisrand_13]
        if count_outcome_13[thisrand_13] == 1:
            score_with_allpostbar[sim] = 1
            print('touch4 goal',score_with_allpostbar)
            count_with_allpostsbar = count_with_allpostsbar + 1
        print('touch4 No goal',score_with_allpostbar)    
        
    elif theta_collect[sim] < np.arctan(height_bar_touch5 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch5 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch5 / distance)):
        thisrand_12 = random.randint(0,10000-1)
        thisarray_12 = possibility(12)
        count_outcome_12[thisrand_12] = thisarray_12[thisrand_12]
        if count_outcome_12[thisrand_12] == 1:
            score_with_allpostbar[sim] = 1
            print('touch5 goal',score_with_allpostbar)
            count_with_allpostsbar = count_with_allpostsbar + 1
        print('touch5 No goal',score_with_allpostbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch6 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch6 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch6 / distance)):
        thisrand_11 = random.randint(0,10000-1)
        thisarray_11 = possibility(11)
        count_outcome_11[thisrand_11] = thisarray_11[thisrand_11]
        if count_outcome_11[thisrand_11] == 1:
            score_with_allpostbar[sim] = 1
            print('touch6 goal',score_with_allpostbar)
            count_with_allpostsbar = count_with_allpostsbar + 1
        print('touch6 No goal',score_with_allpostbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch7 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch7 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch7 / distance)):
        thisrand_10 = random.randint(0,10000-1)
        thisarray_10 = possibility(10)
        count_outcome_10[thisrand_10] = thisarray_10[thisrand_10]
        if count_outcome_10[thisrand_10] == 1:
            score_with_allpostbar[sim] = 1
            print('touch7 goal',score_with_allpostbar)
            count_with_allpostsbar = count_with_allpostsbar + 1
        print('touch7 No goal',score_with_allpostbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch8 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch8 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch8 / distance)):
        thisrand_9 = random.randint(0,10000-1)
        thisarray_9 = possibility(9)
        count_outcome_9[thisrand_9] = thisarray_9[thisrand_9]
        if count_outcome_9[thisrand_9] == 1:
            score_with_allpostbar[sim] = 1
            print('touch8 goal',score_with_allpostbar)
            count_with_allpostsbar = count_with_allpostsbar + 1
        print('touch8 No goal',score_with_allpostbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch9 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch9 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch9 / distance)):
        thisrand_8 = random.randint(0,10000-1)
        thisarray_8 = possibility(8)
        count_outcome_8[thisrand_8] = thisarray_8[thisrand_8]
        if count_outcome_8[thisrand_8] == 1:
            score_with_allpostbar[sim] = 1
            print('touch9 goal',score_with_allpostbar)
            count_with_allpostsbar = count_with_allpostsbar + 1
        print('touch9 No goal',score_with_allpostbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch10 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch10 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch10 / distance)):
        thisrand_7 = random.randint(0,10000-1)
        thisarray_7 = possibility(7)
        count_outcome_7[thisrand_7] = thisarray_7[thisrand_7]
        if count_outcome_7[thisrand_7] == 1:
            score_with_allpostbar[sim] = 1
            print('touch10 goal',score_with_allpostbar)
            count_with_allpostsbar = count_with_allpostsbar + 1
        print('touch10 No goal',score_with_allpostbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch11 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch11 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch11 / distance)):
        thisrand_6 = random.randint(0,10000-1)
        thisarray_6 = possibility(6)
        count_outcome_6[thisrand_6] = thisarray_6[thisrand_6]
        if count_outcome_6[thisrand_6] == 1:
            score_with_allpostbar[sim] = 1
            print('touch11 goal',score_with_allpostbar)
            count_with_allpostsbar = count_with_allpostsbar + 1
        print('touch11 No goal',score_with_allpostbar)
            
    elif theta_collect[sim] < np.arctan(height_bar_touch12 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch12 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch12 / distance)):
        thisrand_5 = random.randint(0,10000-1)
        thisarray_5 = possibility(5)
        count_outcome_5[thisrand_5] = thisarray_5[thisrand_5]
        if count_outcome_5[thisrand_5] == 1:
            score_with_allpostbar[sim] = 1
            print('touch12 goal',score_with_allpostbar)
            count_with_allpostsbar = count_with_allpostsbar + 1
        print('touch12 No goal',score_with_allpostbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch13 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch13 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch13 / distance)):
        thisrand_4 = random.randint(0,10000-1)
        thisarray_4 = possibility(4)
        count_outcome_4[thisrand_4] = thisarray_4[thisrand_4]
        if count_outcome_4[thisrand_4] == 1:
            score_with_allpostbar[sim] = 1
            print('touch13 goal',score_with_allpostbar)
            count_with_allpostsbar = count_with_allpostsbar + 1
        print('touch13 No goal',score_with_allpostbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch14 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch14 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch14 / distance)):
        thisrand_3 = random.randint(0,10000-1)
        thisarray_3 = possibility(3)
        count_outcome_3[thisrand_3] = thisarray_3[thisrand_3]
        if count_outcome_3[thisrand_3] == 1:
            score_with_allpostbar[sim] = 1
            print('touch14 goal',score_with_allpostbar)
            count_with_allpostsbar = count_with_allpostsbar + 1
        print('touch14 No goal',score_with_allpostbar)  
        
    elif theta_collect[sim] < np.arctan(height_bar_touch15 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch15 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch15 / distance)):
        thisrand_2 = random.randint(0,10000-1)
        thisarray_2 = possibility(2)
        count_outcome_2[thisrand_2] = thisarray_2[thisrand_2]
        if count_outcome_2[thisrand_2] == 1:
            score_with_allpostbar[sim] = 1
            print('touch15 goal',score_with_allpostbar)
            count_with_allpostsbar = count_with_allpostsbar + 1
        print('touch15 No goal',score_with_allpostbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch16 / distance_new) \
and (const.pi/2 - np.arctan(half_w_post_touch16 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch16 / distance)):
        thisrand_1 = random.randint(0,10000-1)
        thisarray_1 = possibility(1)
        count_outcome_1[thisrand_1] = thisarray_1[thisrand_1]
        if count_outcome_1[thisrand_1] == 1:
            score_with_allpostbar[sim] = 1
            print('touch16 goal',score_with_allpostbar)
            count_with_allpostsbar = count_with_allpostsbar + 1
        print('touch16 No goal',score_with_allpostbar)
        
    ###################################################################
    # own goal section    
    # delta_own_phi = abs(3*const.pi/2 - phi_all_collect[sim])
    # # use absolute value above
    # distance_own_new = distance / np.cos(delta_own_phi)
    
    elif theta_collect[sim] <= theta_own \
and (3*const.pi/2 - phi_own <= phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + phi_own):
        score_with_ownpostbar[sim] = 1
        print('direct own goal',score_with_ownpostbar)
        # print(score_with_ownpostbar)
        count_with_ownpostsbar = count_with_ownpostsbar + 1
        # print(count_with_ownpostsbar)
    
    elif theta_collect[sim] < np.arctan(height_bar_touch1 / distance_own_new) \
and (3*const.pi/2 - np.arctan(half_w_post_touch1 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch1 / long_distance)):
        thisrand_16 = random.randint(0,10000-1)
        thisarray_16 = possibility(16)
        count_outcome_16[thisrand_16] = thisarray_16[thisrand_16]
        if count_outcome_16[thisrand_16] == 1:
            score_with_ownpostbar[sim] = 1
            print('touch1 own goal',score_with_ownpostbar)
            count_with_ownpostsbar = count_with_ownpostsbar + 1
        print('touch1 No own goal',score_with_ownpostbar)
            
    elif theta_collect[sim] < np.arctan(height_bar_touch2 / distance_own_new) \
and (3*const.pi/2 - np.arctan(half_w_post_touch2 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch2 / long_distance)):
        thisrand_15 = random.randint(0,10000-1)
        thisarray_15 = possibility(15)
        count_outcome_15[thisrand_15] = thisarray_15[thisrand_15]
        if count_outcome_15[thisrand_15] == 1:
            score_with_ownpostbar[sim] = 1
            print('touch2 owngoal',score_with_ownpostbar)
            count_with_ownpostsbar = count_with_ownpostsbar + 1
        print('touch2 No owngoal',score_with_ownpostbar)
            
    elif theta_collect[sim] < np.arctan(height_bar_touch3 / distance_own_new) \
and (3*const.pi/2 - np.arctan(half_w_post_touch3 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch3 / long_distance)):
        thisrand_14 = random.randint(0,10000-1)
        thisarray_14 = possibility(14)
        count_outcome_14[thisrand_14] = thisarray_14[thisrand_14]
        if count_outcome_14[thisrand_14] == 1:
            score_with_ownpostbar[sim] = 1
            print('touch3 owngoal',score_with_ownpostbar)
            count_with_ownpostsbar = count_with_ownpostsbar + 1
        print('touch3 No owngoal',score_with_ownpostbar)
            
    elif theta_collect[sim] < np.arctan(height_bar_touch4 / distance_own_new) \
and (3*const.pi/2 - np.arctan(half_w_post_touch4 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch4 / long_distance)):
        thisrand_13 = random.randint(0,10000-1)
        thisarray_13 = possibility(13)
        count_outcome_13[thisrand_13] = thisarray_13[thisrand_13]
        if count_outcome_13[thisrand_13] == 1:
            score_with_ownpostbar[sim] = 1
            print('touch4 owngoal',score_with_ownpostbar)
            count_with_ownpostsbar = count_with_ownpostsbar + 1
        print('touch4 No owngoal',score_with_ownpostbar)    
        
    elif theta_collect[sim] < np.arctan(height_bar_touch5 / distance_own_new) \
and (3*const.pi/2 - np.arctan(half_w_post_touch5 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch5 / long_distance)):
        thisrand_12 = random.randint(0,10000-1)
        thisarray_12 = possibility(12)
        count_outcome_12[thisrand_12] = thisarray_12[thisrand_12]
        if count_outcome_12[thisrand_12] == 1:
            score_with_ownpostbar[sim] = 1
            print('touch5 owngoal',score_with_ownpostbar)
            count_with_ownpostsbar = count_with_ownpostsbar + 1
        print('touch5 No owngoal',score_with_ownpostbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch6 / distance_own_new) \
and (3*const.pi/2 - np.arctan(half_w_post_touch6 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch6 / long_distance)):
        thisrand_11 = random.randint(0,10000-1)
        thisarray_11 = possibility(11)
        count_outcome_11[thisrand_11] = thisarray_11[thisrand_11]
        if count_outcome_11[thisrand_11] == 1:
            score_with_ownpostbar[sim] = 1
            print('touch6 owngoal',score_with_ownpostbar)
            count_with_ownpostsbar = count_with_ownpostsbar + 1
        print('touch6 No owngoal',score_with_ownpostbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch7 / distance_own_new) \
and (3*const.pi/2 - np.arctan(half_w_post_touch7 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch7 / long_distance)):
        thisrand_10 = random.randint(0,10000-1)
        thisarray_10 = possibility(10)
        count_outcome_10[thisrand_10] = thisarray_10[thisrand_10]
        if count_outcome_10[thisrand_10] == 1:
            score_with_ownpostbar[sim] = 1
            print('touch7 owngoal',score_with_ownpostbar)
            count_with_ownpostsbar = count_with_ownpostsbar + 1
        print('touch7 No owngoal',score_with_ownpostbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch8 / distance_own_new) \
and (3*const.pi/2 - np.arctan(half_w_post_touch8 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch8 / long_distance)):
        thisrand_9 = random.randint(0,10000-1)
        thisarray_9 = possibility(9)
        count_outcome_9[thisrand_9] = thisarray_9[thisrand_9]
        if count_outcome_9[thisrand_9] == 1:
            score_with_ownpostbar[sim] = 1
            print('touch8 owngoal',score_with_ownpostbar)
            count_with_ownpostsbar = count_with_ownpostsbar + 1
        print('touch8 No owngoal',score_with_ownpostbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch9 / distance_own_new) \
and (3*const.pi/2 - np.arctan(half_w_post_touch9 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch9 / long_distance)):
        thisrand_8 = random.randint(0,10000-1)
        thisarray_8 = possibility(8)
        count_outcome_8[thisrand_8] = thisarray_8[thisrand_8]
        if count_outcome_8[thisrand_8] == 1:
            score_with_ownpostbar[sim] = 1
            print('touch9 owngoal',score_with_ownpostbar)
            count_with_ownpostsbar = count_with_ownpostsbar + 1
        print('touch9 No owngoal',score_with_ownpostbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch10 / distance_own_new) \
and (3*const.pi/2 - np.arctan(half_w_post_touch10 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch10 / long_distance)):
        thisrand_7 = random.randint(0,10000-1)
        thisarray_7 = possibility(7)
        count_outcome_7[thisrand_7] = thisarray_7[thisrand_7]
        if count_outcome_7[thisrand_7] == 1:
            score_with_ownpostbar[sim] = 1
            print('touch10 owngoal',score_with_ownpostbar)
            count_with_ownpostsbar = count_with_ownpostsbar + 1
        print('touch10 No owngoal',score_with_ownpostbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch11 / distance_own_new) \
and (3*const.pi/2 - np.arctan(half_w_post_touch11 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch11 / long_distance)):
        thisrand_6 = random.randint(0,10000-1)
        thisarray_6 = possibility(6)
        count_outcome_6[thisrand_6] = thisarray_6[thisrand_6]
        if count_outcome_6[thisrand_6] == 1:
            score_with_ownpostbar[sim] = 1
            print('touch11 owngoal',score_with_ownpostbar)
            count_with_ownpostsbar = count_with_ownpostsbar + 1
        print('touch11 No owngoal',score_with_ownpostbar)
            
    elif theta_collect[sim] < np.arctan(height_bar_touch12 / distance_own_new) \
and (3*const.pi/2 - np.arctan(half_w_post_touch12 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch12 / long_distance)):
        thisrand_5 = random.randint(0,10000-1)
        thisarray_5 = possibility(5)
        count_outcome_5[thisrand_5] = thisarray_5[thisrand_5]
        if count_outcome_5[thisrand_5] == 1:
            score_with_ownpostbar[sim] = 1
            print('touch12 owngoal',score_with_ownpostbar)
            count_with_ownpostsbar = count_with_ownpostsbar + 1
        print('touch12 No owngoal',score_with_ownpostbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch13 / distance_own_new) \
and (3*const.pi/2 - np.arctan(half_w_post_touch13 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch13 / long_distance)):
        thisrand_4 = random.randint(0,10000-1)
        thisarray_4 = possibility(4)
        count_outcome_4[thisrand_4] = thisarray_4[thisrand_4]
        if count_outcome_4[thisrand_4] == 1:
            score_with_ownpostbar[sim] = 1
            print('touch13 owngoal',score_with_ownpostbar)
            count_with_ownpostsbar = count_with_ownpostsbar + 1
        print('touch13 No owngoal',score_with_ownpostbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch14 / distance_own_new) \
and (3*const.pi/2 - np.arctan(half_w_post_touch14 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch14 / long_distance)):
        thisrand_3 = random.randint(0,10000-1)
        thisarray_3 = possibility(3)
        count_outcome_3[thisrand_3] = thisarray_3[thisrand_3]
        if count_outcome_3[thisrand_3] == 1:
            score_with_ownpostbar[sim] = 1
            print('touch14 owngoal',score_with_ownpostbar)
            count_with_ownpostsbar = count_with_ownpostsbar + 1
        print('touch14 No owngoal',score_with_ownpostbar)  
        
    elif theta_collect[sim] < np.arctan(height_bar_touch15 / distance_own_new) \
and (3*const.pi/2 - np.arctan(half_w_post_touch15 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch15 / long_distance)):
        thisrand_2 = random.randint(0,10000-1)
        thisarray_2 = possibility(2)
        count_outcome_2[thisrand_2] = thisarray_2[thisrand_2]
        if count_outcome_2[thisrand_2] == 1:
            score_with_ownpostbar[sim] = 1
            print('touch15 owngoal',score_with_ownpostbar)
            count_with_ownpostsbar = count_with_ownpostsbar + 1
        print('touch15 No owngoal',score_with_ownpostbar)
        
    elif theta_collect[sim] < np.arctan(height_bar_touch16 / distance_own_new) \
and (3*const.pi/2 - np.arctan(half_w_post_touch16 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch16 / long_distance)):
        thisrand_1 = random.randint(0,10000-1)
        thisarray_1 = possibility(1)
        count_outcome_1[thisrand_1] = thisarray_1[thisrand_1]
        if count_outcome_1[thisrand_1] == 1:
            score_with_ownpostbar[sim] = 1
            print('touch16 owngoal',score_with_ownpostbar)
            count_with_ownpostsbar = count_with_ownpostsbar + 1
        print('touch16 No owngoal',score_with_ownpostbar)
        
    # no goal
    else:
        score_with_postbar[sim] = 0
        print('No goal',score_with_postbar)
#     elif theta_collect[sim] < np.arctan(height_bar_touch17 / distance) \
# and (const.pi/2 - np.arctan(half_w_post_touch1 / distance) < phi_collect[sim] \
# and phi_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch1 / distance)):
#         thisrand_1 = random.randint(0,10000-1)
#         thisarray_1 = possibility(1)
#         count_outcome_1[thisrand_1] = thisarray_1[thisrand_1]
#         if count_outcome_1[thisrand_1] == 1:
#             score[sim] = 1
#             print(score)
####Goal keeper section    
    if score_with_postbar[sim] == 1: #or score_with_ownpostbar[sim] == 1:
        
        random_human_phi_index = random.randint(0,int(range_place_phi_deg*100))
        random_phi_man_begin = random_human_phi_index /180 * const.pi
        random_phi_man_end = random_phi_man_begin + range_human_phi
        random_use_phi_area = random_phi_man_begin+random_phi_man_end 
        
        delta_phi_man = abs(const.pi/2 - random_use_phi_area/2)
        distance_man_new = distance / np.cos(delta_phi_man)

        # possible human theta
        range_random_human_theta = np.arctan(human_height/distance_man_new)

        theta_in_goal = np.arctan(height_directgoal/distance)
        theta_ratio = theta_in_goal / range_random_human_theta

        random_human_theta = (theta_in_goal - range_random_human_theta)/ const.pi *180
        random_human_theta_index = random.randint(0,int(random_human_theta*100))
        random_theta_man_begin = random_human_theta_index /180 * const.pi
        random_theta_man_end = random_human_theta_index /180 * const.pi + range_random_human_theta 
        
        if (random_theta_man_begin <= theta_collect[sim] \
and theta_collect[sim] <= random_theta_man_end) \
and (random_phi_man_begin <= phi_all_collect[sim] \
and phi_all_collect[sim] <= random_phi_man_end):
            score_with_allpostbar[sim] = 0
            # score_with_ownpostbar[sim] = 0
            count_with_allpostsbar = count_with_postsbar - 1
            count_keepersave = count_keepersave + 1
                
    

print(count_with_postsbar)
# ball with diameter d
print('The fraction of goals in',sim_time,'isotropic events with posts and bar is:', count_with_allpostsbar/sim_time)
print('Own goals percentage in',sim_time,' isotropic events with posts and bar is:', count_with_ownpostsbar/sim_time)
print('Goals saved by keeper percentage in',sim_time,' isotropic events with posts and bar is:', count_keepersave/sim_time)


#%% There is gravity.

v_avg = 31.29  # m/s

ch_save = np.zeros(244)
ch_save2 = np.zeros(244)
height_t = height_directgoal #2.44
ch = 0
for go in  range(0,244):
    ch = ch+0.01
    sup_1 = v_avg**2+np.sqrt(v_avg**4-const.g*(const.g*distance**2+2*ch*v_avg**2))
    sup_2 = v_avg**2-np.sqrt(v_avg**4-const.g*(const.g*distance**2+2*ch*v_avg**2))
    sub = const.g * distance
    theta_g1 = np.arctan(sup_1 / sub)
    theta_g2 = np.arctan(sup_2 / sub)
    ch_save[go]=theta_g1 / const.pi *180
    ch_save2[go]= theta_g2 /const.pi * 180
# print(const.g)
#%%
plt.figure() 
plt.hist(ch_save)
# plt.xlim(0, 1, 1)
plt.savefig('theta_g1.png')
plt.show()

plt.figure() 
plt.hist(ch_save2)
# plt.xlim(0, 1, 1)
plt.savefig('theta_g2.png')
plt.show()

print(theta_in_goal/const.pi*180,theta_g1/const.pi*180,theta_g2/const.pi*180)
# area = 0 ~ theta_g2(h) ort heta_g1(0~h)

#%%
## perform shoot with gravity
## affect theta for each phi

count_with_ownpostsbar_g = np.zeros(1)
score_with_ownpostbar_g = np.zeros(sim_time)
count_keepersave_g = np.zeros(1)
count_with_postsbar_g = np.zeros(1)
score_with_postbar_g = np.zeros(sim_time)


def sups1(h):
    sup = v_avg**2+np.sqrt(v_avg**4-const.g*(const.g*distance_new**2+2*h*v_avg**2))
    return sup
def sups2(h):
    sup = v_avg**2-np.sqrt(v_avg**4-const.g*(const.g*distance_new**2+2*h*v_avg**2))
    return sup
def ownsups1(h):
    sup = v_avg**2+np.sqrt(v_avg**4-const.g*(const.g*distance_own_new**2+2*h*v_avg**2))
    return sup
def ownsups2(h):
    sup = v_avg**2-np.sqrt(v_avg**4-const.g*(const.g*distance_own_new**2+2*h*v_avg**2))
    return sup
def sups1d(d,h):
    sup = v_avg**2+np.sqrt(v_avg**4-const.g*(const.g*d**2+2*h*v_avg**2))
    return sup
def sups2d(d,h):
    sup = v_avg**2-np.sqrt(v_avg**4-const.g*(const.g*d**2+2*h*v_avg**2))
    return sup

for sim in range(0,sim_time):
    
    print('event:',sim+1)
    #### The goal range: Theta as a function of phi
    delta_phi = abs(const.pi/2 - phi_all_collect[sim])
    # use absolute value above
    distance_new = distance / np.cos(delta_phi)
    
    delta_own_phi = abs(3*const.pi/2 - phi_all_collect[sim])
    # use absolute value above
    distance_own_new = long_distance / np.cos(delta_own_phi)
    
    sups_1 = v_avg**2+np.sqrt(v_avg**4-const.g*(const.g*distance_new**2+2*height_directgoal*v_avg**2))
    sup0_1 = v_avg**2+np.sqrt(v_avg**4-const.g*(const.g*distance_new**2+2*0*v_avg**2))
    sups_2 = v_avg**2-np.sqrt(v_avg**4-const.g*(const.g*distance_new**2+2*height_directgoal*v_avg**2))
    subs = const.g * distance_new
    theta_g1s = np.arctan(sups_1 / subs)
    theta_g10 = np.arctan(sup0_1 / subs)
    theta_g2s = np.arctan(sups_2 / subs)
    
    ownsups_1 = v_avg**2+np.sqrt(v_avg**4-const.g*(const.g*distance_own_new**2+2*height_directgoal*v_avg**2))
    ownsup0_1 = v_avg**2+np.sqrt(v_avg**4-const.g*(const.g*distance_own_new**2+2*0*v_avg**2))
    ownsups_2 = v_avg**2-np.sqrt(v_avg**4-const.g*(const.g*distance_own_new**2+2*height_directgoal*v_avg**2))
    ownsubs = const.g * distance_own_new
    owntheta_g1s = np.arctan(ownsups_1 / ownsubs)
    owntheta_g10 = np.arctan(ownsup0_1 / ownsubs)
    owntheta_g2s = np.arctan(ownsups_2 / ownsubs)
    
    
    
    # area = 0 ~ theta_g2(h) or theta_g1(0~h)
    if (theta_collect[sim] <= theta_g2s or (theta_g10 <= theta_collect[sim] and theta_collect[sim] <= theta_g1s)) \
and (const.pi/2 - np.arctan(half_w_directgoal / distance) <= phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_directgoal / distance)):
        score_with_postbar_g[sim] = 1
        print('direct goal',score_with_postbar)
        count_with_postsbar_g = count_with_postsbar_g + 1
        
    elif (theta_collect[sim] < np.arctan(sups2(height_bar_touch1) / subs) \
or (theta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(sups1(height_bar_touch1) / subs))) \
and (const.pi/2 - np.arctan(half_w_post_touch1 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch1 / distance)):
        thisrand_16 = random.randint(0,10000-1)
        thisarray_16 = possibility(16)
        count_outcome_16[thisrand_16] = thisarray_16[thisrand_16]
        if count_outcome_16[thisrand_16] == 1:
            score_with_postbar_g[sim] = 1
            print('touch1 goal',score_with_postbar_g)
            count_with_postsbar_g = count_with_postsbar_g + 1
        print('touch1 No goal',score_with_postbar_g)
            
    elif (theta_collect[sim] < np.arctan(sups2(height_bar_touch2) / subs) \
or (theta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(sups1(height_bar_touch2) / subs))) \
and (const.pi/2 - np.arctan(half_w_post_touch2 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch2 / distance)):
        thisrand_15 = random.randint(0,10000-1)
        thisarray_15 = possibility(15)
        count_outcome_15[thisrand_15] = thisarray_15[thisrand_15]
        if count_outcome_15[thisrand_15] == 1:
            score_with_postbar_g[sim] = 1
            print('touch2 goal',score_with_postbar_g)
            count_with_postsbar_g = count_with_postsbar_g + 1
        print('touch2 No goal',score_with_postbar_g)
            
    elif (theta_collect[sim] < np.arctan(sups2(height_bar_touch3) / subs) \
or (theta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(sups1(height_bar_touch3) / subs))) \
and (const.pi/2 - np.arctan(half_w_post_touch3 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch3 / distance)):
        thisrand_14 = random.randint(0,10000-1)
        thisarray_14 = possibility(14)
        count_outcome_14[thisrand_14] = thisarray_14[thisrand_14]
        if count_outcome_14[thisrand_14] == 1:
            score_with_postbar_g[sim] = 1
            print('touch3 goal',score_with_postbar_g)
            count_with_postsbar_g = count_with_postsbar_g + 1
        print('touch3 No goal',score_with_postbar_g)
            
    elif (theta_collect[sim] < np.arctan(sups2(height_bar_touch4) / subs) \
or (theta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(sups1(height_bar_touch4) / subs))) \
and (const.pi/2 - np.arctan(half_w_post_touch4 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch4 / distance)):
        thisrand_13 = random.randint(0,10000-1)
        thisarray_13 = possibility(13)
        count_outcome_13[thisrand_13] = thisarray_13[thisrand_13]
        if count_outcome_13[thisrand_13] == 1:
            score_with_postbar_g[sim] = 1
            print('touch4 goal',score_with_postbar_g)
            count_with_postsbar_g = count_with_postsbar_g + 1
        print('touch4 No goal',score_with_postbar_g)    
        
    elif (theta_collect[sim] < np.arctan(sups2(height_bar_touch5) / subs) \
or (theta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(sups1(height_bar_touch5) / subs))) \
and (const.pi/2 - np.arctan(half_w_post_touch5 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch5 / distance)):
        thisrand_12 = random.randint(0,10000-1)
        thisarray_12 = possibility(12)
        count_outcome_12[thisrand_12] = thisarray_12[thisrand_12]
        if count_outcome_12[thisrand_12] == 1:
            score_with_postbar_g[sim] = 1
            print('touch5 goal',score_with_postbar_g)
            count_with_postsbar_g = count_with_postsbar_g + 1
        print('touch5 No goal',score_with_postbar_g)
        
    elif (theta_collect[sim] < np.arctan(sups2(height_bar_touch6) / subs) \
or (theta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(sups1(height_bar_touch6) / subs))) \
and (const.pi/2 - np.arctan(half_w_post_touch6 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch6 / distance)):
        thisrand_11 = random.randint(0,10000-1)
        thisarray_11 = possibility(11)
        count_outcome_11[thisrand_11] = thisarray_11[thisrand_11]
        if count_outcome_11[thisrand_11] == 1:
            score_with_postbar_g[sim] = 1
            print('touch6 goal',score_with_postbar_g)
            count_with_postsbar_g = count_with_postsbar_g + 1
        print('touch6 No goal',score_with_postbar_g)
        
    elif (theta_collect[sim] < np.arctan(sups2(height_bar_touch7) / subs) \
or (theta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(sups1(height_bar_touch7) / subs))) \
and (const.pi/2 - np.arctan(half_w_post_touch7 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch7 / distance)):
        thisrand_10 = random.randint(0,10000-1)
        thisarray_10 = possibility(10)
        count_outcome_10[thisrand_10] = thisarray_10[thisrand_10]
        if count_outcome_10[thisrand_10] == 1:
            score_with_postbar_g[sim] = 1
            print('touch7 goal',score_with_postbar_g)
            count_with_postsbar_g = count_with_postsbar_g + 1
        print('touch7 No goal',score_with_postbar_g)
        
    elif (theta_collect[sim] < np.arctan(sups2(height_bar_touch8) / subs) \
or (theta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(sups1(height_bar_touch8) / subs))) \
and (const.pi/2 - np.arctan(half_w_post_touch8 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch8 / distance)):
        thisrand_9 = random.randint(0,10000-1)
        thisarray_9 = possibility(9)
        count_outcome_9[thisrand_9] = thisarray_9[thisrand_9]
        if count_outcome_9[thisrand_9] == 1:
            score_with_postbar_g[sim] = 1
            print('touch8 goal',score_with_postbar_g)
            count_with_postsbar_g = count_with_postsbar_g + 1
        print('touch8 No goal',score_with_postbar_g)
        
    elif (theta_collect[sim] < np.arctan(sups2(height_bar_touch9) / subs) \
or (theta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(sups1(height_bar_touch9) / subs))) \
and (const.pi/2 - np.arctan(half_w_post_touch9 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch9 / distance)):
        thisrand_8 = random.randint(0,10000-1)
        thisarray_8 = possibility(8)
        count_outcome_8[thisrand_8] = thisarray_8[thisrand_8]
        if count_outcome_8[thisrand_8] == 1:
            score_with_postbar_g[sim] = 1
            print('touch9 goal',score_with_postbar_g)
            count_with_postsbar_g = count_with_postsbar_g + 1
        print('touch9 No goal',score_with_postbar_g)
        
    elif (theta_collect[sim] < np.arctan(sups2(height_bar_touch10) / subs) \
or (theta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(sups1(height_bar_touch10) / subs))) \
and (const.pi/2 - np.arctan(half_w_post_touch10 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch10 / distance)):
        thisrand_7 = random.randint(0,10000-1)
        thisarray_7 = possibility(7)
        count_outcome_7[thisrand_7] = thisarray_7[thisrand_7]
        if count_outcome_7[thisrand_7] == 1:
            score_with_postbar_g[sim] = 1
            print('touch10 goal',score_with_postbar_g)
            count_with_postsbar_g = count_with_postsbar_g + 1
        print('touch10 No goal',score_with_postbar_g)
        
    elif (theta_collect[sim] < np.arctan(sups2(height_bar_touch11) / subs) \
or (theta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(sups1(height_bar_touch11) / subs))) \
and (const.pi/2 - np.arctan(half_w_post_touch11 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch11 / distance)):
        thisrand_6 = random.randint(0,10000-1)
        thisarray_6 = possibility(6)
        count_outcome_6[thisrand_6] = thisarray_6[thisrand_6]
        if count_outcome_6[thisrand_6] == 1:
            score_with_postbar_g[sim] = 1
            print('touch11 goal',score_with_postbar_g)
            count_with_postsbar_g = count_with_postsbar_g + 1
        print('touch11 No goal',score_with_postbar_g)
            
    elif (theta_collect[sim] < np.arctan(sups2(height_bar_touch12) / subs) \
or (theta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(sups1(height_bar_touch12) / subs))) \
and (const.pi/2 - np.arctan(half_w_post_touch12 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch12 / distance)):
        thisrand_5 = random.randint(0,10000-1)
        thisarray_5 = possibility(5)
        count_outcome_5[thisrand_5] = thisarray_5[thisrand_5]
        if count_outcome_5[thisrand_5] == 1:
            score_with_postbar_g[sim] = 1
            print('touch12 goal',score_with_postbar_g)
            count_with_postsbar_g = count_with_postsbar_g + 1
        print('touch12 No goal',score_with_postbar_g)
        
    elif (theta_collect[sim] < np.arctan(sups2(height_bar_touch13) / subs) \
or (theta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(sups1(height_bar_touch13) / subs))) \
and (const.pi/2 - np.arctan(half_w_post_touch13 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch13 / distance)):
        thisrand_4 = random.randint(0,10000-1)
        thisarray_4 = possibility(4)
        count_outcome_4[thisrand_4] = thisarray_4[thisrand_4]
        if count_outcome_4[thisrand_4] == 1:
            score_with_postbar_g[sim] = 1
            print('touch13 goal',score_with_postbar_g)
            count_with_postsbar_g = count_with_postsbar_g + 1
        print('touch13 No goal',score_with_postbar_g)
        
    elif (theta_collect[sim] < np.arctan(sups2(height_bar_touch14) / subs) \
or (theta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(sups1(height_bar_touch14) / subs))) \
and (const.pi/2 - np.arctan(half_w_post_touch14 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch14 / distance)):
        thisrand_3 = random.randint(0,10000-1)
        thisarray_3 = possibility(3)
        count_outcome_3[thisrand_3] = thisarray_3[thisrand_3]
        if count_outcome_3[thisrand_3] == 1:
            score_with_postbar_g[sim] = 1
            print('touch14 goal',score_with_postbar_g)
            count_with_postsbar_g = count_with_postsbar_g + 1
        print('touch14 No goal',score_with_postbar_g)  
        
    elif (theta_collect[sim] < np.arctan(sups2(height_bar_touch15) / subs) \
or (theta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(sups1(height_bar_touch15) / subs))) \
and (const.pi/2 - np.arctan(half_w_post_touch15 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch15 / distance)):
        thisrand_2 = random.randint(0,10000-1)
        thisarray_2 = possibility(2)
        count_outcome_2[thisrand_2] = thisarray_2[thisrand_2]
        if count_outcome_2[thisrand_2] == 1:
            score_with_postbar_g[sim] = 1
            print('touch15 goal',score_with_postbar_g)
            count_with_postsbar_g = count_with_postsbar_g + 1
        print('touch15 No goal',score_with_postbar_g)
        
    elif (theta_collect[sim] < np.arctan(sups2(height_bar_touch16) / subs) \
or (theta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(sups1(height_bar_touch16) / subs))) \
and (const.pi/2 - np.arctan(half_w_post_touch16 / distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch16 / distance)):
        thisrand_1 = random.randint(0,10000-1)
        thisarray_1 = possibility(1)
        count_outcome_1[thisrand_1] = thisarray_1[thisrand_1]
        if count_outcome_1[thisrand_1] == 1:
            score_with_postbar_g[sim] = 1
            print('touch16 goal',score_with_postbar_g)
            count_with_postsbar_g = count_with_postsbar + 1
        print('touch16 No goal',score_with_postbar_g)
        
    ###################################################################
    # own goal section    
    # delta_own_phi = abs(3*const.pi/2 - phi_all_collect[sim])
    # # use absolute value above
    # distance_own_new = distance / np.cos(delta_own_phi)
    
    elif (theta_collect[sim] <= owntheta_g2s \
or (owntheta_g10 <= theta_collect[sim] and theta_collect[sim] <= owntheta_g1s)) \
and (3*const.pi/2 - phi_own <= phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + phi_own):
        score_with_ownpostbar[sim] = 1
        print('direct own goal',score_with_ownpostbar)
        # print(score_with_ownpostbar)
        count_with_ownpostsbar_g = count_with_ownpostsbar_g + 1
        # print(count_with_ownpostsbar)
        
    elif (theta_collect[sim] < np.arctan(ownsups2(height_bar_touch1) / ownsubs) \
or (owntheta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(ownsups1(height_bar_touch1) / subs))) \
and (3*const.pi/2 - np.arctan(half_w_post_touch1 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch1 / long_distance)):
        thisrand_16 = random.randint(0,10000-1)
        thisarray_16 = possibility(16)
        count_outcome_16[thisrand_16] = thisarray_16[thisrand_16]
        if count_outcome_16[thisrand_16] == 1:
            score_with_ownpostbar_g[sim] = 1
            print('touch1 own goal',score_with_ownpostbar_g)
            count_with_ownpostsbar_g = count_with_ownpostsbar_g + 1
        print('touch1 No own goal',score_with_ownpostbar_g)
            
    elif (theta_collect[sim] < np.arctan(ownsups2(height_bar_touch2) / ownsubs) \
or (owntheta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(ownsups1(height_bar_touch2) / subs))) \
and (3*const.pi/2 - np.arctan(half_w_post_touch2 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch2 / long_distance)):
        thisrand_15 = random.randint(0,10000-1)
        thisarray_15 = possibility(15)
        count_outcome_15[thisrand_15] = thisarray_15[thisrand_15]
        if count_outcome_15[thisrand_15] == 1:
            score_with_ownpostbar_g[sim] = 1
            print('touch2 owngoal',score_with_ownpostbar_g)
            count_with_ownpostsbar_g = count_with_ownpostsbar_g + 1
        print('touch2 No owngoal',score_with_ownpostbar_g)
            
    elif (theta_collect[sim] < np.arctan(ownsups2(height_bar_touch3) / ownsubs) \
or (owntheta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(ownsups1(height_bar_touch3) / subs))) \
and (3*const.pi/2 - np.arctan(half_w_post_touch3 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch3 / long_distance)):
        thisrand_14 = random.randint(0,10000-1)
        thisarray_14 = possibility(14)
        count_outcome_14[thisrand_14] = thisarray_14[thisrand_14]
        if count_outcome_14[thisrand_14] == 1:
            score_with_ownpostbar_g[sim] = 1
            print('touch3 owngoal',score_with_ownpostbar_g)
            count_with_ownpostsbar_g = count_with_ownpostsbar_g + 1
        print('touch3 No owngoal',score_with_ownpostbar_g)
            
    elif (theta_collect[sim] < np.arctan(ownsups2(height_bar_touch4) / ownsubs) \
or (owntheta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(ownsups1(height_bar_touch4) / subs))) \
and (3*const.pi/2 - np.arctan(half_w_post_touch4 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch4 / long_distance)):
        thisrand_13 = random.randint(0,10000-1)
        thisarray_13 = possibility(13)
        count_outcome_13[thisrand_13] = thisarray_13[thisrand_13]
        if count_outcome_13[thisrand_13] == 1:
            score_with_ownpostbar_g[sim] = 1
            print('touch4 owngoal',score_with_ownpostbar_g)
            count_with_ownpostsbar_g = count_with_ownpostsbar_g + 1
        print('touch4 No owngoal',score_with_ownpostbar_g)    
        
    elif (theta_collect[sim] < np.arctan(ownsups2(height_bar_touch5) / ownsubs) \
or (owntheta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(ownsups1(height_bar_touch5) / subs))) \
and (3*const.pi/2 - np.arctan(half_w_post_touch5 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch5 / long_distance)):
        thisrand_12 = random.randint(0,10000-1)
        thisarray_12 = possibility(12)
        count_outcome_12[thisrand_12] = thisarray_12[thisrand_12]
        if count_outcome_12[thisrand_12] == 1:
            score_with_ownpostbar_g[sim] = 1
            print('touch5 owngoal',score_with_ownpostbar_g)
            count_with_ownpostsbar_g = count_with_ownpostsbar_g + 1
        print('touch5 No owngoal',score_with_ownpostbar_g)
        
    elif (theta_collect[sim] < np.arctan(ownsups2(height_bar_touch6) / ownsubs) \
or (owntheta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(ownsups1(height_bar_touch6) / subs))) \
and (3*const.pi/2 - np.arctan(half_w_post_touch6 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch6 / long_distance)):
        thisrand_11 = random.randint(0,10000-1)
        thisarray_11 = possibility(11)
        count_outcome_11[thisrand_11] = thisarray_11[thisrand_11]
        if count_outcome_11[thisrand_11] == 1:
            score_with_ownpostbar_g[sim] = 1
            print('touch6 owngoal',score_with_ownpostbar_g)
            count_with_ownpostsbar_g = count_with_ownpostsbar_g + 1
        print('touch6 No owngoal',score_with_ownpostbar_g)
        
    elif (theta_collect[sim] < np.arctan(ownsups2(height_bar_touch7) / ownsubs) \
or (owntheta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(ownsups1(height_bar_touch7) / subs))) \
and (3*const.pi/2 - np.arctan(half_w_post_touch7 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch7 / long_distance)):
        thisrand_10 = random.randint(0,10000-1)
        thisarray_10 = possibility(10)
        count_outcome_10[thisrand_10] = thisarray_10[thisrand_10]
        if count_outcome_10[thisrand_10] == 1:
            score_with_ownpostbar_g[sim] = 1
            print('touch7 owngoal',score_with_ownpostbar_g)
            count_with_ownpostsbar_g = count_with_ownpostsbar_g + 1
        print('touch7 No owngoal',score_with_ownpostbar_g)
        
    elif (theta_collect[sim] < np.arctan(ownsups2(height_bar_touch8) / ownsubs) \
or (owntheta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(ownsups1(height_bar_touch8) / subs))) \
and (3*const.pi/2 - np.arctan(half_w_post_touch8 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch8 / long_distance)):
        thisrand_9 = random.randint(0,10000-1)
        thisarray_9 = possibility(9)
        count_outcome_9[thisrand_9] = thisarray_9[thisrand_9]
        if count_outcome_9[thisrand_9] == 1:
            score_with_ownpostbar_g[sim] = 1
            print('touch8 owngoal',score_with_ownpostbar_g)
            count_with_ownpostsbar_g = count_with_ownpostsbar_g + 1
        print('touch8 No owngoal',score_with_ownpostbar_g)
        
    elif (theta_collect[sim] < np.arctan(ownsups2(height_bar_touch9) / ownsubs) \
or (owntheta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(ownsups1(height_bar_touch9) / subs))) \
and (3*const.pi/2 - np.arctan(half_w_post_touch9 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch9 / long_distance)):
        thisrand_8 = random.randint(0,10000-1)
        thisarray_8 = possibility(8)
        count_outcome_8[thisrand_8] = thisarray_8[thisrand_8]
        if count_outcome_8[thisrand_8] == 1:
            score_with_ownpostbar_g[sim] = 1
            print('touch9 owngoal',score_with_ownpostbar_g)
            count_with_ownpostsbar_g = count_with_ownpostsbar_g + 1
        print('touch9 No owngoal',score_with_ownpostbar_g)
        
    elif (theta_collect[sim] < np.arctan(ownsups2(height_bar_touch10) / ownsubs) \
or (owntheta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(ownsups1(height_bar_touch10) / subs))) \
and (3*const.pi/2 - np.arctan(half_w_post_touch10 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch10 / long_distance)):
        thisrand_7 = random.randint(0,10000-1)
        thisarray_7 = possibility(7)
        count_outcome_7[thisrand_7] = thisarray_7[thisrand_7]
        if count_outcome_7[thisrand_7] == 1:
            score_with_ownpostbar_g[sim] = 1
            print('touch10 owngoal',score_with_ownpostbar_g)
            count_with_ownpostsbar_g = count_with_ownpostsbar_g + 1
        print('touch10 No owngoal',score_with_ownpostbar_g)
        
    elif (theta_collect[sim] < np.arctan(ownsups2(height_bar_touch11) / ownsubs) \
or (owntheta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(ownsups1(height_bar_touch11) / subs))) \
and (3*const.pi/2 - np.arctan(half_w_post_touch11 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch11 / long_distance)):
        thisrand_6 = random.randint(0,10000-1)
        thisarray_6 = possibility(6)
        count_outcome_6[thisrand_6] = thisarray_6[thisrand_6]
        if count_outcome_6[thisrand_6] == 1:
            score_with_ownpostbar_g[sim] = 1
            print('touch11 owngoal',score_with_ownpostbar_g)
            count_with_ownpostsbar_g = count_with_ownpostsbar_g + 1
        print('touch11 No owngoal',score_with_ownpostbar_g)
            
    elif (theta_collect[sim] < np.arctan(ownsups2(height_bar_touch12) / ownsubs) \
or (owntheta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(ownsups1(height_bar_touch12) / subs))) \
and (3*const.pi/2 - np.arctan(half_w_post_touch12 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch12 / long_distance)):
        thisrand_5 = random.randint(0,10000-1)
        thisarray_5 = possibility(5)
        count_outcome_5[thisrand_5] = thisarray_5[thisrand_5]
        if count_outcome_5[thisrand_5] == 1:
            score_with_ownpostbar_g[sim] = 1
            print('touch12 owngoal',score_with_ownpostbar_g)
            count_with_ownpostsbar_g = count_with_ownpostsbar_g + 1
        print('touch12 No owngoal',score_with_ownpostbar_g)
        
    elif (theta_collect[sim] < np.arctan(ownsups2(height_bar_touch13) / ownsubs) \
or (owntheta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(ownsups1(height_bar_touch13) / subs))) \
and (3*const.pi/2 - np.arctan(half_w_post_touch13 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch13 / long_distance)):
        thisrand_4 = random.randint(0,10000-1)
        thisarray_4 = possibility(4)
        count_outcome_4[thisrand_4] = thisarray_4[thisrand_4]
        if count_outcome_4[thisrand_4] == 1:
            score_with_ownpostbar_g[sim] = 1
            print('touch13 owngoal',score_with_ownpostbar_g)
            count_with_ownpostsbar_g = count_with_ownpostsbar_g + 1
        print('touch13 No owngoal',score_with_ownpostbar_g)
        
    elif (theta_collect[sim] < np.arctan(ownsups2(height_bar_touch14) / ownsubs) \
or (owntheta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(ownsups1(height_bar_touch14) / subs))) \
and (3*const.pi/2 - np.arctan(half_w_post_touch14 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch14 / long_distance)):
        thisrand_3 = random.randint(0,10000-1)
        thisarray_3 = possibility(3)
        count_outcome_3[thisrand_3] = thisarray_3[thisrand_3]
        if count_outcome_3[thisrand_3] == 1:
            score_with_ownpostbar_g[sim] = 1
            print('touch14 owngoal',score_with_ownpostbar_g)
            count_with_ownpostsbar_g = count_with_ownpostsbar_g + 1
        print('touch14 No owngoal',score_with_ownpostbar_g)  
        
    elif (theta_collect[sim] < np.arctan(ownsups2(height_bar_touch15) / ownsubs) \
or (owntheta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(ownsups1(height_bar_touch15) / subs))) \
and (3*const.pi/2 - np.arctan(half_w_post_touch15 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch15 / long_distance)):
        thisrand_2 = random.randint(0,10000-1)
        thisarray_2 = possibility(2)
        count_outcome_2[thisrand_2] = thisarray_2[thisrand_2]
        if count_outcome_2[thisrand_2] == 1:
            score_with_ownpostbar_g[sim] = 1
            print('touch15 owngoal',score_with_ownpostbar_g)
            count_with_ownpostsbar_g = count_with_ownpostsbar_g + 1
        print('touch15 No owngoal',score_with_ownpostbar_g)
        
    elif (theta_collect[sim] < np.arctan(ownsups2(height_bar_touch16) / ownsubs) \
or (owntheta_g10<theta_collect[sim] \
and theta_collect[sim]< np.arctan(ownsups1(height_bar_touch16) / subs))) \
and (3*const.pi/2 - np.arctan(half_w_post_touch16 / long_distance) < phi_all_collect[sim] \
and phi_all_collect[sim] <= 3*const.pi/2 + np.arctan(half_w_post_touch16 / long_distance)):
        thisrand_1 = random.randint(0,10000-1)
        thisarray_1 = possibility(1)
        count_outcome_1[thisrand_1] = thisarray_1[thisrand_1]
        if count_outcome_1[thisrand_1] == 1:
            score_with_ownpostbar_g[sim] = 1
            print('touch16 owngoal',score_with_ownpostbar_g)
            count_with_ownpostsbar_g = count_with_ownpostsbar_g + 1
        print('touch16 No owngoal',score_with_ownpostbar_g)
        
    # no goal
    else:
        score_with_postbar[sim] = 0
        print('No goal',score_with_postbar_g)
#     elif theta_collect[sim] < np.arctan(height_bar_touch17 / distance) \
# and (const.pi/2 - np.arctan(half_w_post_touch1 / distance) < phi_collect[sim] \
# and phi_collect[sim] <= const.pi/2 + np.arctan(half_w_post_touch1 / distance)):
#         thisrand_1 = random.randint(0,10000-1)
#         thisarray_1 = possibility(1)
#         count_outcome_1[thisrand_1] = thisarray_1[thisrand_1]
#         if count_outcome_1[thisrand_1] == 1:
#             score[sim] = 1
#             print(score)
####Goal keeper section    
    if score_with_postbar[sim] == 1: #or score_with_ownpostbar[sim] == 1:
        
        random_human_phi_index = random.randint(0,int(abs(range_place_phi_deg*100)))
        random_phi_man_begin = random_human_phi_index /180 * const.pi
        random_phi_man_end = random_phi_man_begin + range_human_phi
        random_use_phi_area = random_phi_man_begin+random_phi_man_end 
        
        delta_phi_man = abs(const.pi/2 - random_use_phi_area/2)
        distance_man_new = distance / np.cos(delta_phi_man)

        # possible human theta
        # range_random_human_theta = np.arctan(human_height/distance_man_new)
        range2_random_human_theta = np.arctan(sups2d(distance_man_new,human_height) / subs)
        range1_random_human_theta = np.arctan(sups1d(distance_man_new,0) / subs) - np.arctan(sups1d(distance_man_new,human_height) / subs)
                                             
        # theta_in_goal = np.arctan(height_directgoal/distance)
        theta_in_goal2 = theta_g2s 
        theta_in_goal1 = theta_g10-theta_g1s 
        theta_ratio1 = theta_in_goal1 / range1_random_human_theta
        theta_ratio2 = theta_in_goal2 / range2_random_human_theta


        # random_human_theta = (theta_in_goal - range_random_human_theta)/ const.pi *180
        # random_human_theta_index = random.randint(0,int(random_human_theta*100))
        # random_theta_man_begin = random_human_theta_index /180 * const.pi
        # random_theta_man_end = random_human_theta_index /180 * const.pi + range_random_human_theta 
        
        try:
            
            random_human_theta1 = (theta_in_goal1 - range1_random_human_theta)/ const.pi *180
            random_human_theta1_index = random.randint(0,int(abs(random_human_theta1*100)))
            random_theta1_man_begin = random_human_theta1_index /180 * const.pi
            random_theta1_man_end = random_human_theta1_index /180 * const.pi + range1_random_human_theta 
        
            random_human_theta2 = (theta_in_goal2 - range2_random_human_theta)/ const.pi *180
            random_human_theta2_index = random.randint(0,int(abs(random_human_theta2*100)))
            random_theta2_man_begin = random_human_theta2_index /180 * const.pi
            random_theta2_man_end = random_human_theta2_index /180 * const.pi + range2_random_human_theta 
        
        except Exception:
            pass  # or use 'continue'    
        
        if ((random_theta1_man_begin <= theta_collect[sim] and theta_collect[sim] <= random_theta1_man_end) \
or (random_theta2_man_begin <= theta_collect[sim] and theta_collect[sim] <= random_theta2_man_end)) \
and (random_phi_man_begin <= phi_all_collect[sim] and phi_all_collect[sim] <= random_phi_man_end):
            score_with_postbar_g[sim] = 0
            score_with_ownpostbar_g[sim] = 0
            count_with_postsbar_g = count_with_postsbar_g - 1
            count_keepersave_g = count_keepersave_g + 1
                
    
# print(count_with_postsbar)
# ball with diameter d
print('The fraction of goals in',sim_time,'isotropic events with gravity, posts and bar is:', count_with_postsbar_g/sim_time)
print('Own goals percentage in',sim_time,' isotropic events with gravity, posts and bar is:', count_with_ownpostsbar_g/sim_time)
print('Goals saved by keeper percentage in',sim_time,' isotropic events with gravity, posts and bar is:', count_keepersave_g/sim_time)

# #%%
# random_human_phi_index = random.randint(0,int(range_place_phi_deg*100))
# random_phi_man_begin = random_human_phi_index /180 * const.pi
# random_phi_man_end = random_phi_man_begin + range_human_phi
# random_use_phi_area = random_phi_man_begin+random_phi_man_end 
        
# delta_phi_man = abs(const.pi/2 - random_use_phi_area/2)
# distance_man_new = distance / np.cos(delta_phi_man)

#         # possible human theta
#         # range_random_human_theta = np.arctan(human_height/distance_man_new)
# range1_random_human_theta = np.arctan(sups2d(distance_man_new,human_height) / subs)
# range2_random_human_theta = np.arctan(sups1d(distance_man_new,0) / subs) - np.arctan(sups1d(distance_man_new,human_height) / subs)
                                             
#         # theta_in_goal = np.arctan(height_directgoal/distance)
# theta_in_goal2 = theta_g2s 
# theta_in_goal1 = theta_g1s - theta_g10 
# theta_ratio1 = theta_in_goal1 / range1_random_human_theta
# theta_ratio2 = theta_in_goal2 / range2_random_human_theta

# print(theta_in_goal1)
# print(theta_in_goal2)
# print(range1_random_human_theta)
# print(range2_random_human_theta)

#         # random_human_theta = (theta_in_goal - range_random_human_theta)/ const.pi *180
#         # random_human_theta_index = random.randint(0,int(random_human_theta*100))
#         # random_theta_man_begin = random_human_theta_index /180 * const.pi
#         # random_theta_man_end = random_human_theta_index /180 * const.pi + range_random_human_theta 
# #%%
        
# random_human_theta1 = (theta_in_goal1 - range1_random_human_theta)/ const.pi *180

# random_human_theta1_index = random.randint(0,int(random_human_theta1*100))
# random_theta1_man_begin = random_human_theta1_index /180 * const.pi
# random_theta1_man_end = random_human_theta1_index /180 * const.pi + range1_random_human_theta 
        
# random_human_theta2 = (theta_in_goal2 - range2_random_human_theta)/ const.pi *180
# random_human_theta2_index = random.randint(0,int(random_human_theta2*100))
# random_theta2_man_begin = random_human_theta2_index /180 * const.pi
# random_theta2_man_end = random_human_theta2_index /180 * const.pi + range2_random_human_theta
# # #%%
# # print(random.randint(0,1010))
# #%%
# print(random_human_theta1)
# print(random_human_theta2)


#%% There is a drag force.
# Can be done by ODE numerical solver in python 
# in my metethod ogf geometry and theta phi relations may not work explicitly.

