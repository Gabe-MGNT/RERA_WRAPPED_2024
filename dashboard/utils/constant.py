
stations_rer_a_constant_dict = {
    "Achères Grand Cormier":["Achères Grand Cormier"],
    "Achères Ville" : ["Achères Ville"],
    "Auber" : ["Auber"],
    "Boissy-Saint-Léger" : ["Boissy-Saint-Léger", "Boissy-St-Léger", "Boissy", "Poissy Saint Léger"],
    "Bry-sur-Marne": ["Bry-sur-Marne"],
    "Bussy-Saint-Georges": ["Bussy-Saint-Georges", "Bussy-St-Georges"],
    "Cergy le Haut" : ["Cergy le Haut", "Cergy"],
    "Cergy Préfecture" : ["Cergy Préfecture"],
    "Cergy Saint-Christophe" : ["Cergy Saint-Christophe", "Cergy St-Christophe"],
    "Champigny": ["Champigny"],
    "Charles de Gaulle-Etoile" : ["Charles de Gaulle-Etoile"],
    "Châtelet les Halles" : ["Châtelet les Halles"],
    "Chatou-Croissy" : ["Chatou-Croissy"],
    "Conflans Fin d'Oise" : ["Conflans Fin d'Oise", "Conflans – Fin d’Oise"],
    "Fontenay-sous-Bois" : ["Fontenay-sous-Bois", "Fontenay"],
    "Gare de Lyon" : ["Gare de Lyon"],
    "Houilles-Carrières-sur-Seine" : ["Houilles-Carrières-sur-Seine", "Houilles"],
    "Joinville-le-Pont" : ["Joinville-le-Pont"],
    "La Défense" : ["La Défense", "Défense"],
    "La Varenne-Chennevières" :["La Varenne-Chennevières", "Varenne-Chennevières", "Varennes Chennevieres"],
    "Parc de Saint-Maur" : ["Parc de Saint-Maur", "Parc de St-Maur", "Parc Saint-Maur", "Parc St-Maur"],
    "Le Vésinet-Centre" : ["Le Vésinet-Centre", "Vésinet-Centre"],
    "Le Vésinet-Le Pecq" : ["Le Vésinet-Le Pecq", "Vésinet-Le Pecq"],
    "Lognes": ["Lognes"],
    "Maisons-Laffitte" : ["Maisons-Laffitte", "Maison-Laffitte", "Maisons-Laffite", "Maison-Laffite"],
    "Marne-la-Vallée-Chessy" : ["Marne-la-Vallée-Chessy", "MLV-Chessy", "Marne la Vallée", "Chessy"],
    "Nanterre Préfecture" : ['Nanterre Préfecture', "Nantere Pref", "Nanterre-P"],
    "Nanterre Université" : ["Nanterre Université"],
    "Nanterre Ville" : ["Nanterre Ville"],
    "Nation" : ["Nation"],
    "Neuilly-Plaisance" : ["Neuilly-Plaisance"],
    "Neuville Université": ["Neuville Université"],
    "Nogent-sur-Marne" : ["Nogent-sur-Marne"],
    "Noisiel" : ["Noisiel"],
    "Noisy-Champs" : ["Noisy-Champs"],
    "Noisy-le-Grand-Mont d'Est" : ["Noisy-le-Grand-Mont d'Est", "Noisy-le-Grand"],
    "Poissy" : ["Poissy"],
    "Rueil-Malmaison" : ["Rueil-Malmaison"],
    "Saint-Germain-en-Laye" : ["Saint-Germain-en-Laye", "St-Germain-En-Laye", "St Germain", "Saint Germain"],
    "Saint-Maur-Créteil" : ["Saint-Maur-Créteil", "St-Maur-Créteil"],
    "Sartrouville" : ["Sartrouville"],
    "Sucy-Bonneuil" : ["Sucy-Bonneuil"],
    "Torcy" : ["Torcy"],
    "Val d'Europe" : ["Val d'Europe"],
    "Val de Fontenay" : ["Val de Fontenay"],
    "Vincennes" : ["Vincennes"],
}


month_dict = {
    1: "Janvier",
    2: "Février",
    3: "Mars",
    4: "Avril",
    5: "Mai",
    6: "Juin",
    7: "Juillet",
    8: "Août",
    9: "Septembre",
    10: "Octobre",
    11: "Novembre",
    12: "Décembre"
}

max_day_per_month = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}


gare_list = list(stations_rer_a_constant_dict.keys())



line_y_1 = 514
line_y_2 = 342
line_y_3 = 173


x_beginning = 435
x_end = 5576
x_gap_space = 132
x_gare_lyon = x_beginning+(x_gap_space*17) + 2*197

