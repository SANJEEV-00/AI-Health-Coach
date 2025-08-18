import os
import streamlit as st
from datetime import date

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI Health Coach", page_icon="🩺")
st.title("🩺 AI Personal Health Coach")

st.sidebar.header("Daily inputs")
steps = st.sidebar.number_input("Steps", min_value=0, value=6000, step=500)
water_ml = st.sidebar.number_input("Water (ml)", min_value=0, value=1800, step=100)
sleep_hr = st.sidebar.number_input("Sleep (hours)", min_value=0.0, value=6.5, step=0.5)
rest_hr = st.sidebar.number_input("Resting HR (bpm)", min_value=30, value=74, step=1)
today = st.sidebar.date_input("Date", value=date.today())

def rule_based_advice():
    tips = []
    if steps < 8000: tips.append("Try a 20–30 min brisk walk to hit 8–10k steps.")
    else: tips.append("Great step count—maintain 8–10k on most days.")
    if water_ml < 2000: tips.append("You're a bit low on hydration; aim for ~2–3L/day.")
    if sleep_hr < 7: tips.append("Sleep below 7h—consider a consistent bedtime routine.")
    if rest_hr > 75: tips.append("Resting HR is slightly high; add low‑intensity cardio and de-stress.")
    if not tips: tips.append("Nice balance today! Keep it up 🔥")
    return tips

st.subheader("Today’s Summary")
st.write(f"**Steps:** {steps} • **Water:** {water_ml} ml • **Sleep:** {sleep_hr} h • **Resting HR:** {rest_hr} bpm")

with st.expander("Coach Suggestions (Rules)"):
    for t in rule_based_advice():
        st.markdown(f"- {t}")

if OPENAI_API_KEY and st.checkbox("Also get AI-generated coaching (uses OPENAI_API_KEY)"):
    import openai
    openai.api_key = OPENAI_API_KEY
    prompt = f"""You are a helpful health coach. Given: steps={steps}, water_ml={water_ml}, sleep_hrs={sleep_hr}, resting_hr={rest_hr}.
    Give 4 concise, safe, habit-focused tips for a healthy adult. Avoid medical claims."""
    try:
        from openai import OpenAI
        client = OpenAI()
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}],
            temperature=0.3
        )
        st.subheader("AI Coach Tips")
        st.write(resp.choices[0].message.content)
    except Exception as e:
        st.error(f"LLM call failed: {e}")

st.caption("Disclaimer: Educational only, not medical advice.")
