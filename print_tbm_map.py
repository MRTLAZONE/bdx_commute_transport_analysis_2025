import pandas as pd
import folium

# Charger les données (remplacer par la lecture des fichiers CSV si besoin)
df_shapes = pd.read_csv("bordeaux.gtfs/shapes.txt")  # Table contenant les tracés
df_routes = pd.read_csv("bordeaux.gtfs/routes.txt")  # Table contenant les lignes et leurs couleurs

# Créer une carte centrée sur Bordeaux
m = folium.Map(location=[44.8378, -0.5792], zoom_start=12)

# Associer les couleurs aux routes (conversion en dictionnaire)
route_colors = df_routes.set_index("route_id")["route_color"].to_dict()

# Dessiner chaque ligne
for shape_id, shape_data in df_shapes.groupby("shape_id"):
    # Trier les points par `shape_pt_sequence`
    shape_data = shape_data.sort_values("shape_pt_sequence")
    
    # Récupérer `route_id` correspondant à ce `shape_id` (s'il existe)
    route_id = df_routes[df_routes["route_short_name"] == str(shape_id)]["route_id"]
    route_id = route_id.iloc[0] if not route_id.empty else None
    
    # Définir la couleur (par défaut gris clair si non trouvée)
    couleur = f"#{route_colors.get(route_id, '0000FF')}"

    # Ajouter de la transparence uniquement si la couleur est bleue
    if couleur == "#0000FF":
        couleur += "20"  # 80% d'opacité
    
    # Ajouter le tracé sur la carte
    folium.PolyLine(
        locations=list(zip(shape_data["shape_pt_lat"], shape_data["shape_pt_lon"])),
        color=couleur,
        weight=4,
        opacity=0.8,
        tooltip=f"Ligne {shape_id}"
    ).add_to(m)

# Sauvegarder et afficher la carte
m.save("carte_reseau_TBM.html")
m
