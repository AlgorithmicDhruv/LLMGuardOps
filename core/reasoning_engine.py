def analyze_risk(
    hallucination,
    toxicity,
    injection,
    response_text=""
):

    analysis = {
        "risk_type": "SAFE",
        "reason": "No major safety concerns detected.",
        "severity": "LOW",
        "recommended_action": "ALLOW"
    }

    # Prompt Injection
    if injection > 0.7:

        analysis = {
            "risk_type": "PROMPT_INJECTION",
            "reason": "User attempted to override or manipulate system instructions.",
            "severity": "CRITICAL",
            "recommended_action": "BLOCK"
        }

    elif injection > 0.4:

        analysis = {
            "risk_type": "PROMPT_INJECTION",
            "reason": "Potential jailbreak or instruction override attempt detected.",
            "severity": "HIGH",
            "recommended_action": "WARN"
        }

    # Toxicity
    elif toxicity > 0.7:

        analysis = {
            "risk_type": "TOXIC_CONTENT",
            "reason": "Generated response contains harmful or offensive language.",
            "severity": "HIGH",
            "recommended_action": "BLOCK"
        }

    # Hallucination
    elif hallucination > 0.6:

        analysis = {
            "risk_type": "HALLUCINATION",
            "reason": "Response may contain fabricated or unsupported claims.",
            "severity": "MEDIUM",
            "recommended_action": "FLAG"
        }

    return analysis