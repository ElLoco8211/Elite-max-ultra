def is_good_bet(edge, prob, odd):
    # regole stile hedge fund
    if edge < 0.04:
        return False
    if prob < 0.40:
        return False
    if odd < 1.8 or odd > 5.0:
        return False
    return True
