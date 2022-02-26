#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python assignment 2
Created on Sun Oct 14 01:12:23 2021
@author: vitorshen
at Uppsala University
by Vitor Jose Shen
"""
#%%
# Import section
import matplotlib.pyplot as plt
import numpy as np
# import math as m
import scipy.constants as const
from scipy.integrate import solve_ivp
from mpl_toolkits.mplot3d import Axes3D

#%%
# Parameter section
# In SI unit

###################################
# # test the constants result first
# print(const.proton_mass)
# print(const.electron_mass)
# print (const.e)
# print(const.e * 10**6)
###################################

m   = const.proton_mass     # proton mass in kg
q   = const.e               # proton positive charge in C
E_k = const.e * 10**6       # knetic energy 1 MeV proton in J
B   = 3                     # Magnetic field magnitude in T


#%% Q1  only v_x 
# F = q(E+vxB)
# dv/dt = q/m (E+vxB)

# Initial velocity in x-direction
vx_0 = np.sqrt(2*E_k/m)             #since E_k=1/2mv^2

# initial state vector Y_i in (x,y,z,v_x,v_y,v_z) -> (position and velocity of 3 components)
Y_i  = (0, 0, 0, vx_0, 0, 0)

# For convinence of calculation
C_qm = q/m

# Define a function as derivitive of velocities 
# which satisfies Newton's law for Lorentz Force in EM field
# state vector Y in (x,y,z,v_x,v_y,v_z) -> (position and velocity of 3 components)
# I wish to return dY/dt 
def deri(t , Y):
    dx_dt = Y[3]
    dy_dt = Y[4]
    dz_dt = Y[5]
    CP = np.cross(Y[3:],[0,0,3]) #Cross product result of vxB
    dvx_dt = C_qm * CP[0]
    dvy_dt = C_qm * CP[1]
    dvz_dt = C_qm * CP[2]
    return (dx_dt, dy_dt, dz_dt, dvx_dt, dvy_dt, dvz_dt)

###################################
# print(np.cross(Y_i[3:],[0,0,3]))
# print(deri(1E-6,Y_i))
###################################

t_span = (0, 1E-6)    #time period is 1 mu s = 1e-6s
t_steps = np.linspace(0.0, 10**-6, 1000)

sol = solve_ivp(deri, t_span, Y_i, method='Radau',t_eval=t_steps)
# print(sol.y)
fig_1xy = plt.figure(1)
plt.plot(sol.y[0], sol.y[1],'*-')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Proton movement in x-y plane')
plt.savefig('Q1xyplane.png')
plt.show()

fig_1xz = plt.figure(2)
plt.plot(sol.y[0], sol.y[2],'*-')
plt.xlabel('x (m)')
plt.ylabel('z (m)')
plt.title('Proton movement in x-z plane')
plt.savefig('Q1xzplane.png')
plt.show()

fig_1yz = plt.figure(3)
plt.plot(sol.y[1], sol.y[2],'*-')
plt.xlabel('y (m)')
plt.ylabel('z (m)')
plt.title('Proton movement in y-z plane')
plt.savefig('Q1yzplane.png')
plt.show()


#%% Q2    with v_x and v_z

# first assume the initial angle between x and z is 45 degree
###################################
# print(np.sin(const.pi / 4))
# print(np.sqrt(2)/2)
###################################
deg = const.pi / 4  #initial angle between x and z 

E_kx = E_k * np.sin(const.pi / 4)   #Knetic Energy in x
E_kz = E_k * np.cos(const.pi / 4)   #Knetic Energy in z

###################################
# print(E_kx,E_kz)
# print(E_kx**2+E_kz**2)
# print(E_k**2)
# ###################################

vx_0 = np.sqrt(2*E_kx/m)             #initial velocity in x
vz_0 = np.sqrt(2*E_kz/m)             #initial velocity in z

Y_ixz  = (0, 0, 0, vx_0, 0, vz_0)
t_span = (0, 1E-6)    #time period is 1 mu s = 1e-6s

t_steps = np.linspace(0.0, 10**-6, 1000)

sol_xz = solve_ivp(deri, t_span, Y_ixz, method='Radau',  t_eval=t_steps)
# sol_xz = solve_ivp(deri, t_span, Y_ixz,  t_steps)


# print(sol.y)
fig_2xy = plt.figure(4)
plt.plot(sol_xz.y[0], sol_xz.y[1],'*-')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Proton movement in x-y plane with xz initial v')
plt.savefig('Q2xyplane.png')
plt.show()

fig_2xz = plt.figure(5)
plt.plot(sol_xz.y[0], sol_xz.y[2],'*-')
plt.xlabel('x (m)')
plt.ylabel('z (m)')
plt.title('Proton movement in x-z plane with xz initial v')
plt.savefig('Q2xzplane.png')
plt.show()

fig_2yz = plt.figure(6)
plt.plot(sol_xz.y[1], sol_xz.y[2],'*-')
plt.xlabel('y (m)')
plt.ylabel('z (m)')
plt.title('Proton movement in y-z plane with xz initial v')
plt.savefig('Q2yzplane.png')
plt.show()


#%% Q3   z-direction and R=3 with cylindrically symmetric B

# a = q/m * vxB

# R = 3
# theta = np.linspace(0, 2*np.pi, 360)
# x = R * np.cos(theta)
# y = R * np.sin(theta)
# # z = z
# # Y_i = (x,y,z,v_xc,v_yc,v_zc)
# B_0=9
# B_x=B_0*(np.cos(np.arctan2(y,x)))
# B_y=B_0*(-np.sin(np.arctan2(y,x)))
# B_z=0
# B = [B_x,B_y,B_z]
# B_0/R 

# (R,theta,z)
# R = np.sqrt(x**2+y**2)
# theta = np.arctan(y / x)
# z = z

# # R = y[0]**2 + y[1]**2 + y[2]**2
# # q / m * np.cross(y[3:6],B)
# phi = np.linspace(0, 2*np.pi, 360)
# # in_r = 3
# phi_i = phi[0]
# Initial Conditions
######################
# i : initial
# r : radius
# tht : theta

r_i = 3.0
# tht_i = m.degrees((0)*np.pi)
tht_i = np.pi * 0
# math.degrees((0)*np.pi)
#theta from Radians to Degrees
z_i = 0.0
R_i = np.array([r_i, tht_i, z_i]) 
#position vector

v_r_i = 0.0
v_tht_i = 0
v_z_i = np.sqrt(2*E_k/m)  
# proton velocity
v_i = np.array([v_r_i, v_tht_i, v_z_i]) 

B_r_i = 0
B_tht_i = -9
B_z_i = 0.0
B_i = np.array([B_r_i, B_tht_i, B_z_i]) 

# Initial Conditions Array
initial = np.array([R_i, v_i, B_i])
starting = initial.reshape(9,)

def B_field(t, y):
    ##velocity
    v_ra = y[3]     #radial
    v_tht = y[4]    #theta
    v_z = y[5]      #z-component
    v = np.array([y[3], y[4], y[5]])
    B_0 = np.array([y[6], y[7]/y[0], y[8]]) 
    # only depends on radius y[0]
    B_result = np.multiply(C_qm , np.cross(v, B_0))
    # magnetic_curl = np.multiply(curl, C_qm)
    
    ## Acceleration
    a_ra = B_result[0]
    a_tht = B_result[1]
    a_z = B_result[2]

    dBx_dt = 0
    dBtht_dt = 0
    dBz_dt = 0
    
    dy_dt = (v_ra,v_tht,v_z,a_ra,a_tht,a_z,dBx_dt,dBtht_dt,dBz_dt)   
    return(dy_dt)

# Time Range
t_range = (0.0, 1e-6)
# Time Steps
t_steps = np.linspace(0.0, 10**-6, 1000)

# Integrate
sol_cylnew = solve_ivp(B_field , t_range, starting, t_eval = t_steps)

# def Bfield(Y,phi,R):
#     # phi = np.linspace(0, 2*np.pi, 360)
#     Y[0] = R * np.cos(phi[0])    # x = R * np.cos(theta)
#     Y[1] = R * np.sin(phi[0])    # y = R * np.sin(theta)
#     # z = z
#     R = np.sqrt(Y[0]**2+Y[1]**2)
#     B_0=9
#     B_x=B_0*(np.cos(np.arctan2(Y[1],Y[0])))
#     B_y=B_0*(-np.sin(np.arctan2(Y[1],Y[0])))
#     B_z=0
#     return (B_x,B_y,B_z)

# def evolution(t, y, parameters):   
#     m, q = parameters
#     dx_dt = y[3]
#     dy_dt = y[4]
#     dz_dt = y[5]
#     product = q/m * np.cross(y[3:],Bfield(y[0:2],0,3))
#     dvx_dt = product[0]
#     dvy_dt = product[1]
#     dvz_dt = product[2]                      
#     return (dx_dt, dy_dt, dz_dt, dvx_dt, dvy_dt, dvz_dt)

# y_initial = np.array([3, 0, 0, 0, 0, np.sqrt(2*E_k/m)])
# time_step = 1E-10
X = sol_cylnew.y[0]*np.cos(sol_cylnew.y[1])
Y = sol_cylnew.y[0]*np.sin(sol_cylnew.y[1])
Z = sol_cylnew.y[2]
# sol_cyl = solve_ivp(lambda t, y : evolution(t, y, (m, q)), t_span, y_initial, method='Radau', max_step=time_step)
# #
fig_33xy = plt.figure(7)
plt.plot(sol_cylnew.y[0], sol_cylnew.y[1],'m*-')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('In x-y plane with cylindrically symmetric B')
plt.savefig('Q3xyplane-newagain.png')
plt.show()

fig_33xz = plt.figure(8)
plt.plot(sol_cylnew.y[0], sol_cylnew.y[2],'m*-')
plt.xlabel('x (m)')
plt.ylabel('z (m)')
plt.title('In x-z plane with cylindrically symmetric B')
plt.savefig('Q3xzplane-newagain.png')
plt.show()

fig_33yz = plt.figure(9)
plt.plot(sol_cylnew.y[1], sol_cylnew.y[2],'m*-')
plt.xlabel('y (m)')
plt.ylabel('z (m)')
plt.title('In y-z plane with cylindrically symmetric B')
plt.savefig('Q3yzplane-newagain.png')
plt.show()

# fig33 = plt.figure(figsize=(14.0,16.0))
# # ax = fig.gca(projection='3d')
# # ax = plt.axes(projection='3d')
# ax = Axes3D(fig33)
# ax.plot(sol_cylnew.y[0,:],sol_cylnew.y[1,:],sol_cylnew.y[2,:],'r-')
# plt.savefig('Q5-3Dnewagain.png')
# plt.show()
#%%

# #Define the function to get the field vector 
# def B(y, B_temp):
#     r = np.array([y[0], y[1], 0])           # vector aligned with the x,y projection of the position vector y
#     r_unit = r / np.sqrt(r[0]**2 + r[1]**2)      # unit vector aligned with the x,y projection of the position vector y
#     r_perp = np.array([-r[0], r[1],0])     # unit vector perpendicular to the x,y projection of position vector y
#     B_field = B_temp[0] * r_unit  +  B_temp[1] * r_perp
#     B_field[2] = B_temp[2]
#     # r = np.array([y[0], y[1], 0])           # vector aligned with the x,y projection of the position vector y
#     # r = r / np.sqrt(r[0]**2 + r[1]**2)      # unit vector aligned with the x,y projection of the position vector y
#     # r_perp = np.array([-r[1], r[0], 0])     # unit vector perpendicular to the x,y projection of position vector y
#     # B_field = B_temp[0] * r  +  B_temp[1] * r_perp
#     # B_field[2] = B_temp[2]
#     return B_field

# R = 3
# B0 = 9.0 / R
# x = np.linspace(3,0,0)
# y = np.linspace(0,0,0)
# z = np.linspace(0,0,0)
# x,y,z = np.meshgrid(x,y,z)

# def B(y, B_temp):
#     theta = np.linspace(0, 2*np.pi, 360)
#     x = R*np.cos(theta)
#     y = R*np.sin(theta)
#     Bx = B0*(np.cos(np.arctan2(y,x)))
#     By = B0*(-np.sin(np.arctan2(y,x)))
#     Bz = 0
#     return(Bx,By,Bz)


# def Bf(x,y):
#     # i = 1                                           #Amps in the wire
#     # mu = 1.26 * 10**(-6)                            #Magnetic constant                       
#     mag = B0/np.sqrt((x)**2+(y)**2) #Magnitude of the vector B
#     By = mag * (np.cos(np.arctan2(y,x)))            #By
#     Bx = mag * (-np.sin(np.arctan2(y,x)))           #Bx
#     Bz = z*0                                        #Bz (zero, using the right-hand rule)
#     return Bx,By,Bz

# def cylinder(r):
#     phi = np.linspace(-2*np.pi,2*np.pi,100)
#     x = r*np.cos(phi)
#     y = r*np.sin(phi)
#     return x,y


#Define the function to get its evolution
# def evo(t, y, parameters):   
#     m, q, B_temp = parameters
#     dx_dt = y[3]
#     dy_dt = y[4]
#     dz_dt = y[5]
#     # product = q/m * np.cross(y[3:6], B(y[0:3], B_temp))
#     product = q/m * np.cross(y[3:6], B(y,B_temp))
#     dvx_dt = product[0]
#     dvy_dt = product[1]
#     dvz_dt = product[2]                      
#     return (dx_dt, dy_dt, dz_dt, dvx_dt, dvy_dt, dvz_dt)
#     # return np.concatenate( (y[3:6], q/m * np.cross(B(B_temp,y[0:3]) ,y[3:6])))
#     # return np.concatenate( (y[3:6], q/m * np.cross(y[3:6], B(y[0:3], B_temp))) )

# # def f(t, y, parameters):   
#     mass, charge, B_templet = parameters
#     return np.concatenate( (y[3:6], (charge/mass)*np.cross(y[3:6], B(y[0:3], B_templet))) )
# phi = np.linspace(0, 2*np.pi, 360)

# B_direction = np.array([-1/2,1/2,0])


# B_magnitude = 9.0

# y_initial = np.array([R, 0, 0, 0, 0, np.sqrt(2*E_k/m)])
# n_iter = 10000
# time_step = 1E-10
# # t_span=[0,n_iter*time_step]
# t_span = np.linspace(0,1E-6,4)

# phi = np.linspace(0, 2*np.pi, 360)
# # B_direction = -y[0]*np.sin(phi)+y[1]*np.cos(phi)
# B_direction = B_magnitude * B_direction / np.sqrt(B_direction.dot(B_direction))
# # time_step = 0.001
# # n_iter = 10000
# # t_span=[0,n_iter*time_step]

# sol_cs = solve_ivp(lambda t, y : evo(t, y, (m, q, B_direction)), t_span, y_initial, method='Radau', max_step=time_step)
# # sol_cs = solve_ivp(lambda t, y : evo(t, y, (m, q, B_direction)), t_span, y_initial)
# # sol = solve_ivp(fun = lambda t, y : f(t, y, (mass, charge, B_direction)), t_span=t_span, y0=xv_start)
# ###################################
# print(np.isnan(xv_start).any())
# print(np.isnan(B_direction).any())
# print(np.isnan(B_direction).any())
# print(np.isinf(xv_start).any())
# print(np.isinf(xv_start).any())
# print(np.isinf(B_direction).any())
# ###################################

# fig_3xy = plt.figure(7)
# plt.plot(sol_cs.y[2], sol_cs.y[1],'m*-')
# plt.xlabel('x (m)')
# plt.ylabel('y (m)')
# plt.title('In x-y plane with cylindrically symmetric B')
# plt.savefig('Q3xyplane-new.png')
# plt.show()

# fig_3xz = plt.figure(8)
# plt.plot(sol_cs.y[2], sol_cs.y[0],'m*-')
# plt.xlabel('x (m)')
# plt.ylabel('z (m)')
# plt.title('In x-z plane with cylindrically symmetric B')
# plt.savefig('Q3xzplane-new.png')
# plt.show()

# fig_3yz = plt.figure(9)
# plt.plot(sol_cs.y[1], sol_cs.y[0],'m*-')
# plt.xlabel('y (m)')
# plt.ylabel('z (m)')
# plt.title('In y-z plane with cylindrically symmetric B')
# plt.savefig('Q3yzplane-new.png')
# plt.show()

# fig = plt.figure(figsize=(14.0,16.0))
# # ax = fig.gca(projection='3d')
# # ax = plt.axes(projection='3d')
# ax = Axes3D(fig)
# ax.plot(sol_cs.y[0,:],sol_cs.y[2,:],sol_cs.y[1,:],'r-')
# # ax.plot(sol_cs.y[2,:],sol_cs.y[1,:],sol_cs.y[0,:],'r-')

# ax.set_xlabel('x (m)')
# ax.set_ylabel('y (m)')
# ax.set_zlabel('z (m)')

# plt.title('3D projection of Question3')
# plt.savefig('Q5-rnew.png')
# plt.show()
#%%
# def B(y, B_templet):
#     r = np.array([y[0], y[1], 0]) # vector aligned with the x,y projection of the position vector y
#     r = r / np.sqrt(r[0]**2 + r[1]**2) # unit vector aligned with the x,y projection of the position vector y
#     r_perp = np.array([-r[1], r[0], 0]) # unit vector perpendicular to the x,y projection of position vector y
#     B_field = B_templet[0] * r  +  B_templet[1] * r_perp
#     B_field[2] = B_templet[2]
#     return B_field

# def f(t, y, parameters):   
#     mass, charge, B_templet = parameters
#     return np.concatenate( (y[3:6], (q/m)*np.cross(y[3:6], B(y[0:3], B_templet))) )


# B_direction = np.array([0.3,1,0.1])
# # B_direction = np.array([0.3,0.1,1])
# # B_direction = np.array([0.1,1,0.3])
# # B_direction = np.array([1,0.3,0.1])

# B_magnitude = 9
# # xv_start = np.array([3, 0, 0, 0, 0, 2])
# xv_start = np.array([3, 0, 0, 0, 0, np.sqrt(2*E_k/m)])

# time_step = 0.01
# n_iter = 10000
# t_span=[0,n_iter*time_step]
# # t_span = np.linspace(0,1E-6,11)

# B_direction = B_magnitude * B_direction / np.sqrt(B_direction.dot(B_direction))

# # sol = solve_ivp(fun = lambda t, y : f(t, y, (mass, charge, B_direction)), t_span=t_span, y0=xv_start, max_step=time_step)
# sol = solve_ivp(fun = lambda t, y : f(t, y, (m, q, B_direction)), t_span=t_span, y0=xv_start)
# # 

# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# # r = 3
# # ax.set_xlim((-r, r))
# # ax.set_ylim((-r, r))
# # ax.set_zlim((-r, r))
# ax.plot(sol.y[0,:], sol.y[1,:], sol.y[2,:], 'r-')
# # ax.plot(sol.y[0,0], sol.y[1,0], sol.y[2,0], 'bo')
# # ax.plot(sol.y[0,-1], sol.y[1,-1], sol.y[2,-1], 'go')
# plt.show()

# fig_1xy = plt.figure(1)
# plt.plot(sol.y[0], sol.y[1],'*-')
# plt.xlabel('x (m)')
# plt.ylabel('y (m)')
# plt.title('Proton movement in x-y plane')
# plt.savefig('Q1xyplane.png')
# plt.show()

# fig_1xz = plt.figure(2)
# plt.plot(sol.y[0], sol.y[2],'*-')
# plt.xlabel('x (m)')
# plt.ylabel('z (m)')
# plt.title('Proton movement in x-z plane')
# plt.savefig('Q1xzplane.png')
# plt.show()

# fig_1yz = plt.figure(3)
# plt.plot(sol.y[1], sol.y[2],'*-')
# plt.xlabel('y (m)')
# plt.ylabel('z (m)')
# plt.title('Proton movement in y-z plane')
# plt.savefig('Q1yzplane.png')
# plt.show()

# fig = plt.figure(figsize=(14.0,16.0))
# # ax = fig.gca(projection='3d')
# # ax = plt.axes(projection='3d')
# ax = Axes3D(fig)
# ax.plot(sol.y[0,:],sol.y[1,:],sol.y[2,:],'r-')

# ax.set_xlabel('x (m)')
# ax.set_ylabel('y (m)')
# ax.set_zlabel('z (m)')

# plt.title('3D projection of Question3')
# plt.savefig('Q5-rtestnew.png')
# plt.show()


#%% 3D for Question1
fig = plt.figure(figsize=(14.0,16.0))
# ax = fig.gca(projection='3d')
# ax = plt.axes(projection='3d')
ax = Axes3D(fig)
ax.plot(sol.y[0],sol.y[1],sol.y[2],'r-')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_zlabel('z (m)')
plt.title('3D projection of Question1')
plt.savefig('3DforQ1-r.png')
plt.show()

#%% Q4  3D for Question2
fig = plt.figure(figsize=(14.0,16.0))
# ax = fig.gca(projection='3d')
# ax = plt.axes(projection='3d')
ax = Axes3D(fig)
ax.plot(sol_xz.y[0],sol_xz.y[1],sol_xz.y[2],'r-')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_zlabel('z (m)')
plt.title('3D projection of Question2')
plt.savefig('Q4-r.png')
plt.show()


#%% Q5  3D for Question3
# fig = plt.figure(figsize=(14.0,16.0))
# # ax = fig.gca(projection='3d')
# # ax = plt.axes(projection='3d')
# ax = Axes3D(fig)
# # ax.plot(sol_cs.y[0,:],sol_cs.y[1,:],sol_cs.y[2,:],'r-')
# ax.plot(sol_cs.y[2,:],sol_cs.y[1,:],sol_cs.y[0,:],'r-')

# ax.set_xlabel('x (m)')
# ax.set_ylabel('y (m)')
# ax.set_zlabel('z (m)')

# plt.title('3D projection of Question3')
# plt.savefig('Q5-rtestnew.png')
# plt.show()
fig33 = plt.figure(figsize=(14.0,16.0))
# ax = fig.gca(projection='3d')
# ax = plt.axes(projection='3d')
ax = Axes3D(fig33)
ax.plot(sol_cylnew.y[0,:],sol_cylnew.y[1,:],sol_cylnew.y[2,:],'r-')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_zlabel('z (m)')
plt.title('3D projection of Question3')
plt.savefig('Q5-3Dnewagain.png')
plt.show()

#%%Q6 drift velocity in question3
# evaluate drift velocity of Q3
# read data point from Q3 in y-z plane directly
print(sol_cylnew.t)
print(sol_cylnew.y[2])
def drift(f_x, f_z, t):
    size = int(len(f_x)/2)   
    s_1 = f_x[:size]
    pos_i = np.argmax(s_1)    
    s_2 = f_x[size:]
    pos_f = np.argmax(s_2) + size   
    d_z = f_z[pos_f]-f_z[pos_i]
    d_t = t[pos_f]-t[pos_i]   
    v_d = d_z / d_t
    return v_d
print(' The drift velocity in Q3:', drift(X,Z,sol_cylnew.t), 'm/s')