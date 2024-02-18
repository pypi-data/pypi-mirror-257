#%%

from vizmath.quadtile_chart import squaremap as sm
from vizmath import functions as vf
import numpy as np

#%%
t = np.linspace(0, 2 * np.pi, 50)
x = 16 * np.sin(t)**3
y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
poly = [(x,y) for x,y in zip(x,y)]
# poly = vf.rotate_polygon(poly,45)
o_sm = sm.random_squaremap(3, 320, constraints=poly, collapse=True, 
    rotate=0, sig=1.05, buffer=.125)
o_sm.o_squaremap.plot_level(level=3)

#%%
# Set up the drawing object with data
o_sm.o_squaremap.o_rad_treemap.df = o_sm.o_squaremap.df_rad_treemap
# Rescale the data for leveraging map layers in Tableau
o_sm.o_squaremap.o_rad_treemap.dataframe_rescale(
    xmin=-20, xmax=20, ymin=-20, ymax=20)
# Write the data to csv
o_sm.o_squaremap.o_rad_treemap.dataframe_to_csv('squaremap_heart')
