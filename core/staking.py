def kelly(prob, odd, bankroll=100):
    edge = (prob * odd) - 1
    if edge <= 0:
        return 0

    fraction = (prob * odd - 1) / (odd - 1)
    return round(bankroll * fraction * 0.5, 2)
