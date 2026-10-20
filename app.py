import requests
import streamlit as st
from analyzer.pipeline import analyze_policy

st.set_page_config(page_title="Privacy Policy Analyzer", page_icon="🔒")


def show_results(result):
    """Display the analysis results on the page."""
    st.subheader("Results")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Risk Level", result["risk"]["level"])
    with col2:
        st.metric("Risk Score", result["risk"]["score"])

    st.subheader("Risk Factors")
    if result["risk"]["factors"]:
        for points, reason in result["risk"]["factors"]:
            st.write(f"{points} – {reason}")
    else:
        st.write("No risk factors found.")

    st.subheader("Summary")
    for line in result["summary"]:
        st.markdown(f"- {line}")

    st.subheader("Detected Language")
    st.write(result["language"])


def run_analysis(text=None, url=None):
    """Run the analysis and show a friendly message if something goes wrong."""
    try:
        with st.spinner("Analyzing..."):
            result = analyze_policy(text=text, url=url)
        show_results(result)
    except ValueError as error:
        st.error(str(error))
    except requests.RequestException:
        st.error("Could not download that page. Check the URL and try again.")


st.title("Privacy Policy Analyzer")
st.markdown("Paste a privacy policy or enter a URL to analyze its risk level.")

tab1, tab2 = st.tabs(["Paste Text", "Enter URL"])

with tab1:
    text = st.text_area("Paste the privacy policy text here:", height=300)
    if st.button("Analyze Text"):
        if not text.strip():
            st.error("Please paste some text.")
        else:
            run_analysis(text=text)

with tab2:
    url = st.text_input("Enter the privacy policy URL:")
    if st.button("Analyze URL"):
        url = url.strip()
        if not url:
            st.error("Please enter a URL.")
        else:
            # Add https:// automatically if the user forgot it
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            run_analysis(url=url)
