#%%
import pandas as pd
import numpy as np
from vizmath.quadtile_chart import polyquadtile as pqt
from vizmath.quadtile_chart import squaremap as sm
from vizmath import functions as vf

#%% general squaremap to csv
o_sm = sm.random_squaremap(num_levels=3, num_top_level_items=120,
    items_range=(2,4), value_range=(1,10), sig=0.75, 
    collapse=True, buffer=0.05)
o_sm.o_squaremap.plot_level(level=3)
#%%
o_sm.o_squaremap.df_rad_treemap.head(10)
#%%
o_sm.o_squaremap.o_rad_treemap.df = o_sm.o_squaremap.df_rad_treemap
o_sm.o_squaremap.o_rad_treemap.dataframe_rescale(
    xmin=-5, xmax=5, ymin=-5, ymax=5)
o_sm.o_squaremap.o_rad_treemap.dataframe_to_csv('squaremap')

#%%
# C: circle
circle = vf.circle(0,0,10)
poly = [(x,y) for x,y,_ in circle]
o1_pqt = pqt.random_polyquadtile(60, constraints=poly, collapse=True, buffer=.25)
o1_pqt.polyquadtile_plot()
#%%
o1_pqt.o_polyquadtile_chart.dataframe_rescale(xmin=-11, xmax=11, ymin=-11, ymax=11)
# o1_pqt.o_polyquadtile_chart.dataframe_to_csv('medium_circle')
o1_pqt.o_polyquadtile_chart.df['shape'] = 'circle'

#%%
# H: heart
t = np.linspace(0, 2 * np.pi, 50)
x = 16 * np.sin(t)**3
y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
poly = [(x,y) for x,y in zip(x,y)]
o2_pqt = pqt.random_polyquadtile(60, constraints=poly, collapse=True, rotate=0, buffer=.3)
o2_pqt.polyquadtile_plot()
#%%
o2_pqt.o_polyquadtile_chart.dataframe_rescale(xmin=-18, xmax=18, ymin=-18, ymax=18)
# o2_pqt.o_polyquadtile_chart.dataframe_to_csv('medium_heart')
o2_pqt.o_polyquadtile_chart.df['shape'] = 'heart'

#%%
# A: arch
circle1 = vf.circle(0,0,10)
circle2 = vf.circle(0,0,3)
poly1 = [(x-6,y) for x,y,_ in circle1[:26]]
poly2 = [(x-6,y) for x,y,_ in reversed(circle2[:26])]
poly = poly1 + poly2
poly = vf.rotate_polygon(poly,90) #45
poly = vf.rotate_polygon(poly,45) #45
o3_pqt = pqt.random_polyquadtile(60, constraints=poly, collapse=True, rotate=45, xc=-5, yc=-2, buffer=.2) #, xc=-1, yc=-1)
o3_pqt.polyquadtile_plot(show_constraints=True)
#%%
o3_pqt.o_polyquadtile_chart.dataframe_rescale(xmin=-20, xmax=10, ymin=-10, ymax=20)
# o3_pqt.o_polyquadtile_chart.dataframe_to_csv('medium_arch')
o3_pqt.o_polyquadtile_chart.df['shape'] = 'arch'

#%%
# R: rectangle
o4_pqt = pqt.random_polyquadtile(60, constraints=[(2,1)], collapse=True, rotate=45, xc=-2.5, buffer=.1)
o4_pqt.polyquadtile_plot()
#%%
o4_pqt.o_polyquadtile_chart.dataframe_rescale(xmin=-6, xmax=10, ymin=-8, ymax=8)
# o4_pqt.o_polyquadtile_chart.dataframe_to_csv('medium_rectangle')
o4_pqt.o_polyquadtile_chart.df['shape'] = 'rectangle'

