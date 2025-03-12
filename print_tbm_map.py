import pandas as pd
import folium

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

# Palette de couleurs en fonction du type de transport
route_type_colors = {
    0: "#FF6600",  # Tramway
    1: "#CC0000",  # Métro
    2: "#0000CC",  # Train de banlieue
    3: "#00B1EB",  # Bus
    4: "#009900",  # Ferry
    5: "#9966CC",  # Téléphérique
    6: "#666666",  # Funiculaire
}

route_type_names = {
    0: "Tramway",
    3: "Bus",
    4: "Bateau",
}

# Créer une carte centrée sur Bordeaux
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

    # Définir la couleur en fonction du `route_type`
    couleur = route_type_colors.get(route_type, "#0000FF")  # Bleu par défaut si non trouvé

    # Ajouter le tracé sur la carte
    folium.PolyLine(
        locations=list(zip(shape_data["shape_pt_lat"], shape_data["shape_pt_lon"])),
        color=couleur,
        weight=4,
        opacity=0.7,
        tooltip=f"{route_name} (Type: {route_type_names.get(route_type)})"
    ).add_to(m)

# Sauvegarder et afficher la carte
m.save("results/carte_reseau_TBM.html")
m
