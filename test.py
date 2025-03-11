import geopandas as gpd
import folium
import pandas as pd
import json
import ast
from shapely.geometry import LineString


# Charger le fichier CSV
df = pd.read_csv("troncons_cyclables_bdx.csv", encoding="utf-8", sep=";")

# Afficher les 5 premières lignes
print(df.head())


valeurs_typamena = df["typamena"].unique()
print(valeurs_typamena)