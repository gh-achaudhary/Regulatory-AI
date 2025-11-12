import streamlit as st
import datetime
from typing import List, Dict, Any
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import inch

# --- Seeded Data (Stub) ---
COUNTRIES = [
    "United States", "United Kingdom", "Japan", "United Arab Emirates", "Korea, Republic of",
    "India", "China", "Italy", "Switzerland", "Taiwan", "Spain", "Turkey", "Israel", "Germany", "Canada"
]
PRODUCTS = [
    "Guardant360", "Guardant360 CDx", "GuardantOMNI", "Guardant Reveal", "Shield"
]

# Example stub updates per country
STUB_UPDATES = [
    {
        "id": 1,
        "country": "United States",
        "regulation_name": "CLIA Update 2025",
        "reference_number": "CLIA-2025-01",
        "authority": "CMS",
        "summary": "CLIA regulations updated for NGS-based diagnostics.",
        "key_changes": [
            "Expanded oversight for ctDNA tests.",
            "New reporting requirements.",
            "Shortened compliance window."
        ],
        "effective_date": "2025-12-01",
        "compliance_deadline": "2026-03-01",
        "transition_period": "3 months",
        "applicable": True,
        "impact_level": "CRITICAL",
        "harmonization": ["CLIA", "CAP", "FDA guidance"],
        "affected_products": ["Guardant360", "GuardantOMNI"],
        "rationale": "Immediate compliance required for NGS-based tests."
    },
    {
        "id": 2,
        "country": "Japan",
        "regulation_name": "PMDA Guidance on Liquid Biopsy",
        "reference_number": "PMDA-2025-02",
        "authority": "PMDA",
        "summary": "New guidance for liquid biopsy cancer screening.",
        "key_changes": [
            "Clarified requirements for ctDNA.",
            "Introduced ISO 15189 mapping.",
            "Defined transition period."
        ],
        "effective_date": "2026-01-15",
        "compliance_deadline": "2026-07-15",
        "transition_period": "6 months",
        "applicable": True,
        "impact_level": "HIGH",
        "harmonization": ["ISO 15189", "IMDRF"],
        "affected_products": ["Guardant Reveal"],
        "rationale": "Action required within 3 months for new tests."
    },
    {
        "id": 3,
        "country": "Germany",
        "regulation_name": "EU IVDR Update",
        "reference_number": "IVDR-2025-03",
        "authority": "BfArM",
        "summary": "EU IVDR changes for multi-gene panels.",
        "key_changes": [
            "Expanded scope for NGS panels.",
            "New harmonization with ISO 13485.",
            "Monitoring only for now."
        ],
        "effective_date": "2025-11-01",
        "compliance_deadline": "2026-05-01",
        "transition_period": "6 months",
        "applicable": False,
        "impact_level": "LOW",
        "harmonization": ["ISO 13485", "EU IVDR"],
        "affected_products": [],
        "rationale": "Monitoring only; no immediate action."
    }
]