gares = [
    {"name": "Cergy le Haut", "location": [x_beginning, line_y_1], "size": 3},
    {"name": "Cergy Saint-Christophe", "location": [x_beginning+x_gap_space, line_y_1], "size": 3},
    {"name": "Cergy Préfecture", "location": [x_beginning+(x_gap_space*2), line_y_1], "size": 3},
    {"name": "Neuville Université", "location": [x_beginning+(x_gap_space*3), line_y_1], "size": 3},
    {"name": "Conflans Fin d'Oise", "location": [x_beginning+(x_gap_space*4), line_y_1], "size": 3},
    {"name": "Achères Ville", "location": [x_beginning+(x_gap_space*5), line_y_1], "size": 3},
    {"name": "Maisons-Laffitte", "location": [x_beginning+(x_gap_space*7), line_y_1], "size": 3},
    {"name": "Sartrouville", "location": [x_beginning+(x_gap_space*8), line_y_1], "size": 3},
    {"name": "Houilles-Carrières-sur-Seine", "location": [x_beginning+(x_gap_space*9), line_y_1], "size": 3},

    {"name": "Poissy", "location": [x_beginning+(x_gap_space*2), line_y_2], "size": 3},
    {"name": "Achères Grand Cormier", "location": [x_beginning+(x_gap_space*3), line_y_2], "size": 3},

    {"name": "Saint-Germain-en-Laye", "location": [x_beginning+(x_gap_space*4), line_y_3], "size": 3},
    {"name": "Le Vésinet-Le Pecq", "location": [x_beginning+(x_gap_space*5), line_y_3], "size": 3},
    {"name": "Le Vésinet-Centre", "location": [x_beginning+(x_gap_space*6), line_y_3], "size": 3},
    {"name": "Chatou-Croissy", "location": [x_beginning+(x_gap_space*7), line_y_3], "size": 3},
    {"name": "Rueil-Malmaison", "location": [x_beginning+(x_gap_space*8), line_y_3], "size": 3},
    {"name": "Nanterre Ville", "location": [x_beginning+(x_gap_space*9), line_y_3], "size": 3},
    {"name": "Nanterre Université", "location": [x_beginning+(x_gap_space*10), line_y_3], "size": 3},


    {"name": "Nanterre Préfecture", "location": [x_beginning+(x_gap_space*13), line_y_2], "size": 3},
    {"name": "La Défense", "location": [x_beginning+(x_gap_space*14), line_y_2], "size": 3},

    {"name": "Charles de Gaulle-Etoile", "location": [x_beginning+(x_gap_space*16), line_y_2], "size": 3},
    {"name": "Auber", "location": [x_beginning+(x_gap_space*17), line_y_2], "size": 3},
    {"name": "Châtelet les Halles", "location": [x_beginning+(x_gap_space*17) + 198, line_y_2], "size": 3},
    {"name": "Gare de Lyon", "location": [x_gare_lyon, line_y_2], "size": 3},
    {"name": "Nation", "location": [x_gare_lyon+(x_gap_space*1), line_y_2], "size": 3},
    {"name": "Vincennes", "location": [x_gare_lyon+(x_gap_space*2), line_y_2], "size": 3},


    {"name": "Val de Fontenay", "location": [x_gare_lyon+(x_gap_space*5), line_y_1], "size": 3},
    {"name": "Neuilly-Plaisance", "location": [x_gare_lyon+(x_gap_space*7), line_y_1], "size": 3},
    {"name": "Bry-sur-Marne", "location": [x_gare_lyon+(x_gap_space*8), line_y_1], "size": 3},
    {"name": "Noisy-le-Grand-Mont d'Est", "location": [x_gare_lyon+(x_gap_space*10), line_y_1], "size": 3},
    {"name": "Noisy-Champs", "location": [x_gare_lyon+(x_gap_space*11), line_y_1], "size": 3},
    {"name": "Noisiel", "location": [x_gare_lyon+(x_gap_space*13), line_y_1], "size": 3},
    {"name": "Lognes", "location": [x_gare_lyon+(x_gap_space*14), line_y_1], "size": 3},
    {"name": "Torcy", "location": [x_gare_lyon+(x_gap_space*15), line_y_1], "size": 3},
    {"name": "Bussy-Saint-Georges", "location": [x_gare_lyon+(x_gap_space*16), line_y_1], "size": 3},
    {"name": "Val d'Europe", "location": [x_gare_lyon+(x_gap_space*17), line_y_1], "size": 3},
    {"name": "Marne-la-Vallée-Chessy", "location": [x_gare_lyon+(x_gap_space*19), line_y_1], "size": 3},


    {"name": "Fontenay-sous-Bois", "location": [x_gare_lyon+(x_gap_space*5), line_y_3], "size": 3},
    {"name":  "Nogent-sur-Marne", "location": [x_gare_lyon+(x_gap_space*6), line_y_3], "size": 3},
    {"name": "Joinville-le-Pont", "location": [x_gare_lyon+(x_gap_space*7), line_y_3], "size": 3},
    {"name": "Saint-Maur-Créteil", "location": [x_gare_lyon+(x_gap_space*8), line_y_3], "size": 3},
    {"name": "Parc de Saint-Maur", "location": [x_gare_lyon+(x_gap_space*9), line_y_3], "size": 3},
    {"name": "Champigny", "location": [x_gare_lyon+(x_gap_space*10), line_y_3], "size": 3},
    {"name": "La Varenne-Chennevières", "location": [x_gare_lyon+(x_gap_space*11), line_y_3], "size": 3},
    {"name": "Sucy-Bonneuil", "location": [x_gare_lyon+(x_gap_space*13), line_y_3], "size": 3},
    {"name": "Boissy-Saint-Léger", "location": [x_gare_lyon+(x_gap_space*14), line_y_3], "size": 3},

]

