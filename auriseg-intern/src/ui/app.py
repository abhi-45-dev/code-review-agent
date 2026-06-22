import inspect
import json
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))
import pandas as pd
import plotly.express as px

import streamlit as st
from repo_handler import prepare_repository
from src.agent.run_agent import run_agent

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Auriseg AI Code Reviewer", page_icon="🛡️", layout="wide"
)

# ==========================================
# LOAD CSS
# ==========================================

CSS_PATH = (
    Path(__file__).resolve().parent
    / "assets"
    / "styles.css"
)

with open(CSS_PATH) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==========================================
# SESSION STATE
# ==========================================

if "repo_path" not in st.session_state:
    st.session_state.repo_path = None

if "reports" not in st.session_state:
    st.session_state.reports = None

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:
    st.header("Repository Input")

    input_type = st.radio("Input Type", ["Single File", "ZIP Repository"])

    st.divider()

    st.header("Review Categories")

    bugs = st.checkbox("🐞 Bugs", value=True)
    security = st.checkbox("🔒 Security", value=True)
    quality = st.checkbox("⚙️ Quality", value=True)
    improvements = st.checkbox("💡 Improvements", value=True)

    st.divider()

    st.header("Provider")

    provider = st.selectbox("Model Provider", ["Groq"])

# ==========================================
# HEADER
# ==========================================

st.title("🔥 Auriseg AI Code Reviewer")

st.caption(
    "AI-Powered Security Analysis, Bug Detection and Code Quality Review"
)

st.divider()

# ==========================================
# UPLOAD SECTION
# ==========================================

st.subheader("📂 Upload Repository")

if input_type == "Single File":
    uploaded_file = st.file_uploader(
        "Upload source file",
        type=["py", "js", "ts", "java", "cpp", "c", "go", "php"],
    )
else:
    uploaded_file = st.file_uploader("Upload ZIP repository", type=["zip"])

# ==========================================
# FILE / ZIP PROCESSING FLOW
# ==========================================

if uploaded_file:
    st.success(f"Loaded: {uploaded_file.name}")

    # ==========================================
    # SINGLE FILE FLOW
    # ==========================================
    if input_type == "Single File":
        upload_dir=Path("uploads")
        if upload_dir.exists():
            import shutil
            shutil.rmtree(upload_dir)
        upload_dir.mkdir(exist_ok=True)    

        file_path = upload_dir / uploaded_file.name

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.session_state.repo_path = str(upload_dir)

    # ==========================================
    # ZIP FLOW
    # ==========================================
    elif input_type == "ZIP Repository":
        if st.button("📦 Extract Repository", use_container_width=True):
            with st.spinner("Extracting repository..."):
                repo_path = prepare_repository(uploaded_file)
                st.session_state.repo_path = repo_path

            st.success("Repository extracted successfully.")

# ==========================================
# EXTRACTED REPO
# ==========================================

if st.session_state.repo_path:
    st.subheader("Extracted Repository Path")
    st.code(st.session_state.repo_path)
    st.divider()

    if st.button(
        "🚀 Analyze Repository", use_container_width=True, type="primary"
    ):
        with st.spinner("Running AI code review..."):
            reports = run_agent(st.session_state.repo_path)
            st.session_state.reports = reports

        st.success(
            f"Analysis complete. Files analyzed: {len(reports)}"
        )

# ==========================================
# RESULTS & REPOSITORY SUMMARY
# ==========================================