# --- Helper Functions ---
def group_updates_by_impact(updates: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    buckets = {"CRITICAL": [], "HIGH": [], "MEDIUM": [], "LOW": []}
    for update in updates:
        buckets[update["impact_level"]].append(update)
    return buckets

def render_update_card(update: Dict[str, Any]):
    st.markdown(f"**[{'GUARDANT HEALTH APPLICABLE' if update['applicable'] else 'NOT DIRECTLY APPLICABLE'}]**")
    st.markdown(f"**Country & Regulation**: {update['country']}, {update['regulation_name']} ({update['reference_number']}), {update['authority']}")
    st.markdown(f"**Change Summary**: {update['summary']}")
    st.markdown("**Key Changes:**")
    for change in update['key_changes']:
        st.markdown(f"- {change}")
    st.markdown("**Guardant Health Impact Assessment:**")
    st.markdown(f"- **Impact Level**: {update['impact_level']}")
    rationale = st.text_area(f"Rationale for update {update['id']}", value=update['rationale'], key=f"rationale_{update['id']}")
    affected = st.text_input(f"Affected Products/Operations for update {update['id']}", value=", ".join(update['affected_products']), key=f"affected_{update['id']}")
    st.markdown("**Action Required:**\n1. [Specific compliance step 1]\n2. [Specific compliance step 2]\n3. [Specific compliance step 3]")
    st.markdown(f"**Timeline:**\n- Effective Date: {update['effective_date']}\n- Compliance Deadline: {update['compliance_deadline']}\n- Transition Period: {update['transition_period']}")
    st.markdown(f"**Related Standards or Regulations**: {', '.join(update['harmonization'])}")
    st.markdown("**Cross-Reference:** [Links or notes to similar changes in other countries if applicable]")
    return rationale, affected

def generate_pdf(updates, rationales, affected):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleH = styles["Heading1"]
    styleH2 = styles["Heading2"]
    styleH3 = styles["Heading3"]
    styleN.alignment = TA_LEFT
    elements = []

    # Header
    elements.append(Paragraph("Guardant Health Regulatory Intelligence - MVP Report", styleH))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("Countries: " + ", ".join(COUNTRIES), styleN))
    elements.append(Paragraph("Products: " + ", ".join(PRODUCTS), styleN))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph(f"Generated at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", styleN))
    elements.append(Spacer(1, 0.3*inch))

    # Group updates by impact
    buckets = group_updates_by_impact(updates)
    impact_sections = [
        ("CRITICAL", "Critical or High Priority"),
        ("HIGH", "High Priority"),
        ("MEDIUM", "Medium Priority"),
        ("LOW", "Emerging Trends / No Material Changes")
    ]
    for impact, section_title in impact_sections:
        section_updates = buckets[impact]
        elements.append(Paragraph(section_title, styleH2))
        elements.append(Spacer(1, 0.15*inch))
        if not section_updates:
            elements.append(Paragraph("No updates in this section.", styleN))
            elements.append(Spacer(1, 0.1*inch))
            continue
        for update in section_updates:
            elements.append(Paragraph(f"<b>[{'GUARDANT HEALTH APPLICABLE' if update['applicable'] else 'NOT DIRECTLY APPLICABLE'}]</b>", styleN))
            elements.append(Paragraph(f"<b>Country & Regulation</b>: {update['country']}, {update['regulation_name']} ({update['reference_number']}), {update['authority']}", styleN))
            elements.append(Paragraph(f"<b>Change Summary</b>: {update['summary']}", styleN))
            elements.append(Paragraph("<b>Key Changes:</b>", styleN))
            for change in update['key_changes']:
                elements.append(Paragraph(f"- {change}", styleN))
            elements.append(Paragraph("<b>Guardant Health Impact Assessment:</b>", styleN))
            elements.append(Paragraph(f"- <b>Impact Level</b>: {update['impact_level']}", styleN))
            rationale = rationales.get(update['id'], update['rationale'])
            elements.append(Paragraph(f"- <b>Rationale</b>: {rationale}", styleN))
            affected_str = affected.get(update['id'], ", ".join(update['affected_products']))
            elements.append(Paragraph(f"- <b>Affected Products or Operations</b>: {affected_str}", styleN))
            elements.append(Paragraph("<b>Action Required:</b>", styleN))
            elements.append(Paragraph("1. [Specific compliance step 1]", styleN))
            elements.append(Paragraph("2. [Specific compliance step 2]", styleN))
            elements.append(Paragraph("3. [Specific compliance step 3]", styleN))
            elements.append(Paragraph("<b>Timeline:</b>", styleN))
            elements.append(Paragraph(f"- Effective Date: {update['effective_date']}", styleN))
            elements.append(Paragraph(f"- Compliance Deadline: {update['compliance_deadline']}", styleN))
            elements.append(Paragraph(f"- Transition Period: {update['transition_period']}", styleN))
            elements.append(Paragraph(f"<b>Related Standards or Regulations</b>: {', '.join(update['harmonization'])}", styleN))
            elements.append(Paragraph("<b>Cross-Reference:</b> [Links or notes to similar changes in other countries if applicable]", styleN))
            elements.append(Spacer(1, 0.2*inch))
        elements.append(PageBreak())

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

# --- Streamlit App ---
st.markdown("### Scope")
st.markdown(f"**Countries:** {', '.join(COUNTRIES)}")
st.markdown(f"**Products:** {', '.join(PRODUCTS)}")

st.set_page_config(page_title="Guardant Health Regulatory Intelligence", layout="wide")
st.markdown('<h1 id="main-title" tabindex="0">Guardant Health Regulatory Intelligence - MVP</h1>', unsafe_allow_html=True)

st.markdown('<h2 id="scope-panel" tabindex="0">Scope</h2>', unsafe_allow_html=True)
st.markdown(f'<p aria-label="Countries list"><b>Countries:</b> {', '.join(COUNTRIES)}</p>', unsafe_allow_html=True)
st.markdown(f'<p aria-label="Products list"><b>Products:</b> {', '.join(PRODUCTS)}</p>', unsafe_allow_html=True)

