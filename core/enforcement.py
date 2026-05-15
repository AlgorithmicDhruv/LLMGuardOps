def enforce_policy(response, analysis):

    action = analysis["recommended_action"]

    if action == "BLOCK":

        return {
            "final_response": (
                "Response blocked by LLM Guard AI "
                "due to policy violation."
            ),
            "blocked": True
        }

    elif action == "WARN":

        return {
            "final_response": (
                "[WARNING] Potential unsafe behavior detected.\n\n"
                + response
            ),
            "blocked": False
        }

    elif action == "FLAG":

        return {
            "final_response": (
                "[FLAGGED FOR REVIEW]\n\n"
                + response
            ),
            "blocked": False
        }

    return {
        "final_response": response,
        "blocked": False
    }