if st.session_state.reports:
    reports = st.session_state.reports
    total_files = len(reports)

    critical_count = 0
    high_count = 0
    medium_count = 0
    low_count = 0
    info_count = 0
    owasp_counts = {}
    cwe_counts = {}

    # Correctly indented single-pass loops to gather summary metrics
    for report in reports.values():
        json_report = report.get("json_report", {})
        summary = json_report.get("summary", {})

        critical_count += summary.get("critical_count", 0)
        high_count += summary.get("high_count", 0)
        medium_count += summary.get("medium_count", 0)
        low_count += summary.get("low_count", 0)
        info_count += summary.get("info_count", 0)

        findings = json_report.get("findings", [])
        if findings:
            st.write(findings[0])
        for finding in findings:
            owasp = finding.get("owasp_category")
            if owasp:
                owasp_counts[owasp] = owasp_counts.get(owasp, 0) + 1

            cwe = finding.get("cwe_id")
            if cwe:
                cwe_counts[cwe] = cwe_counts.get(cwe, 0) + 1

    # ==========================================
    # DISTRIBUTION METRICS
    # ==========================================

    st.subheader("🛡️ OWASP Top 10 Distribution")

    if owasp_counts:
        owasp_df = pd.DataFrame(
            {
                "OWASP": list(owasp_counts.keys()),
                "Count": list(owasp_counts.values())
            }
        )

        fig_owasp = px.bar(
            owasp_df,
            x="OWASP",
            y="Count",
            title="OWASP Findings Distribution"
        )

        st.plotly_chart(
            fig_owasp,
            use_container_width=True
        )

    st.divider()

    st.subheader("📚 CWE Distribution")

    if cwe_counts:
        cwe_df = pd.DataFrame(
            {
                "CWE": list(cwe_counts.keys()),
                "Count": list(cwe_counts.values())
            }
        )

        fig_cwe = px.bar(
            cwe_df,
            x="CWE",
            y="Count",
            title="CWE Findings Distribution"
        )

        st.plotly_chart(
            fig_cwe,
            use_container_width=True
        )

    st.divider()

    # ==========================================
    # OVERALL COUNTS
    # ==========================================

    st.subheader("📈 Repository Summary")
    
    severity_df = pd.DataFrame(
        {
            "Severity": [
                "Critical",
                "High",
                "Medium",
                "Low",
                "Info"
            ],
            "Count": [
                critical_count,
                high_count,
                medium_count,
                low_count,
                info_count
            ]
        }
    )

    fig_severity = px.pie(
        severity_df,
        names="Severity",
        values="Count",
        title="Severity Distribution"
    )

    st.plotly_chart(
        fig_severity,
        use_container_width=True
    )

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric("Files", total_files)
    with col2:
        st.metric("Critical", critical_count)
    with col3:
        st.metric("High", high_count)
    with col4:
        st.metric("Medium", medium_count)
    with col5:
        st.metric("Low", low_count)
    with col6:
        st.metric("Info", info_count)

    st.divider()

    # ==========================================
    # DETAILED PER-FILE EXPANDERS
    # ==========================================

    st.subheader("📊 Analysis Results")
    st.write(f"Files analyzed: {len(reports)}")

    for filename, report in reports.items():
        with st.expander(f"📄 {filename}", expanded=False):
            json_report = report.get("json_report", {})
            summary = json_report.get("summary", {})

            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.metric("Critical", summary.get("critical_count", 0))
            with col2:
                st.metric("High", summary.get("high_count", 0))
            with col3:
                st.metric("Medium", summary.get("medium_count", 0))
            with col4:
                st.metric("Low", summary.get("low_count", 0))
            with col5:
                st.metric("Info", summary.get("info_count", 0))

            findings = json_report.get("findings", [])

            # Correctly indented findings block inside the file expander
            for finding in findings:
                severity = finding.get("severity", "Info").lower()

                # 1. Strip out nested/accidental code lines coming from finding text elements
                issue_title = finding.get("issue", "Finding")
                category_text = finding.get("category", "N/A")
                severity_text = finding.get("severity", "Info")
                location_text = finding.get("line_hint", "N/A")
                explanation_text = finding.get("explanation", "")

                # New parameters from finding configuration definitions
                confidence_text = finding.get("confidence", "")
                cwe_text = finding.get("cwe_id", "")
                owasp_text = finding.get("owasp_category", "")
                remediation_text = finding.get("remediation", "")

                # 2. Use clean, dedicated HTML parsing with st.html() to bypass markdown interpreter completely
                html_content = inspect.cleandoc(f"""
                    <div class="finding-card severity-{severity}">
                        <div class="finding-title">
                            {issue_title}
                        </div>
                        <div class="finding-text">
                            <b>Category:</b> {category_text}<br>
                            <b>Severity:</b> {severity_text}<br>
                            <b>Location:</b> {location_text}<br>
                            {"<b>Confidence:</b> " + confidence_text + "<br>" if confidence_text else ""}
                            {"<b>CWE:</b> " + cwe_text + "<br>" if cwe_text else ""}
                            {"<b>OWASP:</b> " + owasp_text + "<br>" if owasp_text else ""}
                            <br>
                            {explanation_text}
                            {"<br><br><b>Remediation:</b> " + remediation_text if remediation_text else ""}
                        </div>
                    </div>
                """)

                st.html(html_content)

    st.divider()

    # ==========================================
    # EXPORT SECTION
    # ==========================================

    st.subheader("📄 Export Reports")

    report_json = json.dumps(
        reports,
        indent=4
    )

    # Aggregate markdown data from all analyzed files
    all_markdown = ""
    for filename, report in reports.items():
        all_markdown += report.get(
            "markdown_report",
            ""
        )
        all_markdown += "\n\n"

    # Split export utilities into side-by-side columns
    export_col1, export_col2 = st.columns(2)

    with export_col1:
        st.download_button(
            "⬇ Download JSON Report",
            data=report_json,
            file_name="auriseg_report.json",
            mime="application/json",
            use_container_width=True
        )

    with export_col2:
        st.download_button(
            "⬇ Download Markdown Report",
            data=all_markdown,
            file_name="auriseg_report.md",
            mime="text/markdown",
            use_container_width=True
        )