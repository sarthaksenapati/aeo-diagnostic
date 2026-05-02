import streamlit as st
import requests

st.set_page_config(page_title="AEO Diagnostic", page_icon="🔍", layout="wide")

st.title("🔍 AEO Diagnostic Tool")
st.subheader("See how your product ranks when AI assistants answer customer questions")

with st.form("query_form"):
    query = st.text_input("Customer Query", placeholder="e.g. best magnesium supplement for seniors")
    product = st.text_input("Your Product / Brand", placeholder="e.g. Nature Made")
    submitted = st.form_submit_button("Analyze")

if submitted and query and product:
    with st.spinner("Querying 3 AI models simultaneously..."):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/analyze",
                json={"query": query, "product": product}
            )
            data = response.json()

            st.markdown("---")
            st.markdown(f"### Results for: *\"{query}\"*")
            st.markdown(f"**Tracking:** `{product}`")
            st.markdown("---")

            cols = st.columns(len(data["results"]))

            for i, (model_name, result) in enumerate(data["results"].items()):
                analysis = result["analysis"]
                score = analysis["score"]
                rank = analysis["rank"]
                mentioned = analysis["mentioned"]

                with cols[i]:
                    if score == 10:
                        color = "🟢"
                    elif score >= 3:
                        color = "🟡"
                    else:
                        color = "🔴"

                    st.markdown(f"### {color} {model_name}")
                    st.metric("AEO Score", f"{score}/10")
                    st.markdown(f"**Rank:** {rank}")
                    st.markdown(f"**Mentioned:** {'✅ Yes' if mentioned else '❌ No'}")

                    with st.expander("See full response"):
                        st.write(result["response"])

            st.markdown("---")
            scores = [r["analysis"]["score"] for r in data["results"].values()]
            avg = sum(scores) / len(scores)
            st.markdown(f"### 📊 Overall AEO Score: `{avg:.1f}/10`")

            if avg >= 7:
                st.success("Your product has strong AI visibility!")
            elif avg >= 4:
                st.warning("Your product has moderate AI visibility. Room to improve.")
            else:
                st.error("Your product has low AI visibility. Action needed.")

        except Exception as e:
            st.error(f"Error: {e}")