import time as _time
if 'state' not in st.session_state:
    st.session_state['state'] = 'Idle'
    st.session_state['results'] = None
    st.session_state['rationales'] = {}
    st.session_state['affected'] = {}
    st.session_state['logs'] = []

if st.session_state['state'] == 'Idle':
    if st.button("Run Analysis"):
        st.session_state['state'] = 'Running'
        st.session_state['error'] = None
        st.experimental_rerun()
elif st.session_state['state'] == 'Running':
    with st.spinner("Running analysis..."):
        try:
            t0 = _time.time()
            st.session_state['logs'].append(f"Ingestion started at {datetime.datetime.now().strftime('%H:%M:%S')}")
            # Simulate ingestion
            _time.sleep(0.5)
            st.session_state['logs'].append(f"Parsing started at {datetime.datetime.now().strftime('%H:%M:%S')}")
            # Simulate parsing
            _time.sleep(0.5)
            st.session_state['logs'].append(f"Classification started at {datetime.datetime.now().strftime('%H:%M:%S')}")
            # Simulate classification
            _time.sleep(0.5)
            # Simulate error (uncomment to test):
            # raise Exception("Simulated analysis failure.")
            st.session_state['results'] = STUB_UPDATES
            t1 = _time.time()
            st.session_state['logs'].append(f"Analysis complete in {t1-t0:.2f} seconds.")
            st.session_state['state'] = 'Complete'
            st.session_state['error'] = None
            st.experimental_rerun()
        except Exception as e:
            st.session_state['logs'].append(f"Error: {str(e)}")
            st.session_state['error'] = str(e)
            st.session_state['state'] = 'Failure'
            st.experimental_rerun()
elif st.session_state['state'] == 'Complete':
    updates = st.session_state['results']
    buckets = group_updates_by_impact(updates)
    st.markdown('<h2 id="results-section" tabindex="0">Results</h2>', unsafe_allow_html=True)

    # --- Summary Tiles ---
    st.markdown('<div style="display: flex; gap: 2em;">', unsafe_allow_html=True)
    for impact, color in zip(["CRITICAL", "HIGH", "MEDIUM", "LOW"], ["#e74c3c", "#f39c12", "#3498db", "#95a5a6"]):
        st.markdown(f'''<div style="background:{color};color:white;padding:1em 2em;border-radius:8px;min-width:120px;text-align:center;">
            <b>{impact}</b><br>{len(buckets[impact])} update(s)
        </div>''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)

    # --- Collapsible Sections ---
    for impact in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        if buckets[impact]:
            with st.expander(f"{impact} Priority ({len(buckets[impact])})", expanded=True):
                st.markdown(f'<h3 tabindex="0">{impact} Priority</h3>', unsafe_allow_html=True)
                for update in buckets[impact]:
                    rationale, affected = render_update_card(update)
                    st.session_state['rationales'][update['id']] = rationale
                    st.session_state['affected'][update['id']] = affected

    # --- Country List Image Placeholder ---
    st.markdown('<h3 tabindex="0">Country List Visual</h3>', unsafe_allow_html=True)
    st.info("Country list image not found. Please add '/mnt/data/169f5a60-0914-4780-a7f3-1db9e6907549.png' to display the visual.")
    if st.button("Download PDF"):
        t0 = _time.time()
        pdf_bytes = generate_pdf(updates, st.session_state['rationales'], st.session_state['affected'])
        t1 = _time.time()
        st.session_state['logs'].append(f"PDF rendered in {t1-t0:.2f} seconds.")
        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name="guardant_regulatory_report.pdf",
            mime="application/pdf"
        )
    if st.button("Reset"):
        st.session_state['state'] = 'Idle'
        st.session_state['results'] = None
        st.session_state['rationales'] = {}
        st.session_state['affected'] = {}
        st.session_state['logs'] = []
        st.session_state['error'] = None
        st.experimental_rerun()
elif st.session_state['state'] == 'Failure':
    st.error("An error occurred during analysis.")
    if st.session_state.get('error'):
        st.markdown(f"**Error details:** {st.session_state['error']}")
    if st.button("Retry"):
        st.session_state['state'] = 'Idle'
        st.session_state['error'] = None
        st.experimental_rerun()
else:
    st.error("An error occurred. Please try again.")
    if st.button("Retry"):
        st.session_state['state'] = 'Idle'
        st.experimental_rerun()

# --- Observability: Show logs in sidebar ---
with st.sidebar:
    st.markdown('<h2 tabindex="0">App Logs</h2>', unsafe_allow_html=True)
    for log in st.session_state.get('logs', []):
        st.markdown(f"- {log}")
