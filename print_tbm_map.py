import pandas as pd
import folium
import numpy as np
import matplotlib
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# Charger les fichiers GTFS
df_shapes = pd.read_csv("bordeaux.gtfs/shapes.txt")  # Tracés des lignes
df_routes = pd.read_csv("bordeaux.gtfs/routes.txt")  # Infos sur les lignes
df_trips = pd.read_csv("bordeaux.gtfs/trips.txt", low_memory=False)  # Lien entre routes et shapes

# Associer chaque `shape_id` à son `route_id`
shape_to_route = df_trips.set_index("shape_id")["route_id"].to_dict()

# Associer chaque `route_id` à son `route_long_name`
route_names = df_routes.set_index("route_id")["route_long_name"].to_dict()

# Associer chaque `route_id` à son `route_type`
route_types = df_routes.set_index("route_id")["route_type"].to_dict()

# --- 1. Calcul de l'intensité des transports ---
# Compter le nombre de trajets (`trip_id`) par ligne
route_frequencies = df_trips.groupby("route_id")["trip_id"].count()

# Normaliser les valeurs entre 0 et 1
min_freq, max_freq = route_frequencies.min(), route_frequencies.max()
route_frequencies = (route_frequencies - min_freq) / (max_freq - min_freq)

# Définir des palettes adaptées aux types de transport
bus_colormap = matplotlib.colormaps.get_cmap("RdYlGn_r")  # Rouge → Vert (inverse pour que vert = fréquent)
tram_colormap = matplotlib.colormaps.get_cmap("Purples")  # Violet → Bleu (plus intense = fréquent)

route_color_intensity = {}
for route_id, freq in route_frequencies.items():
    route_type = route_types.get(route_id, 3)  # Par défaut, considérer que c'est un bus (3)
    if route_type == 3:  # Bus
        couleur = mcolors.to_hex(bus_colormap(freq))
    elif route_type == 0:  # Tramway
        couleur = mcolors.to_hex(tram_colormap(freq))
    else:
        couleur = "#0000FF"  # Couleur par défaut
    route_color_intensity[route_id] = couleur

# --- 2. Palette de couleurs pour les autres types de transport ---
route_type_colors = {
    0: "TRAM_INTENSITY",  # Tramway (sera coloré dynamiquement)
    1: "#CC0000",  # Métro (rouge)
    2: "#0000CC",  # Train (bleu)
    3: "BUS_INTENSITY",  # Bus (sera coloré dynamiquement)
    4: "#009900",  # Ferry (vert)
    5: "#9966CC",  # Téléphérique (violet)
    6: "#666666",  # Funiculaire (gris)
}

route_types_dico = {
    0: "Tramway",
    1: "Métro",
    2: "Train",
    3: "Bus",
    4: "Bateau",
    5: "Téléphérique",
    6: "Funiculaire"
}

# --- 3. Création de la carte ---
m = folium.Map(location=[44.8378, -0.5792], zoom_start=12)

# Dessiner chaque ligne
for shape_id, shape_data in df_shapes.groupby("shape_id"):
    # Trier les points par `shape_pt_sequence`
    shape_data = shape_data.sort_values("shape_pt_sequence")

    # Trouver le `route_id` correspondant
    route_id = shape_to_route.get(shape_id)

    # Trouver le `route_long_name`
    route_name = route_names.get(route_id, f"Ligne {shape_id}")

    # Trouver le `route_type`
    route_type = route_types.get(route_id, 3)  # Par défaut, considérer que c'est un bus (3)

    # Appliquer la couleur en fonction de l'intensité
    couleur = route_color_intensity.get(route_id, "#0000FF")

    # Ajouter le tracé sur la carte
    folium.PolyLine(
        locations=list(zip(shape_data["shape_pt_lat"], shape_data["shape_pt_lon"])),
        color=couleur,
        weight=4,
        opacity=1,
        tooltip=f"{route_name} (Type: {route_types_dico.get(route_type, 'Inconnu')})"
    ).add_to(m)

# Sauvegarder et afficher la carte
m.save("results/carte_reseau_TBM_intensite.html")
m
