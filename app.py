from flask import Flask, render_template, jsonify, request, redirect
from cards import open_pack as draw_pack
from collection import add_card, get_collection

app = Flask(__name__)

players = [
    {"name":"Kamil Grabara","number":1,"role":"Portiere","country":"Polonia","rating":84},
    {"name":"Carlo Pinsoglio","number":23,"role":"Portiere","country":"Italia","rating":75},
    {"name":"Guglielmo Vicario","number":25,"role":"Portiere","country":"Italia","rating":86},
    {"name":"Norberto Neto","number":33,"role":"Portiere","country":"Brasile","rating":80},
    {"name":"Zeki Çelik","number":2,"role":"Difensore","country":"Turchia","rating":81},
    {"name":"Gleison Bremer","number":3,"role":"Difensore","country":"Brasile","rating":89},
    {"name":"Federico Gatti","number":4,"role":"Difensore","country":"Italia","rating":82},
    {"name":"Lloyd Kelly","number":6,"role":"Difensore","country":"Inghilterra","rating":80},
    {"name":"Pierre Kalulu","number":15,"role":"Difensore","country":"Francia","rating":83},
    {"name":"Andrea Cambiaso","number":20,"role":"Difensore","country":"Italia","rating":85},
    {"name":"Daniele Rugani","number":24,"role":"Difensore","country":"Italia","rating":78},
    {"name":"Jhon Lucumí","number":26,"role":"Difensore","country":"Colombia","rating":81},
    {"name":"Juan Cabal","number":32,"role":"Difensore","country":"Colombia","rating":79},
    {"name":"Manuel Locatelli","number":5,"role":"Centrocampista","country":"Italia","rating":84},
    {"name":"Teun Koopmeiners","number":8,"role":"Centrocampista","country":"Paesi Bassi","rating":86},
    {"name":"Douglas Luiz","number":12,"role":"Centrocampista","country":"Brasile","rating":85},
    {"name":"Kerim Alajbegović","number":17,"role":"Centrocampista","country":"Bosnia","rating":78},
    {"name":"Khéphren Thuram","number":19,"role":"Centrocampista","country":"Francia","rating":85},
    {"name":"Weston McKennie","number":22,"role":"Centrocampista","country":"USA","rating":83},
    {"name":"Pape Matar Sarr","number":29,"role":"Centrocampista","country":"Senegal","rating":82},
    {"name":"Nico González","number":31,"role":"Centrocampista","country":"Argentina","rating":82},
    {"name":"Francisco Conceição","number":7,"role":"Attaccante","country":"Portogallo","rating":85},
    {"name":"Randal Kolo Muani","number":9,"role":"Attaccante","country":"Francia","rating":85},
    {"name":"Kenan Yildiz","number":10,"role":"Attaccante","country":"Turchia","rating":88},
    {"name":"Edon Zhegrova","number":11,"role":"Attaccante","country":"Kosovo","rating":82},
    {"name":"Jérémie Boga","number":13,"role":"Attaccante","country":"Costa d'Avorio","rating":80},
    {"name":"Arkadiusz Milik","number":14,"role":"Attaccante","country":"Polonia","rating":80},
    {"name":"Jeff Ekhator","number":18,"role":"Attaccante","country":"Italia","rating":76},
    {"name":"Nick Woltemade","number":27,"role":"Attaccante","country":"Germania","rating":84},
]

legends = [
    {"name":"Alessandro Del Piero","number":10,"role":"Attaccante","period":"1993–2012","rating":99,"slug":"del-piero","initials":"AD"},
    {"name":"Gianluigi Buffon","number":1,"role":"Portiere","period":"2001–2018","rating":98,"slug":"buffon","initials":"GB"},
    {"name":"Pavel Nedved","number":11,"role":"Centrocampista","period":"2001–2009","rating":96,"slug":"nedved","initials":"PN"},
    {"name":"David Trezeguet","number":17,"role":"Attaccante","period":"2000–2010","rating":96,"slug":"trezeguet","initials":"DT"},
    {"name":"Roberto Baggio","number":10,"role":"Attaccante","period":"1990–1995","rating":97,"slug":"baggio","initials":"RB"},
    {"name":"Zinedine Zidane","number":21,"role":"Centrocampista","period":"1996–2001","rating":98,"slug":"zidane","initials":"ZZ"},
    {"name":"Andrea Pirlo","number":21,"role":"Centrocampista","period":"2011–2015","rating":97,"slug":"pirlo","initials":"AP"},
    {"name":"Claudio Marchisio","number":8,"role":"Centrocampista","period":"2006–2018","rating":94,"slug":"marchisio","initials":"CM"},
    {"name":"Giorgio Chiellini","number":3,"role":"Difensore","period":"2005–2022","rating":96,"slug":"chiellini","initials":"GC"},
    {"name":"Leonardo Bonucci","number":19,"role":"Difensore","period":"2010–2023","rating":95,"slug":"bonucci","initials":"LB"},
    {"name":"Edgar Davids","number":26,"role":"Centrocampista","period":"1997–2004","rating":94,"slug":"davids","initials":"ED"},
    {"name":"Michel Platini","number":10,"role":"Centrocampista","period":"1982–1987","rating":99,"slug":"platini","initials":"MP"},
    {"name":"Gaetano Scirea","number":6,"role":"Difensore","period":"1974–1988","rating":99,"slug":"scirea","initials":"GS"},
    {"name":"Omar Sivori","number":10,"role":"Attaccante","period":"1957–1965","rating":98,"slug":"sivori","initials":"OS"},
    {"name":"John Charles","number":9,"role":"Attaccante","period":"1957–1962","rating":97,"slug":"charles","initials":"JC"},
]

def prepare_players(items):
    for player in items:
        if "slug" not in player:
            player["slug"] = (
                player["name"].lower()
                .replace(" ", "-")
                .replace("ç", "c")
                .replace("é", "e")
                .replace("á", "a")
                .replace("ó", "o")
                .replace("ü", "u")
                .replace("è", "e")
            )
        player.setdefault(
            "initials",
            "".join(part[0] for part in player["name"].split()[:2]).upper()
        )

prepare_players(players)
prepare_players(legends)

@app.route("/")
def home():
    return render_template("index.html", players=players, legends=legends, cards=get_collection())

@app.route("/packs")
def packs():
    return redirect("/album#packs")

@app.route("/packs/legends")
def legends_packs():
    return redirect("/album#legends-packs")

@app.route("/api/open-pack", methods=["POST"])
def api_open_pack():
    data = request.get_json(silent=True) or {}
    pack_type = data.get("type", "normal")

    if pack_type not in ("normal", "legends"):
        return jsonify({"error": "Tipo di bustina non valido"}), 400

    try:
        pool = legends if pack_type == "legends" else players
        card = draw_pack(pack_type, pool)
        add_card(card)
        return jsonify(card)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

@app.route("/album")
def album():
    cards = get_collection()
    return render_template(
        "album.html",
        cards=cards,
        players=players,
        legends=legends,
        owned={c["slug"]: c for c in cards}
    )

@app.route("/del-piero")
def del_piero():
    return redirect("/album#del-piero")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
