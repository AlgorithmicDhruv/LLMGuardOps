import json
import os
from datetime import datetime

def log_interaction(prompt, raw_response, risk_data, analysis, enforcement_result, category="Manual"):
    """
    Saves the evaluation metrics and results to a local JSON file.
    """
    log_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'eval_logs.json')
    
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # Prepare the log entry
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "category": category,
        "input_prompt": prompt,
        "raw_response": raw_response,
        "risk_metrics": {
            "total_score": risk_data.get('risk_score'),
            "risk_level": risk_data.get('risk_level'),
            "severity": analysis.get('severity'),
            "risk_type": analysis.get('risk_type')
        },
        "decision": {
            "action": analysis.get('recommended_action'),
            "blocked": enforcement_result.get('blocked'),
            "final_output": enforcement_result.get('final_response')
        }
    }

    # Read existing logs or start new list
    logs = []
    if os.path.exists(log_path):
        try:
            with open(log_path, 'r') as f:
                logs = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            logs = []

    logs.append(log_entry)

    # Write back to file
    with open(log_path, 'w') as f:
        json.dump(logs, f, indent=4)