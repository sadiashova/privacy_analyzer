import io
import requests
import streamlit as st
from analyzer.pipeline import analyze_policy

CATEGORY_META = {
    "collection": {"icon": "📥", "title": "Personal Data Collected"},
    "purpose": {"icon": "🎯", "title": "Processing Purpose"},
    "sharing": {"icon": "🤝", "title": "Third-Party Sharing"},
    "tracking": {"icon": "🍪", "title": "Tracking & Cookies"},
    "retention": {"icon": "⏳", "title": "Data Retention Duration"},
    "security": {"icon": "🔒", "title": "Security & Encryption"},
    "rights": {"icon": "⚖️", "title": "User Rights & Choices"},
}

SAMPLE_EN = (
    "Example Privacy Policy:\n\n"
    "We collect your email address, full name, phone number, and device location to provide and improve our service.\n"
    "We share personal information with trusted advertising partners and analytics providers for marketing purposes.\n"
    "We utilize cookies, pixels, and tracking beacons to personalize content and track usage activity.\n"
    "We retain your data for as long as your account remains active or up to five years after termination.\n"
    "All communications and data are encrypted using industry-standard TLS and stored securely.\n"
    "You have the right to access, rectify, or request deletion of your information at any time."
)

SAMPLE_DA = (
    "Eksempel på Privatlivspolitik:\n\n"
    "Vi indsamler dit navn, e-mailadresse, telefonnummer og placering for at levere og forbedre vores tjenester.\n"
    "Vi deler dine oplysninger med vores betroede tredjeparts partnere og annoncører.\n"
    "Vi anvender cookies og sporing for at analysere brugernes adfærd.\n"
    "Vi opbevarer dine personoplysninger i op til fem år.\n"
    "Vi beskytter dine data med sikker kryptering og adgangskontrol.\n"
    "Du har ret til indsigt samt ret til at få dine oplysninger slettet."
)


def generate_markdown_report(result):
    md = [
        "# Privacy Policy Inspection Report\n",
        f"**Risk Level:** {result['risk']['level']} (Score: {result['risk']['score']})",
        f"**Detected Language:** {result['language']}\n",
        "## Risk Factors",
    ]
    for pts, reason in result["risk"]["factors"]:
        md.append(f"- **{pts}**: {reason}")
    md.append("\n## Category Disclosures")
    for cat, sentences in result["findings"].items():
        title = CATEGORY_META.get(cat, {}).get("title", cat.title())
        if sentences:
            md.append(f"### {title}")
            for s in sentences:
                md.append(f"> {s}\n")
        else:
            md.append(f"### {title}\n*Not clearly mentioned.*\n")
    return "\n".join(md)


