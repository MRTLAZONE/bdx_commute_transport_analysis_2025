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

# --- 1. Calcul de l'intensité des bus ---
# Compter le nombre de trajets (`trip_id`) par ligne
route_frequencies = df_trips.groupby("route_id")["trip_id"].count()

# Normaliser les valeurs entre 0 et 1
min_freq, max_freq = route_frequencies.min(), route_frequencies.max()
route_frequencies = (route_frequencies - min_freq) / (max_freq - min_freq)

# Définir une palette de couleurs (bleu → rouge selon l'intensité)
colormap = matplotlib.colormaps.get_cmap("coolwarm")  # Palette de couleurs (bleu → rouge)
route_color_intensity = {
    route_id: mcolors.to_hex(colormap(freq))  # Convertir en couleur hex
    for route_id, freq in route_frequencies.items()
}

# --- 2. Palette de couleurs pour les autres types de transport ---
route_type_colors = {
    0: "#FF6600",  # Tramway (orange)
    1: "#CC0000",  # Métro (rouge)
    2: "#0000CC",  # Train (bleu)
    3: "BUS_INTENSITY",  # Les bus seront colorés dynamiquement
    4: "#009900",  # Ferry (vert)
    5: "#9966CC",  # Téléphérique (violet)
    6: "#666666",  # Funiculaire (gris)
}

route_types_dico ={
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

    # Appliquer la couleur : 
    if route_type == 3:  # Si c'est un bus, on utilise l'intensité
        couleur = route_color_intensity.get(route_id, "#0000FF")  # Par défaut bleu
    else:  # Sinon, on utilise la couleur par type de transport
        couleur = route_type_colors.get(route_type, "#0000FF")

    # Ajouter le tracé sur la carte
    folium.PolyLine(
        locations=list(zip(shape_data["shape_pt_lat"], shape_data["shape_pt_lon"])),
        color=couleur,
        weight=4,
        opacity=0.8,
        tooltip=f"{route_name} (Type: {route_types_dico.get(route_type, 'Inconnu')})"
    ).add_to(m)

# Sauvegarder et afficher la carte
m.save("results/carte_reseau_TBM_intensite.html")
m
