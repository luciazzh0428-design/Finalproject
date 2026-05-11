import streamlit as st
import openai
import json
import os
import math
from dotenv import load_dotenv
from prompts import CONTEXT_PROMPT, GRAPH_PROMPT, BASELINE_PROMPT

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Cultural Meaning Explorer", page_icon="🔤", layout="wide")
st.title("🔤 AI Cultural Meaning Explorer")
st.caption("Enter a word to explore how its meaning shifts across cultural and literary contexts.")

def call_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def parse_json(raw):
    cleaned = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(cleaned)

if "graph" not in st.session_state:
    st.session_state["graph"] = None
if "contexts" not in st.session_state:
    st.session_state["contexts"] = None

with st.sidebar:
    st.header("📄 Baseline Comparison")
    st.caption("Plain dictionary-style explanation — no context separation.")
    baseline_word = st.text_input("Enter a word", value="moon", key="baseline")
    if st.button("Generate Baseline"):
        with st.spinner("Generating..."):
            result = call_gpt(BASELINE_PROMPT.format(word=baseline_word))
            st.write(result)

col1, col2 = st.columns([1, 2])

with col1:
    word = st.text_input("Enter a word", value="moon", key="main")
    if st.button("Explore →", type="primary"):
        with st.spinner("Generating cultural contexts..."):
            raw = call_gpt(CONTEXT_PROMPT.format(word=word))
            try:
                st.session_state["contexts"] = parse_json(raw)
                st.session_state["word"] = word
                st.session_state["graph"] = None
            except Exception as e:
                st.error(f"Failed to generate contexts: {e}")

    if st.session_state["contexts"]:
        st.subheader("Select a Context")
        for ctx in st.session_state["contexts"]:
            label = f"{ctx.get('emoji', '')} {ctx['label']}"
            if st.button(label, key=ctx["id"], use_container_width=True):
                with st.spinner("Generating semantic network..."):
                    raw = call_gpt(GRAPH_PROMPT.format(
                        word=st.session_state["word"],
                        context=ctx["label"]
                    ))
                    try:
                        st.session_state["graph"] = parse_json(raw)
                        st.session_state["ctx_label"] = ctx["label"]
                    except Exception as e:
                        st.error(f"Failed to generate graph: {e}")

with col2:
    if st.session_state["graph"]:
        g = st.session_state["graph"]
        st.subheader(f'"{st.session_state["word"]}" in {st.session_state["ctx_label"]}')

        nodes = g.get("nodes", [])
        center = g.get("center", {})
        n = len(nodes)
        W, H = 600, 400
        cx, cy, r = W // 2, H // 2, 130

        circles = ""
        lines = ""
        for i, node in enumerate(nodes):
            angle = 2 * math.pi * i / n - math.pi / 2
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            node["_x"] = x
            node["_y"] = y
            lines += f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="#ccc" stroke-width="1.5"/>'
            circles += f'<circle cx="{x}" cy="{y}" r="36" fill="#E8F4FD" stroke="#5B9BD5" stroke-width="1.5"/>'
            short = node["label"] if len(node["label"]) <= 10 else node["label"][:9] + "…"
            circles += f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" font-size="11" fill="#1a3a5c">{short}</text>'

        svg = f'''<svg width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">
          {lines}{circles}
          <circle cx="{cx}" cy="{cy}" r="44" fill="#EEEDFE" stroke="#7F77DD" stroke-width="2"/>
          <text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="middle" font-size="15" font-weight="bold" fill="#3C3489">{center.get("label", "")}</text>
        </svg>'''

        st.markdown(svg, unsafe_allow_html=True)

        st.subheader("Concept Explanations")
        st.info(f"**{center.get('label', '')}**: {center.get('desc', '')}")
        for node in nodes:
            st.write(f"**{node['label']}**: {node['desc']}")