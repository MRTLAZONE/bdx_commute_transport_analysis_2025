import geopandas as gpd
import folium
import pandas as pd
import json
import ast
from shapely.geometry import LineString
from branca.element import Template, MacroElement


# Charger le fichier CSV
df = pd.read_csv("troncons_cyclables_bdx.csv", encoding="utf-8", sep=";")

# Afficher les 5 premières lignes
print(df.head())

# Convertir la colonne Geo Shape en objets géométriques utilisables
def convert_to_linestring(geo_shape):
    try:
        coordinates = ast.literal_eval(geo_shape)["coordinates"]  # Convertir en liste Python
        return LineString(coordinates)
    except:
        return None  # Gérer les erreurs

# Appliquer la conversion
df["geometry"] = df["Geo Shape"].apply(convert_to_linestring)

# Dictionnaire de couleurs pour chaque type d'aménagement cyclable
color_mapping = {
    "DBLE_SENS_PIST_CYCL": "blue",
    "VOIE_VERTE": "green",
    "AIRE_PIETONNE": "purple",
    "TRAVERSEE": "orange",
    "RACCORD": "gray",
    "PISTES_CYCL": "red",
    "ALLEES_DE_PARCS": "lightgreen",
    "ZONE_30_DBLE_SENS": "pink",
    "BANDES_CYCL": "brown",
    "ZONE_30_SENS_UNIQUE": "yellow",
    "DBLE_SENS_CYCL": "cyan",
    "BANDES_CYCL_DBLE_SENS": "darkblue",
    "COULOIRS_BUS": "black",
    "ZONE_RENCONTRE": "gold",
    "CHAUSS_CENTR_BAN": "darkred",
    "VELORUE": "teal"
}



# Convertir en GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")


# Créer une carte centrée sur Bordeaux
m = folium.Map(location=[44.8378, -0.5792], zoom_start=12)

# Ajouter les tronçons cyclables avec un code couleur
for _, row in gdf.iterrows():
    if row["geometry"]:  # Vérifier que la géométrie est valide
        couleur = color_mapping.get(row["typamena"], "gray")  # Gris par défaut si non défini
        folium.PolyLine(
            locations=[(lat, lon) for lon, lat in row["geometry"].coords],  # Inverser lat/lon
            color=couleur,
            weight=3,
            opacity=0.8,
            tooltip=f"{row['typamena']}"  # Infobulle avec le type d’aménagement
        ).add_to(m)

# Définir le HTML pour la légende
legend_html = """
<div style="
    position: fixed; 
    bottom: 50px; left: 50px; width: 250px; height: 400px; 
    background-color: white; z-index:9999; font-size:14px;
    border:2px solid grey; padding: 10px; overflow-y: auto;">
    <b>Légende des aménagements cyclables</b><br>
    <i style="background:blue; width:10px; height:10px; display:inline-block;"></i> Double sens piste cyclable<br>
    <i style="background:green; width:10px; height:10px; display:inline-block;"></i> Voie verte<br>
    <i style="background:purple; width:10px; height:10px; display:inline-block;"></i> Aire piétonne<br>
    <i style="background:orange; width:10px; height:10px; display:inline-block;"></i> Traversée<br>
    <i style="background:gray; width:10px; height:10px; display:inline-block;"></i> Raccord<br>
    <i style="background:red; width:10px; height:10px; display:inline-block;"></i> Pistes cyclables<br>
    <i style="background:lightgreen; width:10px; height:10px; display:inline-block;"></i> Allées de parcs<br>
    <i style="background:pink; width:10px; height:10px; display:inline-block;"></i> Zone 30 double sens<br>
    <i style="background:brown; width:10px; height:10px; display:inline-block;"></i> Bandes cyclables<br>
    <i style="background:yellow; width:10px; height:10px; display:inline-block;"></i> Zone 30 sens unique<br>
    <i style="background:cyan; width:10px; height:10px; display:inline-block;"></i> Double sens cyclable<br>
    <i style="background:darkblue; width:10px; height:10px; display:inline-block;"></i> Bandes cyclables double sens<br>
    <i style="background:black; width:10px; height:10px; display:inline-block;"></i> Couloirs de bus<br>
    <i style="background:gold; width:10px; height:10px; display:inline-block;"></i> Zone de rencontre<br>
    <i style="background:darkred; width:10px; height:10px; display:inline-block;"></i> Chaussée centrale banalisée<br>
    <i style="background:teal; width:10px; height:10px; display:inline-block;"></i> Vélorue<br>
</div>
"""

# Ajouter la légende à la carte
legend = MacroElement()
legend._template = Template(legend_html)
m.get_root().add_child(legend)


# Sauvegarder et afficher la carte
m.save("carte_cyclable_bordeaux_coloree.html")
m