import pandas as pd 


# data = pd.read_csv('bordeaux.gtfs/shapes.txt')

troncons = pd.read_csv('troncons_cyclables_bdx.csv', sep=';')

data = pd.read_csv('varmod_mobpro_2021.csv', sep=';')


# print(data.head())

shapes = pd.read_csv('bordeaux.gtfs/shapes.txt')
# print(shapes.head())


routes = pd.read_csv('bordeaux.gtfs/routes.txt')
print(routes.head())
