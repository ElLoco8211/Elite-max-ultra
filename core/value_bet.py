from core.ml_model import predict

def calculate_edge(match):
    odds = match["odds"]

    probs = {
        "home": predict(odds["home"]),
        "draw": predict(odds["draw"]),
        "away": predict(odds["away"])
    }

    edge = {}

    for k in odds:
        edge[k] = (probs[k] * odds[k]) - 1

    return edge
