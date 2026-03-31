def kelly_stake(prob, odd, bankroll, fraction=0.5):
    """
    Kelly Criterion (mezzo Kelly default per sicurezza)
    """
    edge = (prob * odd) - 1

    if edge <= 0:
        return 0

    kelly = (prob * (odd - 1) - (1 - prob)) / (odd - 1)

    stake = bankroll * kelly * fraction

    return max(0, round(stake, 2))