#%%
# T: triangle
poly = [(10.0, 0.0),
 (3.0901699437494745, 2.245139882897927),
 (3.0901699437494745, 9.510565162951535),
 (-1.1803398874989484, 3.632712640026805),
 (-8.090169943749473, 5.877852522924733),
 (-3.819660112501052, 4.677734530605232e-16),
 (-8.090169943749476, -5.87785252292473),
 (-1.180339887498949, -3.6327126400268046),
 (3.0901699437494723, -9.510565162951536),
 (3.090169943749474, -2.245139882897928)]
poly = vf.rotate_polygon(poly,63) #45
o5_pqt = pqt.random_polyquadtile(60, constraints=poly, collapse=True, rotate=45, xc=-1, yc=-1, buffer=.15)
o5_pqt.polyquadtile_plot(show_constraints=True)
#%%
o5_pqt.o_polyquadtile_chart.dataframe_rescale(xmin=-15, xmax=15, ymin=-15, ymax=15)
# o5_pqt.o_polyquadtile_chart.dataframe_to_csv('medium_triangle')
o5_pqt.o_polyquadtile_chart.df['shape'] = 'triangle'

#%%
import os
shapes = [
    o1_pqt.o_polyquadtile_chart.df,
    o2_pqt.o_polyquadtile_chart.df,
    o3_pqt.o_polyquadtile_chart.df,
    o4_pqt.o_polyquadtile_chart.df,
    o5_pqt.o_polyquadtile_chart.df
]
df_shapes = pd.concat(shapes, axis=0)
df_shapes.to_csv(os.path.dirname(__file__) + '/medium_shapes.csv', encoding='utf-8', index=False)
#%% backgroundspalsh image

o_pqt = pqt.random_polyquadtile(150, constraints=[(2,1)], collapse=True)
o_pqt.polyquadtile_plot()
#%%
o_pqt.o_polyquadtile_chart.dataframe_rescale(xmin=-5, xmax=5, ymin=-5, ymax=5)
o_pqt.o_polyquadtile_chart.dataframe_to_csv('medium_pqt_1')

#%% main splash image

poly = [
    (-5.2424418604652,-1.0872093023254),
    (-5.1313953488374,2.022093023256),
    (-4.5761627906978,4.9093023255814),
    (-3.5767441860466,7.796511627907),
    (-2.5773255813954,9.6843023255814),
    (-0.911627906976801,11.7941860465118),
    (0.865116279069598,13.3488372093024),
    (2.975,14.3482558139536),
    (5.4180232558138,14.7924418604652),
    (7.638953488372,14.5703488372094),
    (9.8598837209302,13.793023255814),
    (11.7476744186046,12.4604651162792),
    (13.1912790697674,10.5726744186048),
    (14.6348837209302,8.5738372093024),
    (15.5232558139534,6.2418604651164),
    (16.1895348837208,3.6877906976746),
    (16.6337209302324,1.3558139534884),
    (16.6337209302324,-1.3093023255812),
    (16.4116279069766,-4.085465116279),
    (15.7453488372092,-6.7505813953488),
    (14.856976744186,-9.0825581395348),
    (13.635465116279,-11.4145348837208),
    (12.302906976744,-13.1912790697674),
    (10.7482558139534,-14.4127906976744),
    (9.5267441860464,-14.856976744186),
    (8.0831395348836,-13.8575581395348),
    (6.528488372093,-12.8581395348836),
    (4.7517441860464,-12.1918604651162),
    (3.0860465116278,-11.6366279069766),
    (1.4203488372092,-11.4145348837208),
    (-0.245348837209399,-11.5255813953488),
    (-1.911046511628,-11.8587209302324),
    (-3.021511627907,-10.081976744186),
    (-4.1319767441862,-7.9720930232558),
    (-4.7982558139536,-5.4180232558138),
    (-5.2424418604652,-2.975)
    ]

poly = vf.rotate_polygon(poly,45)
poly = [(x-2,y-1) for x, y in poly]
o_sm1 = sm.random_squaremap(num_levels=3, num_top_level_items=120, items_range=(2,4), 
    value_range=(1,10), sig=0.75, collapse=True, constraints=poly, 
    rotate=45, buffer=.15)
