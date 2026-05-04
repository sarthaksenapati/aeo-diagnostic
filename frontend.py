import streamlit as st
import requests

st.set_page_config(
    page_title="AEO Diagnostic",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main { padding-top: 1rem; }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .hero-sub {
        font-size: 1.1rem;
        color: #888;
        margin-top: 0.2rem;
        margin-bottom: 2rem;
    }
    .score-card {
        background: linear-gradient(135deg, #1e1e2e, #2a2a3e);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid #333;
        margin-bottom: 1rem;
    }
    .model-name {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .big-score {
        font-size: 3rem;
        font-weight: 900;
        line-height: 1;
    }
    .tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 3px 2px;
    }
    .rec-box {
        background: #1a1a2e;
        border-left: 4px solid #667eea;
        padding: 1rem 1.2rem;
        border-radius: 0 12px 12px 0;
        margin: 0.5rem 0;
        font-size: 0.95rem;
    }
    .vs-badge {
        text-align: center;
        font-size: 1.5rem;
        font-weight: 900;
        color: #667eea;
        padding: 1rem;
    }
    .winner-badge {
        background: linear-gradient(135deg, #f7971e, #ffd200);
        color: #000;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.6rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
    }
    .stButton > button:hover {
        opacity: 0.9;
    }
    div[data-testid="metric-container"] {
        background: #1e1e2e;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="hero-title">🔍 AEO Diagnostic</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">Discover how AI assistants recommend your product — and what to do about it.</p>', unsafe_allow_html=True)

# Input form
with st.form("query_form"):
    col1, col2, col3 = st.columns([3, 2, 2])
    with col1:
        query = st.text_input("Customer Query", placeholder="e.g. best niacinamide serum for oily skin")
    with col2:
        product = st.text_input("Your Brand", placeholder="e.g. Minimalist")
    with col3:
        competitor = st.text_input("Competitor Brand (optional)", placeholder="e.g. The Ordinary")

    submitted = st.form_submit_button("🔍 Analyze AI Visibility")

if submitted and query and product:
    with st.spinner("⚡ Querying 3 AI models simultaneously..."):
        try:
            response = requests.post(
                "https://aeo-diagnostic.onrender.com/analyze",
                json={"query": query, "product": product, "competitor": competitor},
                timeout=180
            )
            data = response.json()

            st.markdown("---")

            # Summary metrics
            avg = data["avg_score"]
            total_models = len(data["results"])
            mentioned_count = sum(1 for r in data["results"].values() if r["analysis"]["mentioned"])

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Overall AEO Score", f"{avg}/10")
            m2.metric("Models Queried", total_models)
            m3.metric("Mentioned In", f"{mentioned_count}/{total_models} models")

            if competitor and any("competitor_analysis" in r for r in data["results"].values()):
                comp_scores = [r["competitor_analysis"]["score"] for r in data["results"].values() if "competitor_analysis" in r]
                comp_avg = round(sum(comp_scores) / len(comp_scores), 1)
                m4.metric("Competitor Score", f"{comp_avg}/10", delta=f"{round(avg - comp_avg, 1)} vs you")
            else:
                m4.metric("Sentiment", "Positive" if avg >= 7 else "Neutral" if avg >= 4 else "Low")

            st.markdown("---")

            # Overall verdict
            if avg >= 7:
                st.success(f"✅ Strong AI visibility for **{product}**. AI models actively recommend your brand.")
            elif avg >= 4:
                st.warning(f"⚠️ Moderate AI visibility for **{product}**. You're mentioned but not leading.")
            else:
                st.error(f"❌ Low AI visibility for **{product}**. AI models are not recommending your brand.")

            st.markdown("---")
            st.markdown(f"### Results for: *\"{query}\"*")

            # Model results
            cols = st.columns(total_models)
            for i, (model_name, result) in enumerate(data["results"].items()):
                analysis = result["analysis"]
                score = analysis["score"]

                with cols[i]:
                    if score == 10:
                        color = "🟢"
                        score_color = "#00d09c"
                    elif score >= 3:
                        color = "🟡"
                        score_color = "#ffd200"
                    else:
                        color = "🔴"
                        score_color = "#ff4b4b"

                    st.markdown(f"#### {color} {model_name}")
                    st.markdown(f"<p style='font-size:2.5rem;font-weight:900;color:{score_color};margin:0'>{score}<span style='font-size:1rem;color:#888'>/10</span></p>", unsafe_allow_html=True)
                    st.markdown(f"**{product}:** {analysis['rank']} {analysis['sentiment_emoji']}")
                    st.markdown(f"Sentiment: **{analysis['sentiment']}**")

                    if competitor and "competitor_analysis" in result:
                        comp = result["competitor_analysis"]
                        st.markdown(f"**{competitor}:** {comp['rank']} {comp['sentiment_emoji']}")

                        if score > comp["score"]:
                            st.markdown("<span class='winner-badge'>👑 You Win</span>", unsafe_allow_html=True)
                        elif comp["score"] > score:
                            st.markdown(f"<span style='color:#ff4b4b;font-size:0.8rem;font-weight:700'>⚠️ Competitor leads</span>", unsafe_allow_html=True)
                        else:
                            st.markdown("<span style='color:#888;font-size:0.8rem'>🤝 Tied</span>", unsafe_allow_html=True)

                    with st.expander("See full AI response"):
                        st.write(result["response"])

            # Recommendations
            st.markdown("---")
            st.markdown("### 💡 Recommendations")
            for rec in data["recommendations"]:
                st.markdown(f"<div class='rec-box'>💬 {rec}</div>", unsafe_allow_html=True)

            # Footer
            st.markdown("---")
            st.markdown("<p style='text-align:center;color:#555;font-size:0.8rem'>AEO Diagnostic • Powered by Hunyuan, Nemotron 120B, GPT OSS 120B via OpenRouter</p>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")