def calculate_risk_score(hallucination, toxicity, injection):

    risk_score = (
        0.3 * hallucination +
        0.2 * toxicity +
        0.5 * injection  
    )

    if injection > 0.6:
        level = "HIGH_RISK"
    elif risk_score < 0.25:
        level = "SAFE"
    elif risk_score < 0.5:
        level = "WARNING"
    else:
        level = "HIGH_RISK"

    return {
        "risk_score": round(risk_score, 4),
        "risk_level": level
    }