o_sm1.o_squaremap.plot_level(level=3) #, fill='w')
o_sm1.o_squaremap.df_rad_treemap
o_sm1.o_squaremap.o_rad_treemap.df = o_sm1.o_squaremap.df_rad_treemap
o_sm1.o_squaremap.o_rad_treemap.dataframe_rescale(xmin=-11, xmax=20, ymin=-15, ymax=16)
o_sm1.o_squaremap.o_rad_treemap.dataframe_to_csv('medium_squaremap_1')

#%%

#region debugging

##%%
# poly = vf.rotate_polygon(poly,45)
# # poly = [(x-2,y-1) for x, y in poly]
# o_pqt4 = pqt.random_polyquadtile(100, constraints=poly, collapse=True,
#     xc=-2, yc=-1, rotate=45, buffer=.15)
# o_pqt4.polyquadtile_plot(show_constraints=True, color='quad', poly_line='grey')

##%%
# t = np.linspace(0, 2 * np.pi, 50)
# x = 16 * np.sin(t)**3 + 5
# y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
# poly = [(x,y) for x,y in zip(x,y)]
# circle = vf.circle(0,0,10)
# poly = [(x,y) for x,y,_ in circle]
# o_sm1 = sm.random_squaremap(num_levels=3, num_top_level_items=50, items_range=(2,4), 
#     value_range=(1,10), sig=0.8, collapse=True, constraints=poly, 
#     rotate=0, buffer=.5)
# o_sm1.o_squaremap.plot_levels(level=3, fill='w')

##%%
# import os
# poly = [(10.0, 0.0),
#  (4.045084971874737, 2.938926261462366),
#  (3.0901699437494745, 9.510565162951535),
#  (-1.5450849718747368, 4.755282581475768),
#  (-8.090169943749473, 5.877852522924733),
#  (-5.0, 6.123233995736766e-16),
#  (-8.090169943749476, -5.87785252292473),
#  (-1.5450849718747377, -4.755282581475767),
#  (3.0901699437494723, -9.510565162951536),
#  (4.045084971874736, -2.938926261462367)]

##%%
# circle = vf.circle(0,0,10)
# poly = [(x,y) for x,y,_ in circle]

##%%
# t = np.linspace(0, 2 * np.pi, 50)
# x = 16 * np.sin(t)**3
# y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
# poly = [(x,y) for x,y in zip(x,y)]

# o_pqt4 = pqt.random_polyquadtile(300, constraints=poly, collapse=True, 
#     xc=5, rotate=0, buffer=0.2)
# o_pqt4.polyquadtile_plot(show_constraints=True, color='quad', poly_line='grey')

##%%

# poly = vf.rotate_polygon(poly,-45)
# o_pqt4 = pqt.random_polyquadtile(45, constraints=poly, collapse=True, rotate=0, sides=['top'], buffer=0.1)
# o_pqt4.polyquadtile_plot(show_constraints=True, color='quad', poly_line='grey')

##%%
# o_pqt4.df.to_csv(os.path.dirname(__file__) + '/debug_collapse_3.csv', encoding='utf-8', index=False)

##%%
# import os
# poly = [
#     # (10.0, 0.0),
#  (4.045084971874737, 2.938926261462366),
#  (3.0901699437494745, 9.510565162951535),
#  (-1.5450849718747368, 4.755282581475768),
#  (-8.090169943749473, 5.877852522924733),
#  (-1.5450849718747377, -4.755282581475767),
#  ]
# poly = vf.rotate_polygon(poly,-45)
# df = pd.read_csv(os.path.dirname(__file__) + '/debug_collapse_1.csv')
# o_pqt3 = pqt(df, 'id', 'apqt_norm', constraints=poly, collapse=True, rotate=0, sides=['top'], buffer=0.1, auto=False)
# o_pqt3.polyquadtile_plot(show_constraints=True, color='quad', poly_line='grey')

#endregion