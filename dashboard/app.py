import sys
import os
import json
import streamlit as st

# 1. FIX PATHS (Must be at the very top)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2. IMPORTS
from core.llm_service import generate_response
from core.prompt_injection import detect_prompt_injection
from core.toxicity import detect_toxicity
from core.hallucination import detect_hallucination
from core.risk_engine import calculate_risk_score
from core.reasoning_engine import analyze_risk
from core.enforcement import enforce_policy
from core.adversarial_generator import get_adversarial_prompts
from core.logger import log_interaction

# 3. PAGE CONFIG
st.set_page_config(page_title="LLMGuardOps", page_icon="🛡️", layout="wide")

st.title("🛡️ LLMGuardOps")
st.markdown("### **AI Safety & Adversarial Evaluation Dashboard**")
st.divider()

# 4. INPUT AREA
prompt = st.text_area("User Input Prompt", placeholder="Enter a prompt to test safety guardrails...", height=150)

if st.button("🚀 Run Safety Evaluation", use_container_width=True):
    if not prompt.strip():
        st.warning("Please enter a prompt first.")
    else:
        with st.spinner("Analyzing with LLMGuardOps AI Engine..."):
            try:
                # Generate the raw response from the LLM
                raw_response = generate_response(prompt)

                # Run detectors
                inj_score = detect_prompt_injection(prompt)
                tox_score = detect_toxicity(raw_response)
                hall_score = detect_hallucination(prompt, raw_response)

                # Calculate Risk using your updated engine (returns a dict)
                risk_data = calculate_risk_score(hall_score, tox_score, inj_score)
                
                # Analyze Risk (returns a dict)
                analysis = analyze_risk(hall_score, tox_score, inj_score, raw_response)
                
                # Enforce Policy (returns a dict)
                enforcement_result = enforce_policy(raw_response, analysis)
                
                log_interaction(
                    prompt=prompt,
                    raw_response=raw_response,
                    risk_data=risk_data,
                    analysis=analysis,
                    enforcement_result=enforcement_result,
                    category="Manual_Test"
                )

                # --- UI PHASE ---
                st.subheader("Assessment Overview")
                
                # Using containers with borders for a clean "Box" look
                m1, m2, m3 = st.columns(3)
                
                with m1:
                    with st.container(border=True):
                        st.markdown("##### Total Risk Score")
                        # Accessing the key from your updated risk_engine.py
                        st.write(f"## {risk_data['risk_score'] * 100:.1f}%")
                        st.caption(f"Level: {risk_data['risk_level']}")

                with m2:
                    with st.container(border=True):
                        st.markdown("##### Threat Severity")
                        sev = analysis['severity']
                        icon = "🔴" if sev == "CRITICAL" else "🟡" if sev == "HIGH" else "🟢"
                        st.write(f"## {icon} {sev}")
                        st.caption(f"Type: {analysis['risk_type']}")

                with m3:
                    with st.container(border=True):
                        st.markdown("##### Enforcement Action")
                        action = analysis['recommended_action']
                        st.write(f"## {action}")
                        st.caption("Policy Decision")

                st.divider()

                col_left, col_right = st.columns([2, 1])

                with col_left:
                    st.subheader("Final System Output")
                    if enforcement_result['blocked']:
                        st.error(enforcement_result['final_response'])
                    elif "[WARNING]" in enforcement_result['final_response']:
                        st.warning(enforcement_result['final_response'])
                    else:
                        st.info(enforcement_result['final_response'])

                with col_right:
                    st.subheader("Safety Metadata")
                    st.json({
                        "injection_score": inj_score,
                        "toxicity_score": tox_score,
                        "hallucination_score": hall_score,
                        "reason": analysis['reason']
                    })

            except Exception as e:
                st.error(f"Error during evaluation: {str(e)}")

# 5. ADVERSARIAL SECTION
st.divider()
with st.expander("⚔️ Open Adversarial Test Suite"):
    if st.button("Execute Stress Test"):
        adv_suite = get_adversarial_prompts()  # Now receiving a list of dicts
        suite_results = []
        
        my_bar = st.progress(0)
        status_text = st.empty() # Placeholder for dynamic status updates

        for idx, item in enumerate(adv_suite):
            cat = item["category"]
            p = item["prompt"]
            
            # Update status to show WHICH category is being tested
            status_text.markdown(f"**Current Test:** `{cat}`")
            
            # Logic Phase
            r = generate_response(p)
            i = detect_prompt_injection(p)
            t = detect_toxicity(r)
            h = detect_hallucination(p, r)
            
            anlz = analyze_risk(h, t, i, r)
            enf = enforce_policy(r, anlz)
            
            # Add results with Category included
            suite_results.append({
                "Category": cat,
                "Attack Prompt": p[:] + "",
                "Risk Score": calculate_risk_score(h, t, i)['risk_score'],
                "Action": anlz['recommended_action'],
                "Blocked": "✅ Yes" if enf['blocked'] else "❌ No"
            })
            
            risk_data = calculate_risk_score(h, t, i)
            
            # LOG EACH ADVERSARIAL TEST
            log_interaction(
                prompt=p,
                raw_response=r,
                risk_data=risk_data,
                analysis=anlz,
                enforcement_result=enf,
                category=f"Adversarial_{cat}"
            )
            
            # ... (Rest of UI updates)
            # Update progress
            my_bar.progress((idx + 1) / len(adv_suite))
        
        status_text.success("✅ Adversarial Stress Test Complete")
        
        # Display the result table with the Category column first
        st.table(suite_results)