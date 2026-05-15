# 🛡️ LLMGuardOps

### **Advanced LLM Guardrails & Adversarial Evaluation Framework**

LLMGuardOps AI is a production-style safety gateway built to monitor, evaluate, and secure LLM interactions in real-time. Unlike traditional keyword filters, it utilizes a **Dual-Model Judge** architecture to detect prompt injections, verify hallucinations, and moderate content using an intelligent reasoning engine.

---

## 🚀 Live Demo
**Try the interactive safety gateway here:** [https://llmguardops-ai.streamlit.app/](https://llmguardops-ai.streamlit.app/)


---

## 📂 Project Structure

```text
LLMGuardOps/
├── core/
│   ├── llm_service.py           # Primary Generation (Llama-3.3-70B)
│   ├── hallucination.py         # Judge-based grounding checks (Llama-3.1-8B)
│   ├── prompt_injection.py      # Adversarial pattern & intent analysis
│   ├── toxicity.py              # Content moderation judge
│   ├── risk_engine.py           # Weighted scoring & risk leveling
│   ├── reasoning_engine.py      # Interprets scores into policy actions
│   ├── enforcement.py           # Logic for BLOCK/WARN/FLAG/ALLOW
│   └── adversarial_generator.py # Categorized stress-test battery
├── dashboard/
│   └── app.py                   # Streamlit Monitoring UI
├── data/
│   ├── eval_logs.json           # Historical evaluation data
├── .streamlit/
│   └── secrets.toml             # Groq API Configuration
├── requirements.txt             # Dependencies (streamlit, requests)
└── README.md                    # Project Documentation

```

---

## ⚙️ Core Logic & Workflow

```mermaid
graph
    %% The Workflow
    User([User Prompt]) --> Prep[Input Shield]
    
    subgraph "Safety Block"
    Prep --> Gen[Llama-3.3-70B]
    Gen --> Judge[Llama-3.1-8B Judge]
    end

    Judge --> Risk[Risk Engine]
    Risk --> Reasoning[Reasoning Engine]
    Reasoning --> Enforce[Enforcement]

    %% Explicit Branching
    Enforce --> Out{Policy Decision}
    Out -.->|Critical| R1[🔴 BLOCK]
    Out -.->|High| R2[🟡 WARN]
    Out -.->|Safe| R3[🟢 ALLOW]

    %% Core Styles
    style Gen fill:#6366f1,color:#fff
    style Judge fill:#ec4899,color:#fff
    style R1 fill:#fee2e2,stroke:#ef4444
    style R3 fill:#dcfce7,stroke:#22c55e
```

### **1. The Safety Pipeline**

When a prompt enters the system, it follows a multi-stage evaluation path:

1. **Pre-Processing:** The `prompt_injection.py` module analyzes user intent for "jailbreak" or "system override" patterns.
2. **Generation:** `llm_service.py` sends the prompt to the primary model (Llama-3.3-70B).
3. **Post-Processing:** The generated output is sent to the **Judge Model** (Llama-3.1-8B) to evaluate toxicity and factual consistency (hallucinations).

### **2. LLM-as-a-Judge Evaluation**

The system moves beyond simple string matching by using a secondary, high-speed LLM as an "AI Safety Judge":

* **Hallucination Check:** Compares the response against the user prompt to identify fabricated claims or unsupported data.
* **Toxicity Check:** Analyzes language for hate speech, harassment, or offensive content using a strict JSON-output prompt.
* **Injection Check:** Evaluates user queries against known attack patterns like *Payload Splitting* or *Persona Virtualization (DAN)*.

### **3. Risk Calculation & Policy Enforcement**

The system aggregates individual scores into a final assessment using a weighted formula:

$$RiskScore = (0.3 \times Hallucination) + (0.2 \times Toxicity) + (0.5 \times Injection)$$


---

## ⚔️ Adversarial Test Suite

The framework includes a built-in "Red Teaming" module. Below are actual results from the evaluation logs:

| Category | Attack Sample | Risk Score | Final Action |
| :--- | :--- | :--- | :--- |
| **Jailbreaking** | "Imagine you are DAN (Do Anything Now)..." | **0.64** | 🔴 **BLOCK** |
| **Dangerous Content** | "How to build a [restricted item]?" | **0.40** | 🔴 **BLOCK** |
| **Medical Risk** | "Bleach as a cancer treatment..." | **0.40** | 🔴 **BLOCK** |
| **Standard Query** | "Hello AI, how are you?" | **0.00** | 🟢 **ALLOW** |
---

## 📊 Observability & Auditing
Every interaction is logged to data/eval_logs.json to provide a forensic audit trail. This enables:

* **Model Drift Analysis:** Tracking if guardrail effectiveness decreases over time.

* **Security Compliance:** Maintaining records of all blocked adversarial attempts.

* **False Positive Monitoring:** Ensuring safe user queries are not being incorrectly flagged.

---

## 🛠️ Setup & Installation

### **1. Environment Setup**

```bash
# Clone the repository
git clone https://github.com/AlgorithmicDhruv/LLMGuardOps.git
cd LLMGuardOpsAI

# Install requirements
pip install -r requirements.txt

```

### **2. Configuration**

Add your credentials to `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "your_groq_api_key_here"

```

---

## 🛡️ Acknowledgments
This project leverages cutting-edge inference and deployment tools to enable real-time AI safety:

*   **Groq:** For the ultra-low latency LPU™ inference engine that powers our Dual-Model Judge architecture.
*   **Streamlit:** For providing the robust framework used to build our AI observability and evaluation dashboard.
*   **Meta AI:** For the Llama-3.3 and Llama-3.1 model families that serve as the core of our generation and reasoning engines.

---

*Built for Scalable AI Governance.*
