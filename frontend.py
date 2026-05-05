import streamlit as st
import requests
import plotly.graph_objects as go
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AEO Diagnostic",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    .main { padding: 2rem 3rem; background: #0a0a0f; }
    
    .hero { text-align: center; padding: 2rem 0 1rem 0; }
    .hero h1 {
        font-size: 3rem; font-weight: 900;
        background: linear-gradient(135deg, #7c6ff7, #a78bfa, #60a5fa);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .hero p { color: #6b7280; font-size: 1.1rem; margin: 0; }

    .report-card {
        background: linear-gradient(145deg, #13131f, #1a1a2e);
        border: 1px solid #2a2a3e;
        border-radius: 20px;
        padding: 1.8rem;
        height: 100%;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s;
    }
    .report-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 20px 20px 0 0;
    }
    .card-green::before { background: linear-gradient(90deg, #10b981, #34d399); }
    .card-yellow::before { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
    .card-red::before { background: linear-gradient(90deg, #ef4444, #f87171); }

    .card-model-name {
        font-size: 0.85rem; font-weight: 600;
        color: #6b7280; text-transform: uppercase;
        letter-spacing: 0.1em; margin-bottom: 1rem;
    }
    .card-score {
        font-size: 4rem; font-weight: 900;
        line-height: 1; margin-bottom: 0.2rem;
    }
    .score-green { color: #10b981; }
    .score-yellow { color: #f59e0b; }
    .score-red { color: #ef4444; }
    .card-score-sub { font-size: 0.9rem; color: #4b5563; margin-bottom: 1.2rem; }

    .pill {
        display: inline-flex; align-items: center; gap: 5px;
        padding: 4px 12px; border-radius: 20px;
        font-size: 0.75rem; font-weight: 600;
        margin: 3px 2px;
    }
    .pill-green { background: #064e3b; color: #34d399; }
    .pill-yellow { background: #451a03; color: #fbbf24; }
    .pill-red { background: #450a0a; color: #f87171; }
    .pill-blue { background: #1e3a5f; color: #60a5fa; }
    .pill-purple { background: #2e1065; color: #a78bfa; }

    .divider { border: none; border-top: 1px solid #1f2937; margin: 1rem 0; }

    .winner-crown {
        position: absolute; top: 1rem; right: 1rem;
        background: linear-gradient(135deg, #f7971e, #ffd200);
        color: #000; font-size: 0.7rem; font-weight: 800;
        padding: 4px 10px; border-radius: 20px;
    }

    .summary-box {
        background: linear-gradient(145deg, #13131f, #1a1a2e);
        border: 1px solid #2a2a3e;
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin: 1.5rem 0;
    }

    .rec-item {
        display: flex; gap: 12px; align-items: flex-start;
        padding: 0.8rem 1rem;
        background: #0d0d1a;
        border-left: 3px solid #7c6ff7;
        border-radius: 0 10px 10px 0;
        margin: 0.5rem 0;
        font-size: 0.9rem; color: #d1d5db;
    }

    .stButton > button {
        background: linear-gradient(135deg, #7c6ff7, #60a5fa);
        color: white; border: none;
        padding: 0.7rem 2rem; border-radius: 10px;
        font-weight: 700; font-size: 1rem; width: 100%;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.85; }

    div[data-testid="metric-container"] {
        background: #13131f;
        border: 1px solid #2a2a3e;
        border-radius: 12px;
        padding: 1rem;
    }
    div[data-testid="stExpander"] {
        background: #0d0d1a;
        border: 1px solid #1f2937;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <h1>🔍 AEO Diagnostic</h1>
    <p>Discover how AI assistants recommend your product — and beat your competition.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Input
with st.form("query_form"):
    c1, c2, c3 = st.columns([3, 2, 2])
    with c1:
        query = st.text_input("Customer Query", placeholder="e.g. best niacinamide serum for oily skin")
    with c2:
        product = st.text_input("Your Brand", placeholder="e.g. Minimalist")
    with c3:
        competitor = st.text_input("Competitor (optional)", placeholder="e.g. The Ordinary")
    submitted = st.form_submit_button("🔍 Generate Report Card")

if submitted and query and product:
    with st.spinner("⚡ Querying 3 AI models in parallel..."):
        try:
            resp = requests.post(
                "http://127.0.0.1:8000/analyze",
                json={"query": query, "product": product, "competitor": competitor},
                timeout=None
            )
            data = resp.json()
            results = data["results"]
            avg = data["avg_score"]
            recs = data["recommendations"]

            # Summary bar
            mentioned = sum(1 for r in results.values() if r["analysis"]["mentioned"])
            total = len(results)

            st.markdown("---")
            st.markdown(f"### 📋 Report Card — *\"{query}\"*")

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Overall AEO Score", f"{avg}/10")
            m2.metric("AI Models Queried", total)
            m3.metric("Mentioned In", f"{mentioned}/{total} models")
            if competitor and any("competitor_analysis" in r for r in results.values()):
                comp_scores = [r["competitor_analysis"]["score"] for r in results.values() if "competitor_analysis" in r]
                comp_avg = round(sum(comp_scores) / len(comp_scores), 1)
                delta = round(avg - comp_avg, 1)
                m4.metric("vs Competitor", f"{comp_avg}/10", delta=f"{delta:+.1f}")
            else:
                m4.metric("Verdict", "Strong" if avg >= 7 else "Moderate" if avg >= 4 else "Weak")

            # Verdict banner
            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
            if avg >= 7:
                st.success(f"✅ **Strong AI visibility** — {product} is actively recommended by AI assistants.")
            elif avg >= 4:
                st.warning(f"⚠️ **Moderate AI visibility** — {product} is mentioned but not leading.")
            else:
                st.error(f"❌ **Low AI visibility** — {product} is not being recommended by AI assistants.")

            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

            # Gauge chart
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=avg,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': f"<b>{product}</b> AEO Score", 'font': {'color': '#d1d5db', 'size': 16}},
                number={'font': {'color': '#a78bfa', 'size': 48}},
                gauge={
                    'axis': {'range': [0, 10], 'tickcolor': '#4b5563', 'tickfont': {'color': '#6b7280'}},
                    'bar': {'color': '#7c6ff7'},
                    'bgcolor': '#1a1a2e',
                    'bordercolor': '#2a2a3e',
                    'steps': [
                        {'range': [0, 4], 'color': '#1a0a0a'},
                        {'range': [4, 7], 'color': '#1a1500'},
                        {'range': [7, 10], 'color': '#0a1a0f'},
                    ],
                    'threshold': {
                        'line': {'color': '#a78bfa', 'width': 3},
                        'thickness': 0.75,
                        'value': avg
                    }
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#d1d5db'},
                height=250,
                margin=dict(t=50, b=0, l=30, r=30)
            )

            # Bar chart comparing models
            model_names = list(results.keys())
            your_scores = [results[m]["analysis"]["score"] for m in model_names]
            
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                name=product,
                x=model_names,
                y=your_scores,
                marker_color='#7c6ff7',
                marker_line_color='#a78bfa',
                marker_line_width=1.5,
                text=your_scores,
                textposition='outside',
                textfont={'color': '#a78bfa', 'size': 14, 'family': 'Inter'}
            ))

            if competitor and any("competitor_analysis" in r for r in results.values()):
                comp_scores_list = [results[m].get("competitor_analysis", {}).get("score", 0) for m in model_names]
                fig_bar.add_trace(go.Bar(
                    name=competitor,
                    x=model_names,
                    y=comp_scores_list,
                    marker_color='#ef4444',
                    marker_line_color='#f87171',
                    marker_line_width=1.5,
                    text=comp_scores_list,
                    textposition='outside',
                    textfont={'color': '#f87171', 'size': 14, 'family': 'Inter'}
                ))

            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                barmode='group',
                font={'color': '#d1d5db', 'family': 'Inter'},
                height=280,
                margin=dict(t=20, b=20, l=20, r=20),
                legend=dict(bgcolor='rgba(0,0,0,0)', font={'color': '#9ca3af'}),
                xaxis=dict(gridcolor='#1f2937', tickfont={'color': '#6b7280'}),
                yaxis=dict(gridcolor='#1f2937', tickfont={'color': '#6b7280'}, range=[0, 13]),
            )

            g1, g2 = st.columns([1, 2])
            with g1:
                st.plotly_chart(fig_gauge, use_container_width=True)
            with g2:
                st.plotly_chart(fig_bar, use_container_width=True)

            st.markdown("---")
            st.markdown("### 🗂️ Model Report Cards")

# Cards - use components.html to bypass Streamlit's HTML sanitizer
            model_items = list(results.items())
            your_scores_dict = {m: results[m]["analysis"]["score"] for m in results}
            winner_model = max(your_scores_dict, key=your_scores_dict.get)

            all_cards_html = """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
            * { font-family: 'Inter', sans-serif; box-sizing: border-box; }
            .grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 1.2rem; }
            .card { background: linear-gradient(145deg,#13131f,#1a1a2e); border: 1px solid #2a2a3e; border-radius: 20px; padding: 1.8rem; position: relative; overflow: hidden; }
            .card-top { position:absolute; top:0; left:0; right:0; height:3px; border-radius:20px 20px 0 0; }
            .model-name { font-size:0.85rem; font-weight:600; color:#6b7280; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:1rem; }
            .score { font-size:4rem; font-weight:900; line-height:1; margin-bottom:0.2rem; }
            .score-sub { font-size:0.9rem; color:#4b5563; margin-bottom:1.2rem; }
            .divider { border:none; border-top:1px solid #1f2937; margin:1rem 0; }
            .pill { display:inline-flex; align-items:center; gap:5px; padding:4px 12px; border-radius:20px; font-size:0.75rem; font-weight:600; margin:3px 2px; }
            .crown { position:absolute; top:1rem; right:1rem; background:linear-gradient(135deg,#f7971e,#ffd200); color:#000; font-size:0.7rem; font-weight:800; padding:4px 10px; border-radius:20px; }
            </style>
            <div class="grid">
            """

            for model_name, result in model_items:
                analysis = result["analysis"]
                score = analysis["score"]
                rank = analysis["rank"]
                sentiment = analysis["sentiment"]
                sentiment_emoji = analysis["sentiment_emoji"]

                if score >= 7:
                    top_color = "linear-gradient(90deg,#10b981,#34d399)"
                    score_color = "#10b981"
                    rank_icon = "🟢"
                elif score >= 3:
                    top_color = "linear-gradient(90deg,#f59e0b,#fbbf24)"
                    score_color = "#f59e0b"
                    rank_icon = "🟡"
                else:
                    top_color = "linear-gradient(90deg,#ef4444,#f87171)"
                    score_color = "#ef4444"
                    rank_icon = "🔴"

                is_winner = (model_name == winner_model and score > 0)
                crown_html = '<div class="crown">👑 Best</div>' if is_winner else ''

                sentiment_bg = "#064e3b" if sentiment == "Positive" else "#450a0a" if sentiment == "Negative" else "#451a03"
                sentiment_color = "#34d399" if sentiment == "Positive" else "#f87171" if sentiment == "Negative" else "#fbbf24"

                comp_html = ""
                if competitor and "competitor_analysis" in result:
                    comp = result["competitor_analysis"]
                    if score > comp["score"]:
                        comp_html = f'<span class="pill" style="background:#064e3b;color:#34d399;">👑 You lead {competitor}</span>'
                    elif comp["score"] > score:
                        comp_html = f'<span class="pill" style="background:#450a0a;color:#f87171;">⚠️ {competitor} leads</span>'
                    else:
                        comp_html = f'<span class="pill" style="background:#2e1065;color:#a78bfa;">🤝 Tied with {competitor}</span>'

                all_cards_html += f"""
                <div class="card">
                    <div class="card-top" style="background:{top_color};"></div>
                    {crown_html}
                    <div class="model-name">{model_name}</div>
                    <div class="score" style="color:{score_color};">{score}<span style="font-size:1.5rem;color:#374151">/10</span></div>
                    <div class="score-sub">AEO Score</div>
                    <hr class="divider">
                    <div style="margin-bottom:0.8rem;">
                        <span class="pill" style="background:#1a1a2e;color:{score_color};">{rank_icon} {rank}</span>
                        <span class="pill" style="background:{sentiment_bg};color:{sentiment_color};">{sentiment_emoji} {sentiment}</span>
                    </div>
                    <div style="margin-top:0.5rem;">{comp_html}</div>
                </div>
                """

            all_cards_html += "</div>"
            components.html(all_cards_html, height=320, scrolling=False)

            # Expanders — native widgets, work fine in columns
            cols = st.columns(3)
            for i, (model_name, result) in enumerate(model_items):
                with cols[i]:
                    with st.expander(f"📄 {model_name} — Full AI Response"):
                        st.write(result["response"])

            cols = st.columns(3)

            # Recommendations
            st.markdown("---")
            st.markdown("### 💡 AI Recommendations")
            for rec in recs:
                st.markdown(f"""
                <div class="rec-item">
                    <span style="font-size:1.2rem">💬</span>
                    <span>{rec}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("<p style='text-align:center;color:#374151;font-size:0.8rem'>AEO Diagnostic • Powered by Gemini 2.0 Flash · Nemotron 3 Super · GPT OSS 120B via OpenRouter</p>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")