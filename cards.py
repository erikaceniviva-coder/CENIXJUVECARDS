import random

RARITIES = {
    "COMMON": {"chance": 55, "color": "#BFC3CA"},
    "RARE": {"chance": 27, "color": "#6EA8FF"},
    "EPIC": {"chance": 13, "color": "#B58AFF"},
    "LEGENDARY": {"chance": 5, "color": "#E6D69B"},
}

LEGENDS = [
    {"name":"Alessandro Del Piero","slug":"del-piero","rating":99,"number":10},
    {"name":"Gianluigi Buffon","slug":"buffon","rating":98,"number":1},
    {"name":"Zinedine Zidane","slug":"zidane","rating":98,"number":21},
    {"name":"Roberto Baggio","slug":"baggio","rating":97,"number":10},
    {"name":"Andrea Pirlo","slug":"pirlo","rating":97,"number":21},
    {"name":"Pavel Nedved","slug":"nedved","rating":96,"number":11},
    {"name":"David Trezeguet","slug":"trezeguet","rating":96,"number":17},
    {"name":"Giorgio Chiellini","slug":"chiellini","rating":96,"number":3},
    {"name":"Leonardo Bonucci","slug":"bonucci","rating":95,"number":19},
    {"name":"Claudio Marchisio","slug":"marchisio","rating":94,"number":8},
    {"name":"Edgar Davids","slug":"davids","rating":94,"number":26},
    {"name":"Michel Platini","slug":"platini","rating":99,"number":10},
    {"name":"Gaetano Scirea","slug":"scirea","rating":99,"number":6},
    {"name":"Omar Sivori","slug":"sivori","rating":98,"number":10},
    {"name":"John Charles","slug":"charles","rating":97,"number":9},
]

def open_pack(pack_type="normal", players=None):
    if pack_type == "legends":
        pool = LEGENDS
        collection_type = "LEGENDS"
    else:
        pool = players or []
        collection_type = "JUVE"

    if not pool:
        raise ValueError("Non ci sono figurine disponibili per questa bustina")

    names = list(RARITIES.keys())
    weights = [RARITIES[name]["chance"] for name in names]
    rarity = random.choices(names, weights=weights, k=1)[0]
    player = random.choice(pool)

    return {
        **player,
        "rarity": rarity,
        "color": RARITIES[rarity]["color"],
        "collection_type": collection_type,
    }
