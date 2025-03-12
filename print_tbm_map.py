import pandas as pd
import folium

# Charger les fichiers GTFS
df_shapes = pd.read_csv("bordeaux.gtfs/shapes.txt")  # Tracés des lignes
df_routes = pd.read_csv("bordeaux.gtfs/routes.txt")  # Infos sur les lignes
df_trips = pd.read_csv("bordeaux.gtfs/trips.txt", low_memory=False)  # Fait le lien entre routes et shapes

# Associer chaque `shape_id` à son `route_id`
shape_to_route = df_trips.set_index("shape_id")["route_id"].to_dict()

# Associer chaque `route_id` à son `route_long_name`
route_names = df_routes.set_index("route_id")["route_long_name"].to_dict()

# Associer les couleurs des lignes
route_colors = df_routes.set_index("route_id")["route_color"].to_dict()

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

    # Définir la couleur (par défaut bleu si non trouvée)
    couleur = f"#{route_colors.get(route_id, '0000FF')}"

    # Ajouter le tracé sur la carte
    folium.PolyLine(
        locations=list(zip(shape_data["shape_pt_lat"], shape_data["shape_pt_lon"])),
        color=couleur,
        weight=4,
        opacity=0.3,
        tooltip=route_name  # Infobulle avec le vrai nom de la ligne
    ).add_to(m)

# Sauvegarder et afficher la carte
m.save("results/carte_reseau_TBM.html")
m