def render_dashboard(result):
    st.divider()
    st.markdown("## 📊 Analysis Dashboard")

    risk_info = result["risk"]
    level = risk_info["level"]
    score = risk_info["score"]
    lang = result["language"]
    findings = result["findings"]

    # Level styling config
    if level == "Low":
        badge_cls = "badge-low"
        badge_icon = "🛡️"
        bar_val = min(max(score / 10.0, 0.1), 0.35)
    elif level == "Medium":
        badge_cls = "badge-medium"
        badge_icon = "⚠️"
        bar_val = min(max(score / 10.0, 0.4), 0.75)
    else:
        badge_cls = "badge-high"
        badge_icon = "🚨"
        bar_val = 1.0

    # Top KPI Metrics Cards
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 6px;">RISK TIER</div>
                <div class="badge-pill {badge_cls}">{badge_icon} {level.upper()} RISK</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 6px;">RISK SCORE</div>
                <div style="font-size: 1.6rem; font-weight: 700;">{score} <span style="font-size: 0.85rem; font-weight: 400; color: #94a3b8;">/ 10</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        lang_label = "🌐 English (EN)" if lang == "en" else ("🌐 Danish (DA)" if lang == "da" else f"🌐 {lang.upper()}")
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 6px;">DETECTED LANGUAGE</div>
                <div style="font-size: 1.3rem; font-weight: 600;">{lang_label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        found_count = sum(1 for v in findings.values() if len(v) > 0)
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 6px;">DISCLOSURES FOUND</div>
                <div style="font-size: 1.3rem; font-weight: 600;">{found_count} of {len(findings)} <span style="font-size: 0.85rem; font-weight: 400; color: #94a3b8;">topics</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Risk Meter Progress Bar
    st.progress(bar_val)

    # 2-Column Split: Risk Factors on Left, Category Insights on Right
    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.markdown("### ⚠️ Risk Factors Identified")
        if risk_info["factors"]:
            for points, reason in risk_info["factors"]:
                cls = "factor-pill-danger" if points.startswith("+") else "factor-pill-safe"
                icon = "🔺" if points.startswith("+") else "🔻"
                st.markdown(
                    f"""
                    <div class="{cls}">
                        <strong>{icon} {points} pts</strong> — {reason}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                """
                <div class="factor-pill-safe">
                    ✅ <strong>Clean Assessment</strong> — No elevated risk factors identified.
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        # Export Report Button
        report_data = generate_markdown_report(result)
        st.download_button(
            label="📥 Export Report (Markdown)",
            data=report_data,
            file_name="privacy_policy_report.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with col_right:
        st.markdown("### 🔍 Category-by-Category Findings")
        for cat_key, meta in CATEGORY_META.items():
            sentences = findings.get(cat_key, [])
            icon = meta["icon"]
            title = meta["title"]

            if sentences:
                badge_html = f"<span style='color: #10b981; font-weight: 600;'>● {len(sentences)} sentence(s)</span>"
                st.markdown(
                    f"""
                    <div class="category-box present">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <strong>{icon} {title}</strong>
                            {badge_html}
                        </div>
                        <div style="font-size: 0.95rem; font-style: italic; color: #cbd5e1;">
                            "{sentences[0][:260]}{'...' if len(sentences[0]) > 260 else ''}"
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if len(sentences) > 1:
                    with st.expander(f"View all {len(sentences)} extracted disclosures for {title}"):
                        for idx, s in enumerate(sentences, 1):
                            st.markdown(f"**{idx}.** {s}")
            else:
                st.markdown(
                    f"""
                    <div class="category-box absent">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <strong>{icon} {title}</strong>
                            <span style="color: #64748b; font-size: 0.85rem;">Not clearly mentioned</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def main():
    st.set_page_config(
        page_title="Privacy Policy Inspector",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom Styling (Dark & Light Theme Friendly)
    st.markdown(
        """
        <style>
        /* Global Card Style */
        .metric-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 12px;
            padding: 18px 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            transition: transform 0.15s ease;
        }
        .metric-card:hover {
            transform: translateY(-2px);
        }
        
        /* Risk Badge Styles */
        .badge-pill {
            display: inline-block;
            padding: 4px 14px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.88rem;
            letter-spacing: 0.5px;
        }
        .badge-low {
            background: rgba(16, 185, 129, 0.18);
            color: #10b981;
            border: 1px solid rgba(16, 185, 129, 0.4);
        }
        .badge-medium {
            background: rgba(245, 158, 11, 0.18);
            color: #f59e0b;
            border: 1px solid rgba(245, 158, 11, 0.4);
        }
        .badge-high {
            background: rgba(239, 68, 68, 0.18);
            color: #ef4444;
            border: 1px solid rgba(239, 68, 68, 0.4);
        }
        
        /* Category Card Styles */
        .category-box {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-left: 4px solid #3b82f6;
            border-radius: 8px;
            padding: 14px 16px;
            margin-bottom: 12px;
        }
        .category-box.present {
            border-left-color: #10b981;
        }
        .category-box.absent {
            border-left-color: #64748b;
            opacity: 0.75;
        }
        
        /* Risk Factor Pill */
        .factor-pill-danger {
            background: rgba(239, 68, 68, 0.12);
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: #f87171;
            padding: 6px 12px;
            border-radius: 8px;
            margin-bottom: 8px;
            font-size: 0.92rem;
        }
        .factor-pill-safe {
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: #34d399;
            padding: 6px 12px;
            border-radius: 8px;
            margin-bottom: 8px;
            font-size: 0.92rem;
        }
        /* Primary Action Button */
        button[kind="primary"] {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            border: none !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            letter-spacing: 0.3px !important;
            border-radius: 8px !important;
            padding: 0.6rem 1.2rem !important;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25) !important;
            transition: all 0.2s ease !important;
        }
        button[kind="primary"]:hover {
            background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
            box-shadow: 0 6px 18px rgba(37, 99, 235, 0.4) !important;
            transform: translateY(-1px) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ----------------- SIDEBAR -----------------
    with st.sidebar:
        st.markdown("### 🛡️ Privacy Inspector")
        st.caption("Automated Transparency & Risk Analysis Engine")
        st.divider()

        st.markdown("#### 📊 Risk Scoring Weights")
        st.markdown(
            """
            - **Data Sharing:** `+3 pts`
            - **≥ 3 Personal Data Types:** `+3 pts`
            - **Tracking / Cookies:** `+2 pts`
            - **User Rights Granted:** `-1 pt`
            
            **Tiers:**
            - 🟢 **Low Risk:** ≤ 3
            - 🟡 **Medium Risk:** 4 - 7
            - 🔴 **High Risk:** ≥ 8
            """
        )
        st.divider()
        st.markdown("#### 🌐 Supported Languages")
        st.markdown("• **English** (`EN`)\n• **Danish** (`DA`)")
        st.divider()
        st.caption("🔒 **Client-Side Privacy:** Analyzed text is processed in memory and never persisted externally.")

    # ----------------- HERO HEADER -----------------
    st.title("🛡️ Privacy Policy Analyzer")
    st.markdown(
        "Perform automated transparency audits, inspect third-party tracking, and calculate compliance risk scores in seconds."
    )

    # ----------------- INPUT SECTION -----------------
    tab_text, tab_url = st.tabs(["📄 Paste Policy Text", "🌐 Analyze from Web URL"])

    input_text = None
    input_url = None

    with tab_text:
        col_t1, col_t2 = st.columns([3, 1])
        with col_t2:
            st.markdown("**Sample Presets:**")
            if st.button("🇺🇸 English Example", use_container_width=True):
                st.session_state["policy_text_input"] = SAMPLE_EN
            if st.button("🇩🇰 Danish Example", use_container_width=True):
                st.session_state["policy_text_input"] = SAMPLE_DA
            if st.button("🗑️ Clear Text", use_container_width=True):
                st.session_state["policy_text_input"] = ""

        with col_t1:
            default_val = st.session_state.get("policy_text_input", "")
            pasted_text = st.text_area(
                "Paste Privacy Policy Text:",
                value=default_val,
                height=240,
                placeholder="Paste privacy policy text here (minimum 50 characters)...",
            )
            if st.button("🔍 Analyze Pasted Text", type="primary", use_container_width=True):
                if not pasted_text.strip():
                    st.warning("Please paste some privacy policy text first.")
                else:
                    input_text = pasted_text

    with tab_url:
        col_u1, col_u2 = st.columns([3, 1])
        with col_u2:
            st.markdown("**Example Links:**")
            if st.button("🔗 LinkedIn Policy", use_container_width=True):
                st.session_state["policy_url_input"] = "https://www.linkedin.com/legal/privacy-policy"
            if st.button("🔗 GitHub Privacy", use_container_width=True):
                st.session_state["policy_url_input"] = "https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement"

        with col_u1:
            default_url = st.session_state.get("policy_url_input", "")
            entered_url = st.text_input(
                "Enter Privacy Policy URL:",
                value=default_url,
                placeholder="https://example.com/privacy",
            )
            if st.button("🌐 Fetch & Analyze URL", type="primary", use_container_width=True):
                entered_url = entered_url.strip()
                if not entered_url:
                    st.warning("Please enter a valid web URL.")
                else:
                    if not entered_url.startswith(("http://", "https://")):
                        entered_url = "https://" + entered_url
                    input_url = entered_url

    # Trigger Execution
    active_text = input_text
    active_url = input_url

    if active_text or active_url:
        try:
            with st.spinner("Analyzing disclosures, tracking markers, and privacy risks..."):
                result = analyze_policy(text=active_text, url=active_url)
                st.session_state["latest_result"] = result
        except ValueError as err:
            st.error(f"⚠️ Validation Error: {err}")
        except requests.RequestException:
            st.error("🌐 Network Error: Could not fetch text from the provided URL. Please verify the URL.")
        except Exception as err:
            st.error(f"❌ Unexpected Error: {err}")

    # Show persisted result if available
    if "latest_result" in st.session_state:
        render_dashboard(st.session_state["latest_result"])


if __name__ == "__main__":
    main()
