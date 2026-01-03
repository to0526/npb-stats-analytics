def expectation_star(pred_ops: float) -> str:
    if pred_ops >= 0.900:
        return "★★★★★"
    elif pred_ops >= 0.800:
        return "★★★★☆"
    elif pred_ops >= 0.700:
        return "★★★☆☆"
    elif pred_ops >= 0.600:
        return "★★☆☆☆"
    else:
        return "★☆☆☆☆"
